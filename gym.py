'''
1 Problem Statement
Design and implement an application for a Health and Fitness Club Management System. This system will serve
as a comprehensive platform catering to the diverse needs of club members, trainers, and administrative staff.
Members should be able to register and manage their profiles, establish personal fitness goals (you can
determine suitable fitness goals such as weight and time, and members will set the values), and input health
metrics. They should have access to a personalized dashboard that tracks exercise routines, fitness achievements,
and health statistics. Members can schedule, reschedule, or cancel personal training sessions with certified
trainers. Additionally, they should be able to register for group fitness classes.
Trainers should have the ability to manage their schedules and view member profiles.
Administrative Staff should be equipped with features to manage room bookings, monitor fitness equipment
maintenance, update class schedules, oversee billing, and process payments for membership fees, personal
training sessions, and other services.
Functions to Implement:
Member Functions:
1. User Registration
2. Profile Management (Updating personal information, fitness goals, health metrics)
3. Dashboard Display (Displaying exercise routines, fitness achievements, health statistics)
4. Schedule Management (Scheduling personal training sessions or group fitness classes. The system
must ensure that the trainer is available)
Trainer Functions:
1. Schedule Management (Trainer can set the time for which they are available.)
2. Member Profile Viewing (Search by Member’s name)
Administrative Staff Functions:
1. Room Booking Management
2. Equipment Maintenance Monitoring
3. Class Schedule Updating
4. Billing and Payment Processing (Your system should assume integration with a payment service
[Note: Do not actually integrate with a payment service])
You are not required to demonstrate the entire sequence of operations, but rather focus on individual operations.
For instance, when a new member joins, the subsequent step involves scheduling a session. Following that, the
system generates a bill, the member makes a payment, and then the system confirms the transaction. I do not
anticipate you to follow this sequence explicitly. Instead, I only need you to provide an operation (function) in
your code along with its corresponding SQL code. You are encouraged to test these functions separately in your
demo video.

CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    certification VARCHAR(255)
    
);
TrainerAvailability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INT,
    pricing DECIMAL(10, 2),
    date_time TIMESTAMP,
    duration INTERVAL,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
);

CREATE TABLE PersonalTrainingSession (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT,
    member_id INT,
    date DATE,
    time TIME,
    duration INTERVAL,
    pricing DECIMAL(10, 2),
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id),
);

CREATE TABLE GroupFitnessClass (
    class_id SERIAL PRIMARY KEY,
    trainer_id INT,
    date DATE,
    time TIME,
    duration INTERVAL,
    pricing DECIMAL(10, 2),
    max_capacity INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
);
CREATE TABLE REGISTRATION (
    registration_id SERIAL PRIMARY KEY,
    class_id INT,
    member_id INT,
    date DATE,
    time TIME,
    FOREIGN KEY (class_id) REFERENCES GroupFitnessClass(class_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

CREATE TABLE RoomBooking (
    booking_id SERIAL PRIMARY KEY,
    room_number VARCHAR(50),
    date DATE,
    time TIME,
    duration INTERVAL
);

CREATE TABLE Fitness (
    fitness_id SERIAL PRIMARY KEY,
    member_id INT,
    weight DECIMAL(10, 2),
    time TIME,
    health_metrics VARCHAR(255),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    status VARCHAR(50)
);

CREATE TABLE Billing (
    bill_id SERIAL PRIMARY KEY,
    member_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

CREATE TABLE Payment (
    payment_id SERIAL PRIMARY KEY,
    bill_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    FOREIGN KEY (bill_id) REFERENCES Billing(bill_id)
    status VARCHAR(50)
);
CREATE TABLE ExerciseRoutines (
    routine_id SERIAL PRIMARY KEY,
    member_id INT,
    exercise_name VARCHAR(255),
    sets INT,
    reps INT,
    weight DECIMAL(10, 2),
    duration INTERVAL,
    date DATE,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);
create Table Admin (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

select * from member;
'''


import psycopg2
import datetime

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="fast",
    port="5432"
)


