import tkinter as tk
import time
import math
from datetime import datetime

class AnalogClock(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=400, height=450, bg='#1E1E1E')
        self.configure(highlightthickness=0)
        self.zoom_scale = 1.0
        self.is_animating = False
        self.center_x = 200
        self.center_y = 200
        self.create_clock_face()
        self.hands = self.create_hands()
        self.update_clock()
        
        # Bind mouse events
        self.bind('<Enter>', self.zoom_in)
        self.bind('<Leave>', self.zoom_out)

    def zoom_in(self, event):
        if not self.is_animating:
            self.animate_zoom(1.0, 1.2)

    def zoom_out(self, event):
        if not self.is_animating:
            self.animate_zoom(1.2, 1.0)

    def animate_zoom(self, start, end):
        steps = 10
        step_size = (end - start) / steps
        self.is_animating = True

        def animate_step(step):
            if step <= steps:
                self.zoom_scale = start + (step * step_size)
                self.delete('all')
                self.create_clock_face()
                self.hands = self.create_hands()
                if step < steps:
                    self.after(20, lambda: animate_step(step + 1))
                else:
                    self.is_animating = False
            
        animate_step(0)

    def create_clock_face(self):
        # Scale all coordinates based on zoom_scale
        radius = 150 * self.zoom_scale
        
        # Clock circle
        self.create_oval(
            self.center_x - radius, self.center_y - radius,
            self.center_x + radius, self.center_y + radius,
            width=2, outline='#4A90E2', fill='#2D2D2D'
        )
        
        # Hour markers and numbers
        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            marker_length = 15 * self.zoom_scale
            start_x = self.center_x + (radius - marker_length) * math.cos(angle)
            start_y = self.center_y + (radius - marker_length) * math.sin(angle)
            end_x = self.center_x + radius * math.cos(angle)
            end_y = self.center_y + radius * math.sin(angle)
            
            # Draw hour numbers
            number = 12 if i == 0 else i
            num_radius = (radius - 30) * self.zoom_scale
            num_x = self.center_x + num_radius * math.cos(angle)
            num_y = self.center_y + num_radius * math.sin(angle)
            self.create_text(num_x, num_y, text=str(number),
                           font=('Helvetica', int(12 * self.zoom_scale)),
                           fill='#FFFFFF')
            
            # Draw markers
            width = 5 if i % 3 == 0 else 2
            color = '#4A90E2' if i % 3 == 0 else '#808080'
            self.create_line(start_x, start_y, end_x, end_y,
                           width=width, fill=color)

        # Center dot
        dot_size = 5 * self.zoom_scale
        self.create_oval(
            self.center_x - dot_size, self.center_y - dot_size,
            self.center_x + dot_size, self.center_y + dot_size,
            fill='#4A90E2'
        )

    def create_hands(self):
        # Create initial hands
        hour_hand = self.create_line(0, 0, 0, 0, width=8, fill='#4A90E2')
        minute_hand = self.create_line(0, 0, 0, 0, width=4, fill='#FFFFFF')
        second_hand = self.create_line(0, 0, 0, 0, width=2, fill='#FF4444')
        return [hour_hand, minute_hand, second_hand]

    def update_clock(self):
        # Get current time
        now = datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second

        # Modify hand lengths based on zoom_scale
        hour_length = 80 * self.zoom_scale
        minute_length = 120 * self.zoom_scale
        second_length = 130 * self.zoom_scale
        
        # Hour hand
        hour_angle = (hours + minutes/60) * math.pi/6 - math.pi/2
        self.coords(self.hands[0], self.center_x, self.center_y,
            self.center_x + hour_length * math.cos(hour_angle),
            self.center_y + hour_length * math.sin(hour_angle))

        # Minute hand
        minute_angle = minutes * math.pi/30 - math.pi/2
        self.coords(self.hands[1], self.center_x, self.center_y,
            self.center_x + minute_length * math.cos(minute_angle),
            self.center_y + minute_length * math.sin(minute_angle))

        # Second hand
        second_angle = seconds * math.pi/30 - math.pi/2
        self.coords(self.hands[2], self.center_x, self.center_y,
            self.center_x + second_length * math.cos(second_angle),
            self.center_y + second_length * math.sin(second_angle))

        # Update date and time text
        self.delete('time_text')
        current_time = now.strftime('%H:%M:%S')
        current_date = now.strftime('%B %d, %Y')
        self.create_text(self.center_x, 400, text=f'{current_time}\n{current_date}',
                        fill='#FFFFFF', font=('Helvetica', 14), tags='time_text')

        # Schedule next update
        self.after(1000, self.update_clock)

def main():
    root = tk.Tk()
    root.title("Arch's Analog Clock")
    root.configure(bg='#1E1E1E')
    root.resizable(False, False)
    
    clock = AnalogClock(root)
    clock.pack(padx=20, pady=20)
    
    root.mainloop()

if __name__ == '__main__':
    main()
