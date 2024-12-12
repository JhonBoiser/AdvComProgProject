import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import mysql.connector
from mysql.connector import Error


class SalonSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Salon and Spa Management System")

        # Set the window size instead of full screen
        self.root.geometry("800x600") # Window size is set to 800x600
        self.root.config(bg="#f4f4f4")

        # Center the window on the screen
        self.center_window(800, 600)

        # Bind the close event to a custom method
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Database connection
        self.create_database()

        # Predefined Services with Specific Options
        self.services = {
            "Haircut": [("Standard", 100.00), ("Premium", 200.00), ("Deluxe", 300.00)],
            "Manicure": [("Basic", 250.00), ("Gel Polish", 300.00)],
            "Body Massage": [("Relaxation", 400.00), ("Therapeutic", 500.00)]
        }

        self.login_screen(self)

    def center_window(self, width, height):
        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center the window
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)

        # Set the window position
        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def create_database(self):
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='')
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS salon_spa")
            conn.database = 'salon_spa'

            # Create Admins Table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Admins (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )''')

            # Insert default admin if not already there
            cursor.execute("SELECT * FROM Admins WHERE username = 'admin'")
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO Admins (username, password) VALUES ('admin', 'admin123')")

            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def login_screen(self, root):
        self.clear_screen()
        self.root.geometry("400x400")
        self.center_window(400, 400)

        login_frame = tk.Frame(self.root, bg="#801650")
        login_frame.pack(fill="both", expand=True)

        tk.Label(login_frame, text="ADMIN", font=("Verdana", 24, "bold"),fg="white", bg="#801650").pack(pady=30)

        # Username and Password Fields
        tk.Label(login_frame, text="Username:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=30, pady=5)
        username_entry = tk.Entry(login_frame, font=("Arial", 12))
        username_entry.pack(fill="x", padx=30)

        tk.Label(login_frame, text="Password:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=30, pady=5)
        password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
        password_entry.pack(fill="x", padx=30)

        # Show password checkbox
        def toggle_password():
            if password_entry.cget('show') == "*":
                password_entry.config(show="")
                show_password_var.set(True)
            else:
                password_entry.config(show="*")
                show_password_var.set(False)

        show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(login_frame, text="Show Password", variable=show_password_var, fg="white", bg="#801650", command=toggle_password,pady=5)
        show_password_check.pack(anchor="w", padx=30)

        # Reset Button
        def reset_fields():
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

        reset_button = tk.Button(login_frame, text="Reset", width=30,command=reset_fields, font=("Arial", 14), bg="#FFC107", fg="white")
        reset_button.pack(pady=10)

        # Login Button
        login_button = tk.Button(login_frame, text="Login", width=30,command=lambda: self.check_credentials(
            username_entry.get(), password_entry.get()), font=("Arial", 14), bg="#007BFF", fg="white")
        login_button.pack(pady=20)

    def check_credentials(self, username, password):
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='salon_spa')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Admins WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                # If login successful, show the main menu
                self.setup_main_menu(self)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
            
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def setup_main_menu(self,root):
        # Clear current screen (if any)
        self.clear_screen()
        self.root.geometry("1000x500")
        self.center_window(1000, 500)
        tk.Label(self.root, text="Salon and Spa Management System", font=("Verdana", 24, "bold"), fg="white",bg="#801650").pack(pady=20)
        
        btn_frame = tk.Frame(self.root, bg="#801650")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Add Client & Appointment", command=self.add_client_screen,
                  font=("Arial", 14), width=25, bg="#007BFF", fg="white").grid(row=0, column=0, padx=10, pady=10)

        tk.Button(btn_frame, text="View Appointments", command=self.view_appointments_screen,
                  font=("Arial", 14), width=25, bg="#28A745", fg="white").grid(row=0, column=1, padx=10, pady=10)

        tk.Button(btn_frame, text="View Client History", command=self.view_client_history_screen,
                  font=("Arial", 14), width=25, bg="#FFC107", fg="white").grid(row=1, column=0, padx=10, pady=10)

        tk.Button(btn_frame, text="Exit", command=self.root.quit,
                  font=("Arial", 14), width=25, bg="#DC3545", fg="white").grid(row=1, column=1, padx=10, pady=10)

    def add_client_screen(self):
        self.clear_screen()
        add_window = tk.Frame(self.root, bg="#801650")
        add_window.pack(fill="both", expand=True)

        tk.Label(add_window, text="Add Client & Appointment", font=("Arial", 18, "bold"),fg="white", bg="#801650").pack(pady=10)

        # Client Details
        tk.Label(add_window, text="Client Name:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=20, pady=5)
        name_entry = tk.Entry(add_window, font=("Arial", 12))
        name_entry.pack(fill="x", padx=20)

        tk.Label(add_window, text="Phone:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=20, pady=5)
        phone_entry = tk.Entry(add_window, font=("Arial", 12))
        phone_entry.pack(fill="x", padx=20)

        tk.Label(add_window, text="Email:", font=("Arial", 12), fg="white", bg="#801650").pack(anchor="w", padx=20, pady=5)
        email_entry = tk.Entry(add_window, font=("Arial", 12))
        email_entry.pack(fill="x", padx=20)

        tk.Label(add_window, text="Address:", font=("Arial", 12), fg="white", bg="#801650").pack(anchor="w", padx=20, pady=5)
        address_entry = tk.Entry(add_window, font=("Arial", 12))
        address_entry.pack(fill="x", padx=20)

        # Service Selection
        tk.Label(add_window, text="Choose Service:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=20, pady=5)
        service_var = tk.StringVar(value="Haircut")
        service_dropdown = ttk.Combobox(add_window, textvariable=service_var, state="readonly",
                                          values=list(self.services.keys()), font=("Arial", 12))
        service_dropdown.pack(fill="x", padx=20)

        tk.Label(add_window, text="Choose Specific Service:", font=("Arial", 12),fg="white",  bg="#801650").pack(anchor="w", padx=20, pady=5)
        specific_service_var = tk.StringVar()
        specific_service_dropdown = ttk.Combobox(add_window, textvariable=specific_service_var, state="readonly",
                                                  font=("Arial", 12))
        specific_service_dropdown.pack(fill="x", padx=20)

        def update_specific_services(event):
            service = service_var.get()
            specific_services = [f"{s[0]} (₱{s[1]:.2f})" for s in self.services[service]]
            specific_service_dropdown.config(values=specific_services)
            specific_service_var.set(specific_services[0])

        service_dropdown.bind("<<ComboboxSelected>>", update_specific_services)
        update_specific_services(None)

        # Appointment Date
        tk.Label(add_window, text="Appointment Date:", font=("Arial", 12),fg="white", bg="#801650").pack(anchor="w", padx=20, pady=5)
        calendar = Calendar(add_window, date_pattern="yyyy-mm-dd")
        calendar.pack(pady=10)

        # Submit Button (moved to the right side of the calendar)
        submit_button_frame = tk.Frame(add_window, bg="#801650")
        submit_button_frame.pack(fill="x", padx=20, pady=10)

        # Submit Button
        submit_button = tk.Button(submit_button_frame, text="Submit", command=lambda: self.add_client(
            name_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            address_entry.get(),
            specific_service_var.get(),
            calendar.get_date()
        ), font=("Arial", 14), bg="#007BFF", fg="white")
        submit_button.pack(side="right")

        # Back Button beside Submit Button
        back_button = tk.Button(submit_button_frame, text="Back", command=lambda:self.setup_main_menu(self),
                                font=("Arial", 14), bg="#DC3545", fg="white")
        back_button.pack(side="left", padx=10)

    def add_client(self, name, phone, email, address, service_name, appointment_date):
        if not all([name, phone, email, address, service_name, appointment_date]):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            # Parse the service name and extract payment
            service_desc, payment_str = service_name.split(" (₱")
            payment = float(payment_str[:-1])

            conn = mysql.connector.connect(host='localhost', user='root', password='', database='salon_spa')
            cursor = conn.cursor()

            # Insert Client
            cursor.execute('INSERT INTO Clients (name, phone, email, address) VALUES (%s, %s, %s, %s)',
                           (name, phone, email, address))
            client_id = cursor.lastrowid

            # Insert Appointment
            cursor.execute('INSERT INTO Appointments (client_id, service_name, appointment_date, payment) VALUES (%s, %s, %s, %s)',
                           (client_id, service_desc, appointment_date, payment))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Client and Appointment added successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def view_appointments_screen(self):
        self.clear_screen()
        view_window = tk.Frame(self.root, bg="#801650")
        view_window.pack(fill="both", expand=True)

        tk.Label(view_window, text="All Appointments", font=("Arial", 20, "bold"),fg="white", bg="#801650").pack(pady=10)

        # Create a Treeview widget to display the appointments
        columns = ("Appointment ID", "Client Name", "Service", "Date", "Payment")
        treeview = ttk.Treeview(view_window, columns=columns, show="headings")
        treeview.pack(fill="both", expand=True, padx=20, pady=10)

        # Define column headings
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center")

        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='salon_spa')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.appointment_id, c.name, a.service_name, a.appointment_date, a.payment
                FROM Appointments a
                JOIN Clients c ON a.client_id = c.client_id
            ''')
            rows = cursor.fetchall()
            for row in rows:
                treeview.insert("", "end", values=row)

            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

        # Back Button
        back_button = tk.Button(view_window, text="Back", command=lambda:self.setup_main_menu(self),
                                font=("Arial", 14), bg="#DC3545", fg="white")
        back_button.pack(pady=10)

    def view_client_history_screen(self):
        self.clear_screen()
        history_window = tk.Frame(self.root, bg="#801650")
        history_window.pack(fill="both", expand=True)

        tk.Label(history_window, text="Client Appointment History", font=("Verdana", 20, "bold"), fg="white", bg="#801650").pack(pady=10)

        # Create a Treeview widget to display all client histories
        columns = ("Client Name", "Appointment ID", "Service", "Date", "Payment")
        treeview = ttk.Treeview(history_window, columns=columns, show="headings")
        treeview.pack(fill="both", expand=True, padx=20, pady=10)

        # Define column headings
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center")
            
        
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='salon_spa')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.appointment_id, c.name, a.service_name, a.appointment_date, a.payment
                FROM Appointments a
                JOIN Clients c ON a.client_id = c.client_id
            ''')
            rows = cursor.fetchall()
            for row in rows:
                treeview.insert("", "end", values=row)

            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

        # Back Button
        back_button = tk.Button(history_window, text="Back", command=lambda:self.setup_main_menu(self),
                                font=("Arial", 14), bg="#DC3545", fg="white")
        back_button.pack(pady=10)    
            
       

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_close(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SalonSystem(root)
    root.mainloop()
