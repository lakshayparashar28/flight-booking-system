import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import re

# MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="Lakshay@2004",  
    database="flight_booking_system6"
)
cursor = db_connection.cursor()

# Function to view available flights
def view_flights():
    cursor.execute("SELECT * FROM flights WHERE seats_available > 0")
    flights = cursor.fetchall()
    flight_tree.delete(*flight_tree.get_children())  # Clear existing data
    for flight in flights:
        flight_tree.insert("", "end", values=flight)

# Function to book a flight
def book_flight():
    selected_item = flight_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a flight to book.")
        return

    flight_details = flight_tree.item(selected_item, "values")
    flight_id = flight_details[0]  # flight_id
    full_name = full_name_entry.get()
    dob = dob_entry.get()
    passport_number = passport_entry.get()
    gender = gender_var.get()
    email = email_entry.get()
    phone = phone_entry.get()

    # Validate input fields
    if not full_name or not dob or not passport_number or not gender or not email or not phone:
        messagebox.showerror("Error", "All fields must be filled out.")
        return
    
    # Validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return
    
    # Validate phone number format (simple validation)
    phone_regex = r'^\+?[0-9]{10,15}$'
    if not re.match(phone_regex, phone):
        messagebox.showerror("Error", "Please enter a valid phone number.")
        return

    try:
        cursor.execute(''' 
            INSERT INTO bookings (flight_id, full_name, dob, passport_number, gender, email, phone, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Booked')
        ''', (flight_id, full_name, dob, passport_number, gender, email, phone))
        db_connection.commit()
        messagebox.showinfo("Success", "Flight booked successfully.")
    except Exception as e:
        db_connection.rollback()
        messagebox.showerror("Error", str(e))

# Function to view bookings
def view_bookings():
    cursor.execute('''
        SELECT b.booking_id, f.flight_number, f.origin, f.destination, f.departure_time, f.arrival_time, b.full_name, b.phone, b.email, b.status 
        FROM bookings b 
        JOIN flights f ON b.flight_id = f.flight_id 
        WHERE b.status = 'Booked'
    ''')
    bookings = cursor.fetchall()
    booking_tree.delete(*booking_tree.get_children())  # Clear existing data
    for booking in bookings:
        booking_tree.insert("", "end", values=booking)

# Function to view all history (booked and canceled bookings)
def view_history():
    cursor.execute('''
        SELECT b.booking_id, f.flight_number, f.origin, f.destination, f.departure_time, f.arrival_time, b.full_name, b.phone, b.email, b.status 
        FROM bookings b 
        JOIN flights f ON b.flight_id = f.flight_id
    ''')
    history = cursor.fetchall()
    history_tree.delete(*history_tree.get_children())  # Clear existing data
    for record in history:
        history_tree.insert("", "end", values=record)

# Function to cancel a booking
def cancel_booking():
    selected_item = booking_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a booking to cancel.")
        return

    booking_id = booking_tree.item(selected_item, "values")[0]  # booking_id
    try:
        cursor.execute("UPDATE bookings SET status = 'Canceled' WHERE booking_id = %s", (booking_id,))
        db_connection.commit()
        messagebox.showinfo("Success", "Booking canceled successfully.")
        view_bookings()  # Refresh the bookings
        view_history()   # Refresh the history
    except Exception as e:
        db_connection.rollback()
        messagebox.showerror("Error", str(e))

# Function to update booking status
def update_booking_status():
    selected_item = booking_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a booking to update.")
        return

    booking_id = booking_tree.item(selected_item, "values")[0]  # booking_id
    new_status = status_var.get()

    if not new_status:
        messagebox.showerror("Error", "Please select a new status.")
        return

    try:
        cursor.execute("UPDATE bookings SET status = %s WHERE booking_id = %s", (new_status, booking_id))
        db_connection.commit()
        messagebox.showinfo("Success", "Booking status updated successfully.")
        view_bookings()  # Refresh the bookings
        view_history()   # Refresh the history
    except Exception as e:
        db_connection.rollback()
        messagebox.showerror("Error", str(e))

# Function to create the home tab content
def create_home_tab():
    home_label = tk.Label(
        home_tab, 
        text="Welcome to KahaUdoge - Your Gateway to the World", 
        font=("Arial", 28, "bold"), 
        bg="navy", fg="white", 
        padx=10, pady=20
    )
    home_label.pack(pady=10, fill='x')

    discount_frame = tk.Frame(home_tab, bg="#FFD700", pady=10)
    discount_frame.pack(fill='x', padx=5, pady=5)
    
    discount_label = tk.Label(
        discount_frame, 
        text="🌍 Special Offer: 20% OFF on all international flights! ✈️ Book Now and Save Big! 🏷️",
        font=("Arial", 18, "bold"),
        fg="darkred", bg="#FFD700"
    )
    discount_label.pack(pady=5)

    info_label = tk.Label(
        home_tab, 
        text="Why Book with Us?", 
        font=("Arial", 24, "bold"), 
        fg="darkblue"
    )
    info_label.pack(pady=20)
    
    info_text = """✈️ Wide range of domestic and international flights.
💼 Seamless booking process with secure payments.
💲 Exclusive deals and discounts for frequent flyers.
📅 Flexible travel dates and easy rescheduling.
👩‍💼 24/7 customer support to assist you with any queries.
🧳 Travel insurance and special baggage allowance options."""
    info_content = tk.Label(
        home_tab, 
        text=info_text, 
        font=("Arial", 14), 
        justify="left", 
        padx=20
    )
    info_content.pack(pady=10)

    recommended_label = tk.Label(home_tab, text="Recommended Flights for You", font=("Arial", 20, "bold"), pady=10)
    recommended_label.pack()

    recommended_tree = ttk.Treeview(home_tab, columns=("Flight ID", "Flight Number", "Origin", "Destination", "Departure", "Arrival", "Price"), show="headings")
    recommended_tree.pack(fill="x")
    for col in recommended_tree["columns"]:
        recommended_tree.heading(col, text=col)

    cursor.execute("SELECT * FROM flights WHERE seats_available > 0 LIMIT 5")
    recommended_flights = cursor.fetchall()
    for flight in recommended_flights:
        recommended_tree.insert("", "end", values=flight)

