import tkinter as tk
from tkinter import messagebox
import random

class Job:
    def __init__(self, from_city, to_city, transport_type, pay):
        self.from_city = from_city
        self.to_city = to_city
        self.transport_type = transport_type
        self.pay = pay

class JobScreen(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lalamove Driver - Jobs")
        self.geometry("360x780")
        self.resizable(False, False)

        self.cities = ["City 1", "City 2", "City 3", "City 4", "City 5"]
        self.transport_type = "Van"

        self.on_duty = False
        self.current_job = None
        self.job_timer_id = None

        # Duty toggle button
        self.duty_btn = tk.Button(self, text="Off Duty", bg="gray", fg="white",
                                  font=("Arial", 14, "bold"), command=self.toggle_duty)
        self.duty_btn.place(x=10, y=10, width=100, height=40)

        # Job display box frame (orange border)
        self.job_frame = tk.Frame(self, highlightbackground="#FF6600", highlightthickness=3, bd=0)
        self.job_frame.place(x=20, y=70, width=320, height=220)

        # Job info labels
        self.job_from_label = tk.Label(self.job_frame, text="", font=("Arial", 16, "bold"))
        self.job_from_label.pack(pady=(15, 0))

        self.job_to_label = tk.Label(self.job_frame, text="", font=("Arial", 16, "bold"))
        self.job_to_label.pack(pady=(5, 10))

        self.transport_label = tk.Label(self.job_frame, text="", font=("Arial", 14))
        self.transport_label.pack()

        self.pay_label = tk.Label(self.job_frame, text="", font=("Arial", 14, "bold"), fg="#FF6600")
        self.pay_label.pack(pady=(10, 15))

        # Accept and Decline buttons
        btn_frame = tk.Frame(self.job_frame)
        btn_frame.pack(pady=(5, 10))

        self.accept_btn = tk.Button(btn_frame, text="Accept", bg="#28a745", fg="white",
                                    font=("Arial", 14, "bold"), width=10, command=self.accept_job)
        self.accept_btn.pack(side="left", padx=10)

        self.decline_btn = tk.Button(btn_frame, text="Decline", bg="#dc3545", fg="white",
                                     font=("Arial", 14, "bold"), width=10, command=self.decline_job)
        self.decline_btn.pack(side="right", padx=10)

        # Initially disable buttons and clear job info
        self.clear_job()

    def toggle_duty(self):
        self.on_duty = not self.on_duty
        if self.on_duty:
            self.duty_btn.config(text="On Duty", bg="#FF6600")
            self.start_job_cycle()
        else:
            self.duty_btn.config(text="Off Duty", bg="gray")
            self.stop_job_cycle()
            self.clear_job()

    def start_job_cycle(self):
        if not self.on_duty:
            return
        if self.current_job is None:
            self.current_job = self.generate_random_job()
            self.show_job(self.current_job)
            # Enable buttons
            self.accept_btn.config(state="normal")
            self.decline_btn.config(state="normal")

    def stop_job_cycle(self):
        if self.job_timer_id:
            self.after_cancel(self.job_timer_id)
            self.job_timer_id = None
        self.current_job = None
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

    def generate_random_job(self):
        from_city = random.choice(self.cities)
        to_city = random.choice(self.cities)
        while to_city == from_city:
            to_city = random.choice(self.cities)
        pay = random.uniform(8, 30)
        pay = f"SGD ${pay:.2f}"
        return Job(from_city, to_city, self.transport_type, pay)

    def show_job(self, job):
        self.job_from_label.config(text=f"From: {job.from_city}")
        self.job_to_label.config(text=f"To: {job.to_city}")
        self.transport_label.config(text=f"Transport: {job.transport_type}")
        self.pay_label.config(text=f"Pay: {job.pay}")

    def clear_job(self):
        self.job_from_label.config(text="")
        self.job_to_label.config(text="")
        self.transport_label.config(text="")
        self.pay_label.config(text="")
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

    def accept_job(self):
        messagebox.showinfo("Accepted", "Job accepted! (To be implemented)")
        # After accept, stop job cycle and clear current job
        self.stop_job_cycle()
        self.clear_job()
        # TODO: implement next screen here

    def decline_job(self):
        # Disable buttons immediately to prevent multiple clicks
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

        # Clear current job from display
        self.clear_job()
        self.current_job = None

        # Wait 15-30 seconds, then show a new job if still on duty
        if self.on_duty:
            wait_time = random.randint(15, 30) * 1000
            self.job_timer_id = self.after(wait_time, self.start_job_cycle)

class LalamoveDriverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lalamove Driver App")
        self.geometry("360x780")
        self.resizable(False, False)

        # Mobile Number Label and Entry
        tk.Label(self, text="Mobile Number", font=("Arial", 14)).pack(pady=(100,5))
        self.mobile_entry = tk.Entry(self, font=("Arial", 16))
        self.mobile_entry.pack(ipadx=50, ipady=8, pady=(0,20))

        # Password Label and Entry
        tk.Label(self, text="Password", font=("Arial", 14)).pack(pady=(0,5))
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.pack(ipadx=50, ipady=8, pady=(0,40))

        # Orange Login Button
        self.login_button = tk.Button(self, text="LOGIN", bg="#FF6600", fg="white",
                                      font=("Arial", 18, "bold"), command=self.login)
        self.login_button.pack(side="bottom", fill="x", ipady=15)

    def login(self):
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()

        if mobile == "1" and password == "1":
            self.open_job_screen()
        else:
            messagebox.showerror("Error", "Invalid mobile number or password.")

    def open_job_screen(self):
        self.withdraw()
        job_screen = JobScreen(self)
        job_screen.mainloop()

if __name__ == "__main__":
    app = LalamoveDriverApp()
    app.mainloop()
