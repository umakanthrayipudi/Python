import tkinter as tk
from tkinter import messagebox
import time
import pickle

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer with Memory")
        master.geometry("400x250")

        self.time_left = 0
        self.is_running = False
        self.last_timer_file = "last_timer.pkl"

        self.load_last_timer()

        self.time_label = tk.Label(master, text="00:00:00", font=("Arial", 40))
        self.time_label.pack(pady=10)

        self.input_frame = tk.Frame(master)
        self.input_frame.pack()

        self.hour_entry = self.create_time_entry(self.input_frame, "Hours")
        self.minute_entry = self.create_time_entry(self.input_frame, "Minutes")
        self.second_entry = self.create_time_entry(self.input_frame, "Seconds")

        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(self.btn_frame, text="Reset", command=self.reset_timer)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.load_btn = tk.Button(self.btn_frame, text="Load Last", command=self.load_last_timer_display)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_time_entry(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(side=tk.LEFT, padx=5)
        label = tk.Label(frame, text=label_text)
        label.pack()
        entry = tk.Entry(frame, width=5)
        entry.insert(0, "00")
        entry.pack()
        return entry

    def start_timer(self):
        if not self.is_running:
            try:
                hours = int(self.hour_entry.get())
                minutes = int(self.minute_entry.get())
                seconds = int(self.second_entry.get())
                self.time_left = hours * 3600 + minutes * 60 + seconds
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")
                return

            self.is_running = True
            self.start_btn.config(text="Stop", command=self.stop_timer)
            self.update_timer()

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.display_time(self.time_left)
            self.master.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.stop_timer()
            messagebox.showinfo("Timer Done", "Time is up!")

    def stop_timer(self):
        self.is_running = False
        self.start_btn.config(text="Start", command=self.start_timer)

    def reset_timer(self):
        self.stop_timer()
        self.save_last_timer(self.time_left)
        self.time_left = 0
        self.display_time(self.time_left)
        self.hour_entry.delete(0, tk.END)
        self.hour_entry.insert(0, "00")
        self.minute_entry.delete(0, tk.END)
        self.minute_entry.insert(0, "00")
        self.second_entry.delete(0, tk.END)
        self.second_entry.insert(0, "00")

    def display_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        self.time_label.config(text=f"{hours:02}:{minutes:02}:{secs:02}")

    def save_last_timer(self, timer_value):
        with open(self.last_timer_file, 'wb') as f:
            pickle.dump(timer_value, f)

    def load_last_timer(self):
        try:
            with open(self.last_timer_file, 'rb') as f:
                self.time_left = pickle.load(f)
                self.display_time(self.time_left)
        except (FileNotFoundError, pickle.UnpicklingError):
            self.time_left = 0
            self.display_time(self.time_left)

    def load_last_timer_display(self):
        self.load_last_timer()
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = self.time_left % 60

        self.hour_entry.delete(0, tk.END)
        self.hour_entry.insert(0, f"{hours:02}")
        self.minute_entry.delete(0, tk.END)
        self.minute_entry.insert(0, f"{minutes:02}")
        self.second_entry.delete(0, tk.END)
        self.second_entry.insert(0, f"{seconds:02}")
        self.display_time(self.time_left)


    def on_closing(self):
        if self.is_running:
            self.save_last_timer(self.time_left)
        elif self.time_left > 0:
             self.save_last_timer(self.time_left)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
