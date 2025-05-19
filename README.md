# ✈️ Flight Booking System – Project Report (KahaUdoge)

---

## 📌 1. Project Title

**KahaUdoge – A GUI-Based Flight Booking System**

---

## 🧠 2. Objective

To develop a user-friendly desktop application for booking flights using Python (Tkinter) for the front end and MySQL for the backend. The system enables users to book, view, and manage flight tickets efficiently.

---

## ⚙️ 3. Technology Stack

| Component       | Technology Used          |
|----------------|--------------------------|
| Frontend        | Python (Tkinter)         |
| Backend         | Python                   |
| Database        | MySQL                    |
| Libraries Used  | mysql-connector-python, tkinter, re |

---


## 🧰 5. Key Features

- **Home Page**: Branding and popular flight routes.
- **Flight Booking**: Form with validation for user input.
- **View Flights**: Display of available flights from database.
- **Ticket Status**: Update, cancel, or confirm bookings.
- **History**: Shows booking and cancellation records.
- **Validation**: Email and phone number pattern validation.

---

## 🛠️ 6. Functional Modules

### a. Home Tab
- Branding and intro.

### b. Flights Tab
- Displays available flights with origin, destination, times, and price.

### c. Booking Tab
- Fields: Full Name, DOB, Passport No, Gender, Email, Phone
- Button: **Book Flight**
- Status: Defaults to **Pending**

### d. View Tickets
- Shows user's booked tickets.
- Options to change status to Confirmed/Canceled.

### e. Booking History
- Displays complete history of user actions.

---

## 🧪 7. Validation Logic

- **Email**: Must match regex pattern for valid format.
- **Phone**: Exactly 10 digits, only numbers allowed.

---

## 🔗 8. Database Structure

### Database Name: `flight_booking_system6`

#### Table: `flights`
| Column Name     | Type    | Description                |
|-----------------|---------|----------------------------|
| flight_id       | INT     | Primary Key (Auto)         |
| flight_number   | VARCHAR | Unique Flight Number       |
| origin          | VARCHAR | Departure City             |
| destination     | VARCHAR | Arrival City               |
| departure_time  | VARCHAR | Flight Departure Time      |
| arrival_time    | VARCHAR | Flight Arrival Time        |
| seats_available | INT     | Number of seats left       |
| price           | DECIMAL | Ticket price               |

#### Table: `bookings`
| Column Name      | Type    | Description                          |
|------------------|---------|--------------------------------------|
| booking_id       | INT     | Primary Key (Auto)                   |
| flight_id        | INT     | Foreign Key from `flights` table     |
| full_name        | VARCHAR | User's Full Name                     |
| dob              | VARCHAR | Date of Birth                        |
| passport_number  | VARCHAR | Passport / Govt ID                   |
| gender           | VARCHAR | Gender                               |
| email            | VARCHAR | Email Address                        |
| phone            | VARCHAR | Contact Number                       |
| status           | VARCHAR | Booking status (Pending/Confirmed)   |

---

## 📷 9. Screenshots (To be added)

- Home Page UI
- Flight Booking Form
- Ticket Viewing Interface
- Booking History Page

---

## 🚀 10. Future Enhancements

- Add login/signup for users and admin
- Add flight filters (by date, destination)
- Integrate payment gateway (mock)
- Date picker for DOB and travel date
- PDF ticket generation

---

## 👨‍💻 11. Author

**Lakshay Parashar**  
B.Tech CSE, Amity University Noida (2022–2026)

GitHub: [github.com/lakshayparashar](https://github.com/lakshayparashar28)  
LinkedIn: [linkedin.com/in/lakshayparashar](https://www.linkedin.com/in/lakshay-parashar-029568232?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---