# Create the main application window
root = tk.Tk()
root.title("KahaUdoge")
root.geometry("1000x700")

# Create tabs
tab_control = ttk.Notebook(root)

# Home tab
home_tab = tk.Frame(tab_control, bg="white")
tab_control.add(home_tab, text="Home")
create_home_tab()

# Flight booking tab
flight_booking_tab = tk.Frame(tab_control)
tab_control.add(flight_booking_tab, text="Flight Booking")

# View bookings tab
view_booking_tab = tk.Frame(tab_control)
tab_control.add(view_booking_tab, text="View Tickets")

# History tab
history_tab = tk.Frame(tab_control)
tab_control.add(history_tab, text="History")

# Add tabs to the main window
tab_control.pack(expand=1, fill="both")

# Flight Booking Tab - View Flights
flight_label = tk.Label(flight_booking_tab, text="Available Flights", font=("Arial", 16, "bold"))
flight_label.pack(pady=10)

flight_tree = ttk.Treeview(flight_booking_tab, columns=("Flight ID", "Flight Number", "Origin", "Destination", "Departure", "Arrival", "Seats", "Price"), show="headings")
flight_tree.pack(fill="x")
for col in flight_tree["columns"]:
    flight_tree.heading(col, text=col)

view_flights_button = tk.Button(flight_booking_tab, text="View Flights", command=view_flights, bg="#4CAF50", fg="white", font=("Arial", 12))
view_flights_button.pack(pady=10)

# Flight Booking Tab - Booking Form
booking_form_label = tk.Label(flight_booking_tab, text="Book Your Flight", font=("Arial", 16, "bold"))
booking_form_label.pack(pady=10)

form_frame = tk.Frame(flight_booking_tab)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
full_name_entry = tk.Entry(form_frame)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)

dob_label = tk.Label(form_frame, text="Date of Birth (YYYY/MM/DD):")
dob_label.grid(row=1, column=0, padx=5, pady=5)
dob_entry = tk.Entry(form_frame)
dob_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
gender_var = tk.StringVar()
gender_options = ["Male", "Female", "Other"]
gender_menu = ttk.OptionMenu(form_frame, gender_var, gender_options[0], *gender_options)
gender_menu.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Passport Number:").grid(row=3, column=0, padx=5, pady=5)
passport_entry = tk.Entry(form_frame)
passport_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Email:").grid(row=4, column=0, padx=5, pady=5)
email_entry = tk.Entry(form_frame)
email_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Phone:").grid(row=5, column=0, padx=5, pady=5)
phone_entry = tk.Entry(form_frame)
phone_entry.grid(row=5, column=1, padx=5, pady=5)

book_button = tk.Button(flight_booking_tab, text="Book Flight", command=book_flight, bg="#FF9800", fg="white", font=("Arial", 12))
book_button.pack(pady=10)

# View Bookings Tab
booking_label = tk.Label(view_booking_tab, text="Your Bookings", font=("Arial", 16, "bold"))
booking_label.pack(pady=10)

booking_tree = ttk.Treeview(view_booking_tab, columns=("Booking ID", "Flight Number", "Origin", "Destination", "Departure", "Arrival", "Full Name", "Phone", "Email", "Status"), show="headings")
for col in booking_tree["columns"]:
    booking_tree.heading(col, text=col)
booking_tree.pack(fill="x")

# View Bookings Button
view_bookings_button = tk.Button(view_booking_tab, text="View Bookings", command=view_bookings, bg="#4CAF50", fg="white", font=("Arial", 12))
view_bookings_button.pack(pady=10)

# Cancel Booking Button
cancel_booking_button = tk.Button(view_booking_tab, text="Cancel Booking", command=cancel_booking, bg="red", fg="white", font=("Arial", 12))
cancel_booking_button.pack(pady=10)

# Status Update Section
status_label = tk.Label(view_booking_tab, text="Update Booking Status", font=("Arial", 14, "bold"))
status_label.pack(pady=10)

status_var = tk.StringVar()
status_options = ["Pending", "Confirmed", "Canceled"]
status_menu = ttk.OptionMenu(view_booking_tab, status_var, status_options[0], *status_options)
status_menu.pack(pady=5)

update_status_button = tk.Button(view_booking_tab, text="Update Status", command=update_booking_status, bg="#FF9800", fg="white", font=("Arial", 12))
update_status_button.pack(pady=10)

# History Tab
history_label = tk.Label(history_tab, text="Booking History", font=("Arial", 16, "bold"))
history_label.pack(pady=10)

history_tree = ttk.Treeview(history_tab, columns=("Booking ID", "Flight Number", "Origin", "Destination", "Departure", "Arrival", "Full Name", "Phone", "Email", "Status"), show="headings")
for col in history_tree["columns"]:
    history_tree.heading(col, text=col)
history_tree.pack(fill="x")

view_history_button = tk.Button(history_tab, text="View History", command=view_history, bg="#4CAF50", fg="white", font=("Arial", 12))
view_history_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
