import tkinter as tk
import math
from datetime import datetime

hour_positions = {
    1:  (270, 90),
    2:  (310, 135),
    3:  (325, 200),
    4:  (310, 265),
    5:  (270, 310),
    6:  (200, 325),
    7:  (130, 310),
    8:  (90, 265),
    9:  (75, 200),
    10: (90, 135),
    11: (130, 90),
    12: (200, 75)
}

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyCircularList:
    def __init__(self, limit):
        self.start = None
        prev = None
        for i in range(limit):
            new_node = Node(i)
            if self.start is None:
                self.start = new_node
            else:
                prev.next = new_node
                new_node.prev = prev
            prev = new_node
        prev.next = self.start
        self.start.prev = prev

class Clock:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cx, self.cy = 200, 200

        self.seconds = DoublyCircularList(60)
        self.minutes = DoublyCircularList(60)
        self.hours = DoublyCircularList(12)

        self.roman = True
        self.after_id = None

        self.set_time_from_system()
        self.draw_dial()
        self.update()

    def draw_dial(self):
        self.canvas.delete("dial")
        self.canvas.create_oval(50, 50, 350, 350, outline="#D4AF37", width=4, tags="dial")
        self.canvas.create_oval(60, 60, 340, 340, outline="#222", width=4, tags="dial")

        roman_numerals = {
            1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
            7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"
        }

        for hour, (x, y) in hour_positions.items():
            text = roman_numerals[hour] if self.roman else str(hour)
            self.canvas.create_text(x, y, text=text, fill="white", font=("Times New Roman", 16, "bold"), tags="dial")

        self.canvas.create_oval(self.cx - 5, self.cy - 5, self.cx + 5, self.cy + 5,
                                fill="white", outline="white", tags="dial")

    def draw_hand(self, value, kind):
        angle_deg = (value * 6) - 90 if kind != "hour" else (value * 30) - 90
        angle_rad = math.radians(angle_deg)

        length = 70 if kind == "sec" else 60 if kind == "min" else 45
        width = 1 if kind == "sec" else 3 if kind == "min" else 5
        color = "red" if kind == "sec" else "blue" if kind == "min" else "white"

        x = self.cx + length * math.cos(angle_rad)
        y = self.cy + length * math.sin(angle_rad)

        self.canvas.create_line(self.cx, self.cy, x, y, fill=color, width=width, tags="hand")

    def advance(self):
        self.current_sec = self.current_sec.next
        if self.current_sec.value == 0:
            self.current_min = self.current_min.next
            if self.current_min.value == 0:
                self.current_hour = self.current_hour.next

    def update(self):
        self.canvas.delete("hand")
        self.draw_hand(self.current_sec.value, "sec")
        self.draw_hand(self.current_min.value, "min")
        self.draw_hand(self.current_hour.value, "hour")

        self.advance()
        self.after_id = self.canvas.after(1000, self.update)

    def stop(self):
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def set_time(self, h, m, s):
        if not (0 <= h <= 11 and 0 <= m <= 59 and 0 <= s <= 59):
            return

        self.stop()

        self.current_hour = self.hours.start
        for _ in range(h):
            self.current_hour = self.current_hour.next

        self.current_min = self.minutes.start
        for _ in range(m):
            self.current_min = self.current_min.next

        self.current_sec = self.seconds.start
        for _ in range(s):
            self.current_sec = self.current_sec.next

        self.update()

    def set_time_from_system(self):
        now = datetime.now()
        h = now.hour % 12
        m = now.minute
        s = now.second
        self.set_time(h, m, s)

    def toggle_numeration(self):
        self.roman = not self.roman
        self.draw_dial()

def start_application():
    window = tk.Tk()
    window.title("Traditional Analog Clock")
    window.configure(bg="black")

    canvas = tk.Canvas(window, width=400, height=400, bg="black", highlightthickness=0)
    canvas.pack()

    clock = Clock(canvas)

    input_frame = tk.Frame(window, bg="black")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Hour:", fg="white", bg="black").grid(row=0, column=0)
    entry_h = tk.Entry(input_frame, width=3)
    entry_h.grid(row=0, column=1)

    tk.Label(input_frame, text="Min:", fg="white", bg="black").grid(row=0, column=2)
    entry_m = tk.Entry(input_frame, width=3)
    entry_m.grid(row=0, column=3)

    tk.Label(input_frame, text="Sec:", fg="white", bg="black").grid(row=0, column=4)
    entry_s = tk.Entry(input_frame, width=3)
    entry_s.grid(row=0, column=5)

    def set_clock():
        try:
            h = int(entry_h.get()) % 12
            m = int(entry_m.get()) % 60
            s = int(entry_s.get()) % 60
            clock.set_time(h, m, s)
        except ValueError:
            pass

    button = tk.Button(input_frame, text="Set", command=set_clock)
    button.grid(row=0, column=6, padx=10)

    toggle_button = tk.Button(window, text="Toggle Style (Roman / Normal)", command=clock.toggle_numeration, bg="#444", fg="white")
    toggle_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    start_application()