def fitness_table(member_id):
    print("let's record your Fitness Metrics now😀")
    weight = input("Enter your weight in kg: ")
    while True:
        time_input = input("Enter your time now (HH:MM:SS): ")
        try:
            valid_time = datetime.datetime.strptime(time_input, "%H:%M:%S").time()
            break
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS format.")
    
    health_metrics = input("Enter your heart rate per mins (normally 60-100, health metrics): ")
    cur = conn.cursor()
    cur.execute("INSERT INTO Fitness (member_id, weight, time, health_metrics) VALUES (%s, %s, %s, %s)", (member_id, weight, valid_time, health_metrics))
    conn.commit()
    cur.close()  

def exercise_routines(member_id):
    print("let's record your goal and Exercise Routines😀")
    exercise_name = input("Enter your exercise name for your fitness goal: ")
    reps = input("Enter your reps: ")
    sets = input("Enter your sets: ")   
    weight = input("Enter your ideal weight in kg: ")
    duration = input("Enter your today's plan duration (HH:MM:SS): ")
    cur = conn.cursor()
    cur.execute("INSERT INTO ExerciseRoutines (member_id, exercise_name, sets, reps, weight, duration, date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (member_id, exercise_name, sets, reps, weight, duration, datetime.date.today()))
    conn.commit()
    cur.close()
    

# Function for user registration
def register_user():
    print("User Registration")
    while True:
        try:
            # Collect user details
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            # Insert user details into the database
            cur = conn.cursor()
            cur.execute("INSERT INTO Member (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            print("User registered successfully! enjoy your work out💪!")
            cur.execute("SELECT member_id FROM Member WHERE email = %s", (email,))
            member_id = cur.fetchone()[0]
            cur.close()
            fitness_table(member_id)
            exercise_routines(member_id)
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to register user. Please try again.")

def login_user():
    print("User Login")
    while True:
        try:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            cur = conn.cursor()
            cur.execute("SELECT member_id FROM Member WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            if user:
                print("User login successful!")
                return user[0]
            else:
                print("User login failed. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to login user. Please try again.")
        finally:
            cur.close()

# Function for profile management
def manage_profile(user_id):
    print("Profile Management")
    new_email = input("Enter your new email (leave blank to skip): ")
    new_password = input("Enter your new password (leave blank to skip): ")
    try:
        # Update user details in the database
        cur = conn.cursor()
        if new_email:
            cur.execute("UPDATE Member SET email = %s WHERE member_id = %s", (new_email, user_id))
        if new_password:
            cur.execute("UPDATE Member SET password = %s WHERE member_id = %s", (new_password, user_id))
        conn.commit()
        print("Profile updated successfully!")
        cur.close()
        fitness_table(user_id)
        exercise_routines(user_id)
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update profile. Please try again.")

# Function for dashboard display


def display_dashboard(member_id):
    print("Dashboard Display")
    try:
        with conn.cursor() as cur:
            # Fetch the latest member's information
            cur.execute("SELECT * FROM Member WHERE member_id = %s", (member_id,))
            member_info = cur.fetchone()
            if member_info:
                print("Member Information:")
                print("Member ID:", member_info[0])
                print("Name:", member_info[1])
                print("Email:", member_info[2])
                print("\n")

            # Fetch the latest fitness metrics
            cur.execute("SELECT * FROM Fitness WHERE member_id = %s ORDER BY time DESC LIMIT 1", (member_id,))
            fitness_metrics = cur.fetchone()
            if fitness_metrics:
                print("Latest Fitness Metrics:")
                print("Weight:", fitness_metrics[2])
                print("Time:", fitness_metrics[3])
                print("Health Metrics:", fitness_metrics[4])
                print("\n")

            # Fetch the latest exercise routine
            cur.execute("SELECT * FROM ExerciseRoutines WHERE member_id = %s ORDER BY date DESC LIMIT 1", (member_id,))
            exercise_routine = cur.fetchone()
            if exercise_routine:
                print("Latest Exercise Routine:")
                print("Exercise Name:", exercise_routine[2])
                print("Sets:", exercise_routine[3])
                print("Reps:", exercise_routine[4])
                print("Weight:", exercise_routine[5])
                print("Duration:", exercise_routine[6])
                print("Date:", exercise_routine[7])
                print("\n")

            # Fetch the latest personal training session
            cur.execute("SELECT * FROM PersonalTrainingSession WHERE member_id = %s ORDER BY date DESC, time DESC LIMIT 1", (member_id,))
            personal_session = cur.fetchone()
            if personal_session:
                print("Latest Personal Training Session:")
                print("Trainer ID:", personal_session[1])
                print("Date:", personal_session[3])
                print("Time:", personal_session[4])
                print("Duration:", personal_session[5])
                print("Pricing:", personal_session[6])
                print("\n")

            # Fetch the latest registered group fitness class
            cur.execute("""
                SELECT g.* FROM GroupFitnessClass g
                JOIN Registration r ON g.class_id = r.class_id
                WHERE r.member_id = %s
                ORDER BY g.date DESC, g.time DESC LIMIT 1
            """, (member_id,))
            group_class = cur.fetchone()
            if group_class:
                print("Latest Registered Group Fitness Class:")
                print("Trainer ID:", group_class[1])
                print("Date:", group_class[2])
                print("Time:", group_class[3])
                print("Duration:", group_class[4])
                print("Pricing:", group_class[5])
                print("Max Capacity:", group_class[6])
                print("\n")

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving dashboard information:", error)
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to display dashboard.")

# Function for schedule management
def cancel_schedule(member_id):
    print("Cancel Schedule")
    with conn.cursor() as cur:
        # Retrieve personal training sessions
        cur.execute("SELECT session_id, date, time FROM PersonalTrainingSession WHERE member_id = %s", (member_id,))
        personal_sessions = cur.fetchall()
        print("Personal Training Sessions:")
        for session in personal_sessions:
            session_id, date, time = session
            print(f"Session ID: {session_id}, Date: {date}, Time: {time}")
        
        # Retrieve group fitness classes
        cur.execute("""
            SELECT GroupFitnessClass.class_id, GroupFitnessClass.date, GroupFitnessClass.time
            FROM Registration
            JOIN GroupFitnessClass ON Registration.class_id = GroupFitnessClass.class_id
            WHERE Registration.member_id = %s
        """, (member_id,))
        group_sessions = cur.fetchall()
        print("Group Fitness Classes:")
        for session in group_sessions:
            class_id, date, time = session
            print(f"Class ID: {class_id}, Date: {date}, Time: {time}")
    
        # Ask user which session to cancel
        session_type = input("Enter session type (personal training or group fitness): ")
        session_id = input("Enter session ID: ")

        # Delete session entry and corresponding billing
        if session_type == "personal training":
            cur.execute("DELETE FROM PersonalTrainingSession WHERE session_id = %s", (session_id,))
        elif session_type == "group fitness":
            cur.execute("DELETE FROM Registration WHERE class_id = %s", (session_id,))

        # Assuming billing records can be identified by member_id and session date
        cur.execute("SELECT bill_id FROM Billing WHERE member_id = %s AND date = %s", (member_id, date))
        bill_id_result = cur.fetchone()
        if bill_id_result:
            bill_id = bill_id_result[0]
            cur.execute("DELETE FROM Payment WHERE bill_id = %s", (bill_id,))
            cur.execute("DELETE FROM Billing WHERE bill_id = %s", (bill_id,))

        print("Schedule cancelled successfully!")
        
        conn.commit()
    
def add_or_cancel_schedule(member_id):
    print("Schedule Management")
    action = input("Enter action (add or cancel): ")
    if action == "add":
        manage_schedule(member_id)
        showbill(member_id)
    elif action == "cancel":
        cancel_schedule(member_id)
        showbill(member_id)
    else:
        print("Invalid action. Please try again.")
        
def personal_session(member_id):
    print("Available Personal Training Sessions")
    with conn.cursor() as cur:
        # Retrieve all future available personal training sessions
        cur.execute("""
            SELECT ta.availability_id, t.name, ta.date_time, ta.duration, ta.pricing
            FROM TrainerAvailability ta
            JOIN Trainer t ON ta.trainer_id = t.trainer_id
            WHERE ta.date_time > NOW() -- Assuming you want to show future sessions only
            ORDER BY ta.date_time
        """)
        available_sessions = cur.fetchall()

        if not available_sessions:
            print("No personal training sessions available.")
            return

        # Display available sessions to the user
        for session in available_sessions:
            print(f"Session ID: {session[0]}")
            print(f"Trainer Name: {session[1]}")
            print(f"Date and Time: {session[2]}")
            print(f"Duration: {session[3]}")
            print(f"Pricing: {session[4]}")
            print()

        # Ask user to choose a session
        chosen_session_id = input("Enter the session ID you wish to book: ")

        # Check if the chosen session ID is valid
        chosen_session = next((s for s in available_sessions if str(s[0]) == chosen_session_id), None)
        if not chosen_session:
            print("Invalid session ID.")
            return

        # Book the chosen personal training session
        try:
            cur.execute("""
                INSERT INTO PersonalTrainingSession (trainer_id, member_id, date, time, duration, pricing)
                SELECT trainer_id, %s, date_time::date, date_time::time, duration, pricing
                FROM TrainerAvailability
                WHERE availability_id = %s
            """, (member_id, chosen_session_id))

            # Calculate the amount for billing
            amount = chosen_session[4]

            # Insert billing information
            cur.execute("INSERT INTO Billing (member_id, amount, date) VALUES (%s, %s, CURRENT_DATE)", (member_id, amount))

            # Retrieve the bill_id of the inserted billing information
            cur.execute("SELECT bill_id FROM Billing WHERE member_id = %s ORDER BY bill_id DESC LIMIT 1", (member_id,))
            bill_id = cur.fetchone()[0]

            # Insert payment information
            cur.execute("INSERT INTO Payment (bill_id, amount, date, status) VALUES (%s, %s, CURRENT_DATE, 'Pending')", (bill_id, amount))

            # Commit the changes to the database
            conn.commit()
            print("Personal training session booked successfully!")

        except (Exception, psycopg2.Error) as error:
            conn.rollback()
            print("Error booking personal training session:", error)

    
def group_schedule(member_id):
        print("Group Fitness Sessions")
        cur = conn.cursor()

        # Retrieve available group fitness classes
        cur.execute("SELECT class_id, date, time,trainer_id FROM GroupFitnessClass WHERE max_capacity > 0")
        group_sessions = cur.fetchall()

        print("Available Group Fitness Classes:")
        for session in group_sessions:
            print("Class ID:", session[0])
            print("Trainer ID:", session[3])
            print("Date:", session[1])
            print("Time:", session[2])
            print("Price:", session[4])
            print()

        # Ask user to select a class
        class_id = input("Enter class ID: ")

        # Insert data into Registration table
        cur.execute("INSERT INTO Registration (class_id, member_id, date, time) VALUES (%s, %s, %s, %s)", (class_id, member_id, datetime.date.today(), datetime.datetime.now().time()))
        #

        # Decrement max capacity by 1 in GroupFitnessClass table
        cur.execute("UPDATE GroupFitnessClass SET max_capacity = max_capacity - 1 WHERE class_id = %s", (class_id,))
        # Calculate billing amount for the class
        cur.execute("SELECT pricing, COUNT(*) FROM Registration JOIN GroupFitnessClass ON Registration.class_id = GroupFitnessClass.class_id WHERE Registration.class_id = %s GROUP BY pricing", (class_id,))
        result = cur.fetchone()
        if result:
            pricing = result[0]
            total_members = result[1]
            billing_amount = pricing / total_members

            # Insert data into Billing table for each member
            cur.execute("SELECT member_id FROM Registration WHERE class_id = %s", (class_id,))
            member_ids = cur.fetchall()
            for member_id in member_ids:
                cur.execute("INSERT INTO Billing (member_id, amount, date) VALUES (%s, %s, %s)", (member_id[0], billing_amount, datetime.date.today()))
                

            print("Billing processed successfully!")
            
            #insert into payment table
            cur.execute("SELECT bill_id FROM Billing WHERE member_id = %s ORDER BY bill_id DESC LIMIT 1", (member_id,))
            bill_id = cur.fetchone()
            bill_id = bill_id[0]
            cur.execute("INSERT INTO Payment (bill_id, amount, date, status) VALUES (%s, %s, %s, %s)", (bill_id, billing_amount, datetime.date.today(), "Pending"))
            
        else:
            print("No registrations found for the class.")
        print("Group session scheduled successfully!")

        conn.commit()
        cur.close()


def manage_schedule(member_id):
    print("Schedule Management")
    schedule_type = input("Enter schedule type (personal training or group fitness): ")
    try:
        if schedule_type.lower() == "personal training":
            personal_session(member_id)
            
        elif schedule_type.lower() == "group fitness":
            group_schedule(member_id)
            
            
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to manage schedule. Please try again.")
        
def manage_trainer_schedule():
    print("Schedule Management")
    trainer_id = input("Enter your trainer ID: ")
    availability = input("Enter availability (YYYY-MM-DD HH:MM:SS): ")
    duration = input("Enter duration (HH:MM:SS): ")
    pricing = input("Enter Session Charges: ")
    try:
        # Insert trainer availability into the database
        cur = conn.cursor()
        cur.execute("INSERT INTO TrainerAvailability (trainer_id,pricing,date_time, duration) VALUES (%s, %s, %s,%s)", (trainer_id, pricing,availability, duration))
        conn.commit()
        print("Trainer availability set successfully!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to manage schedule. Please try again.")
    
def manage_room_booking():
    print("Room Booking Management")
    room_number = input("Enter room number (room *): ")
    date = input("Enter date (YYYY-MM-DD): ")

    # show current bookings for the room on the date
    try:
        cur = conn.cursor()
        cur.execute("SELECT time, duration FROM RoomBooking WHERE room_number = %s AND date = %s ORDER BY time", (room_number, date))
        bookings = cur.fetchall()
        if bookings:
            print("Current bookings for room", room_number, "on", date, ":")
            for booking in bookings:
                start_time = booking[0]
                duration = booking[1]
                end_time = (datetime.datetime.combine(datetime.date(1, 1, 1), start_time) + duration).time()
                print(f"Booked from {start_time} to {end_time}")
        else:
            print("No bookings for room", room_number, "on", date)

        # enter new booking details
        time = input("Enter time (HH:MM:SS) for the new booking: ")
        duration = input("Enter duration (HH:MM:SS): ")

        # put the new booking into the database
        cur.execute("INSERT INTO RoomBooking (room_number, date, time, duration) VALUES (%s, %s, %s, %s)", (room_number, date, time, duration))
        conn.commit()
        print("Room booking successful!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to manage room booking. Please try again.")
        
def monitor_equipment():
    print("Equipment Maintenance Monitoring")
    #view all equipments
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Equipment")
        equipment = cur.fetchall()
        print("Equipment:")
        for item in equipment:
            print(item)
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to monitor equipment. Please try again.")
    #update equipment status
    print("Update Equipment Status")
    equipment_id = input("Enter equipment ID: ")
    status = input("Enter status of the equipment: ")
    try:
        # Update equipment status in the database
        cur = conn.cursor()
        cur.execute("UPDATE Equipment SET status = %s WHERE equipment_id = %s", (status, equipment_id))
        conn.commit()
        print("Equipment status updated successfully!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to monitor equipment. Please try again.")
        
def create_group_fitness_class():
    print("Group Class Schedule Updating")
    trainer_id = input("Enter trainer ID: ")
    date = input("Enter date for the class (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM:SS): ")
    datetime_input = f"{date} {time}"
    duration = input("Enter duration (HH:MM:SS): ")
    max_capacity = input("Enter maximum capacity: ")
    pricing = input("Enter the price for the class: ")

    # Insert group fitness class details into the database
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO GroupFitnessClass (trainer_id, date, time, duration, max_capacity, pricing) VALUES (%s, %s, %s, %s, %s, %s)",
                    (trainer_id, date, time, duration, max_capacity, pricing))
        conn.commit()
        print("Group fitness class created successfully!")
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        print(f"Error: {e}")
        print("Failed to create group fitness class. Please try again.")
    finally:
        cur.close()


def process_billing(member_id, amount):
    cur = conn.cursor()
    print("Billing and Payment Processing")
    cur.execute("SELECT class_id, pricing FROM Registration JOIN GroupFitnessClass ON Registration.class_id = GroupFitnessClass.class_id WHERE member_id = %s", (member_id,))
    result = cur.fetchone()
    if result:
        class_id, pricing = result
        amount += pricing
        try:
            # Insert billing details into the database
            cur.execute("INSERT INTO Billing (member_id, amount, date) VALUES (%s, %s, %s)", (member_id, amount, datetime.date.today()))
            conn.commit()
            print("Billing processed successfully!")
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to process billing. Please try again.")
    else:
        print("No registration found for the member.")
    cur.close()

def trainer_login():
    print("Trainer Login")
    while True:
        try:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            cur = conn.cursor()
            cur.execute("SELECT trainer_id FROM Trainer WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            if user:
                print("Trainer login successful!")
                return user[0]
            else:
                print("Trainer login failed. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to login trainer. Please try again.")
        finally:
            cur.close()
            
def showbill(member_id):
    cur = conn.cursor()
    cur.execute("SELECT bill_id, amount, date FROM Billing WHERE member_id = %s", (member_id,))
    bill = cur.fetchall()
    print("Billing:")
    for item in bill:
        bill_id, amount, date = item
        cur.execute("SELECT status FROM Payment WHERE bill_id = %s", (bill_id,))
        payment_status = cur.fetchone()
        if payment_status is None:
            payment_status = ("No payment status",)
        print(f"Bill ID: {bill_id}, Amount: {amount}, Date: {date}, Payment Status: {payment_status[0]}")
    cur.close()

def admin_login():
    print("Admin Login")
    while True:
        try:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            cur = conn.cursor()
            cur.execute("SELECT admin_id FROM Admin WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            if user:
                print("Admin login successful!")
                return user[0]
            else:
                print("Admin login failed. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to login admin. Please try again.")
        finally:
            cur.close()
            
     
def trainer_ui():
    print("\nHealth and Fitness Club Management System - Trainer")
    if(trainer_login()):
        while True:
            print("\n1. Schedule Management")
            print("2. Member Profile Viewing")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                manage_trainer_schedule()
            elif choice == "2":
                member_name = input("Enter member's name: ")
                member_profile_viewing_by_name(member_name)

def member_profile_viewing_by_name(name):
    query = "SELECT member_id FROM Member WHERE name ILIKE %s"
    with conn.cursor() as cur:
        cur.execute(query, (f"%{name}%",))
        members = cur.fetchall()
        if members:
            for member in members:
                member_id = member[0]
                print(f"\nDisplaying dashboard for Member ID: {member_id}")
                display_dashboard(member_id)
        else:
            print("No member found with that name.")
                
def admin_ui():
    print("\nHealth and Fitness Club Management System - Admin")
    print("Admin Login")
    if(admin_login()):
        while True:
            print("\n1. Room Booking Management")
            print("2. Equipment Maintenance Monitoring")
            print("3. Group Class Schedule Updating")
            print("4. Billing and Payment Processing")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                manage_room_booking()
            elif choice == "2":
                monitor_equipment()
            elif choice == "3":
                create_group_fitness_class()
            elif choice == "4":
                showbill(input("Enter member ID: "))
            elif choice == "5":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
def member_ui():
    print("\nHealth and Fitness Club Management System")
    member_id = login_user()
    while True:
        print("\n1. User Registration")
        print("2. Profile Management")
        print("3. Dashboard Display")
        print("4. Schedule Management")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            member_id = register_user()
        elif choice == "2":
            manage_profile(member_id)
        elif choice == "3":
            display_dashboard(member_id)
        elif choice == "4":
            add_or_cancel_schedule(member_id)
        elif choice == "5":
            print("Exiting program. Goodbye!")
        else:
            print("Invalid choice. Please try again.")
            
        
def main():
    while True:
        user=input("Are you a member, trainer, admin? or REGISTER now💪! (member/trainer/admin/register): ")
        if user=="member":
            member_ui()
        elif user=="trainer":
            trainer_ui()
        elif user=="admin":
            admin_ui()
        elif user=="register":
            register_user()
        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()