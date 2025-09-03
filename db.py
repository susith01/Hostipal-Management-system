import sqlite3
from datetime import datetime

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    # Patients Table
    cur.execute("""CREATE TABLE IF NOT EXISTS patients(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    contact TEXT)""")

    # Doctors Table
    cur.execute("""CREATE TABLE IF NOT EXISTS doctors(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    specialization TEXT,
                    contact TEXT)""")

    # Appointments Table
    cur.execute("""CREATE TABLE IF NOT EXISTS appointments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    doctor_id INTEGER,
                    date TEXT,
                    time TEXT,
                    status TEXT,
                    FOREIGN KEY(patient_id) REFERENCES patients(id),
                    FOREIGN KEY(doctor_id) REFERENCES doctors(id))""")

    # Billing Table
    cur.execute("""CREATE TABLE IF NOT EXISTS billing(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    total_amount REAL,
                    paid_status TEXT,
                    date TEXT,
                    FOREIGN KEY(patient_id) REFERENCES patients(id))""")

    conn.commit()
    conn.close()

# ---------------- Patients ----------------
def add_patient():
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    contact = input("Enter contact number: ")

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO patients(name, age, gender, contact) VALUES(?,?,?,?)",
                (name, age, gender, contact))
    conn.commit()
    conn.close()
    print("✅ Patient added successfully!\n")

def view_patients():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    print("\n--- Patients List ---")
    for row in rows:
        print(row)

# ---------------- Doctors ----------------
def add_doctor():
    name = input("Enter doctor name: ")
    specialization = input("Enter specialization: ")
    contact = input("Enter contact number: ")

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors(name, specialization, contact) VALUES(?,?,?)",
                (name, specialization, contact))
    conn.commit()
    conn.close()
    print("✅ Doctor added successfully!\n")

def view_doctors():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()
    conn.close()
    print("\n--- Doctors List ---")
    for row in rows:
        print(row)

# ---------------- Appointments ----------------
def add_appointment():
    view_patients()
    patient_id = int(input("Enter patient ID: "))
    view_doctors()
    doctor_id = int(input("Enter doctor ID: "))
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM): ")
    status = "Scheduled"

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO appointments(patient_id, doctor_id, date, time, status) VALUES(?,?,?,?,?)",
                (patient_id, doctor_id, date, time, status))
    conn.commit()
    conn.close()
    print("✅ Appointment booked successfully!\n")

def view_appointments():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("""SELECT a.id, p.name, d.name, a.date, a.time, a.status
                   FROM appointments a
                   JOIN patients p ON a.patient_id = p.id
                   JOIN doctors d ON a.doctor_id = d.id""")
    rows = cur.fetchall()
    conn.close()
    print("\n--- Appointments List ---")
    for row in rows:
        print(row)

# ---------------- Billing ----------------
def add_bill():
    view_patients()
    patient_id = int(input("Enter patient ID: "))
    total_amount = float(input("Enter total amount: "))
    paid_status = input("Paid status (Paid/Unpaid/Partial): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO billing(patient_id, total_amount, paid_status, date) VALUES(?,?,?,?)",
                (patient_id, total_amount, paid_status, date))
    conn.commit()
    conn.close()
    print("✅ Bill added successfully!\n")

def view_bills():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("""SELECT b.id, p.name, b.total_amount, b.paid_status, b.date
                   FROM billing b
                   JOIN patients p ON b.patient_id = p.id""")
    rows = cur.fetchall()
    conn.close()
    print("\n--- Billing List ---")
    for row in rows:
        print(row)

# ---------------- Main Menu ----------------
def menu():
    while True:
        print("\n🏥 Hospital Management System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Book Appointment")
        print("6. View Appointments")
        print("7. Add Bill")
        print("8. View Bills")
        print("9. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            add_doctor()
        elif choice == "4":
            view_doctors()
        elif choice == "5":
            add_appointment()
        elif choice == "6":
            view_appointments()
        elif choice == "7":
            add_bill()
        elif choice == "8":
            view_bills()
        elif choice == "9":
            print("👋 Exiting system...")
            break
        else:
            print("❌ Invalid choice, try again!")

# Run the program
if __name__ == "__main__":
    init_db()
    menu()
