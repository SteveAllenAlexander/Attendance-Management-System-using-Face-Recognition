import tkinter as tk
from tkinter import messagebox, ttk
import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime

# Initialize Tkinter window with color
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("650x600")
root.configure(bg="#add8e6")  # Light blue background

# Paths for CSV Files
student_data_file = 'student_data.csv'
attendance_file = 'attendance.csv'

# Ensure CSV files exist
if not os.path.exists(student_data_file):
    with open(student_data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Roll Number', 'Name', 'Branch', 'Encoding'])

if not os.path.exists(attendance_file):
    with open(attendance_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Roll Number', 'Name', 'Branch', 'Date', 'Time'])

# Function to capture face with preview window
def capture_face_preview():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Face Capture - Press 's' to Save")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Face Capture - Press 's' to Save", frame)
        
        # Press 's' to save face and 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cam.release()
            cv2.destroyAllWindows()
            return frame
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            return None
    cam.release()
    cv2.destroyAllWindows()

# Function to register a new student with face encoding
def register_student():
    roll_number = roll_number_entry.get()
    name = name_entry.get()
    branch = branch_entry.get()

    if not roll_number or not name or not branch:
        messagebox.showerror("Error", "Please enter Roll Number, Name, and Branch.")
        return

    frame = capture_face_preview()
    if frame is not None:
        face_encodings = face_recognition.face_encodings(frame)
        if face_encodings:
            encoding = face_encodings[0]
            encoding_str = np.array2string(encoding, separator=',')
            
            # Save student details with encoding in CSV
            with open(student_data_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([roll_number, name, branch, encoding_str])

            messagebox.showinfo("Registration", "Student Registered Successfully!")
        else:
            messagebox.showerror("Error", "No face detected!")
    else:
        messagebox.showerror("Error", "Face capture cancelled.")

# Function to mark attendance with a preview window
def mark_attendance():
    frame = capture_face_preview()
    if frame is not None:
        face_encodings = face_recognition.face_encodings(frame)
        if face_encodings:
            current_encoding = face_encodings[0]
            
            # Load student encodings from CSV
            with open(student_data_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    roll_number, name, branch, encoding_str = row
                    stored_encoding = np.fromstring(encoding_str[1:-1], sep=',')

                    # Check for a match
                    matches = face_recognition.compare_faces([stored_encoding], current_encoding)
                    if matches[0]:
                        now = datetime.now()
                        date_str = now.strftime("%Y-%m-%d")
                        time_str = now.strftime("%H:%M:%S")

                        # Save attendance in CSV
                        with open(attendance_file, 'a', newline='') as attendance_file_obj:
                            writer = csv.writer(attendance_file_obj)
                            writer.writerow([roll_number, name, branch, date_str, time_str])

                        messagebox.showinfo("Attendance", f"Attendance marked for {name}!")
                        load_attendance()  # Refresh attendance table
                        return
            messagebox.showerror("Error", "Face not recognized!")
        else:
            messagebox.showerror("Error", "No face detected!")
    else:
        messagebox.showerror("Error", "Face capture cancelled.")

# Function to load attendance records into the table
def load_attendance():
    for row in attendance_table.get_children():
        attendance_table.delete(row)
    
    with open(attendance_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            attendance_table.insert('', tk.END, values=row)

# Function to display registered student details in a new window
def display_student_details():
    details_window = tk.Toplevel(root)
    details_window.title("Student Details")
    details_window.geometry("500x300")
    details_window.configure(bg="#add8e6")

    student_table = ttk.Treeview(details_window, columns=("Roll Number", "Name", "Branch"), show="headings")
    student_table.heading("Roll Number", text="Roll Number")
    student_table.heading("Name", text="Name")
    student_table.heading("Branch", text="Branch")
    student_table.pack(fill=tk.BOTH, expand=True)

    # Load student data from CSV
    with open(student_data_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            student_table.insert('', tk.END, values=(row[0], row[1], row[2]))

# GUI Elements for Registration with colors
title_label = tk.Label(root, text="Attendance Management System", font=("Helvetica", 16), bg="#add8e6", fg="blue")
title_label.pack(pady=10)

roll_label = tk.Label(root, text="Roll Number", font=("Helvetica", 12), bg="#add8e6", fg="darkblue")
roll_label.pack(pady=5)
roll_number_entry = tk.Entry(root)
roll_number_entry.pack(pady=5)

name_label = tk.Label(root, text="Name", font=("Helvetica", 12), bg="#add8e6", fg="darkblue")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

branch_label = tk.Label(root, text="Branch", font=("Helvetica", 12), bg="#add8e6", fg="darkblue")
branch_label.pack(pady=5)
branch_entry = tk.Entry(root)
branch_entry.pack(pady=5)

register_button = tk.Button(root, text="Register Student", command=register_student, bg="green", fg="white", font=("Helvetica", 12))
register_button.pack(pady=10)

attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance, bg="orange", fg="white", font=("Helvetica", 12))
attendance_button.pack(pady=10)

display_button = tk.Button(root, text="Display Student Details", command=display_student_details, bg="purple", fg="white", font=("Helvetica", 12))
display_button.pack(pady=10)

# Attendance Table
table_frame = tk.Frame(root)
table_frame.pack(pady=20)

attendance_table = ttk.Treeview(table_frame, columns=("Roll Number", "Name", "Branch", "Date", "Time"), show="headings")
attendance_table.heading("Roll Number", text="Roll Number")
attendance_table.heading("Name", text="Name")
attendance_table.heading("Branch", text="Branch")
attendance_table.heading("Date", text="Date")
attendance_table.heading("Time", text="Time")
attendance_table.pack()

# Refresh Attendance Button
refresh_button = tk.Button(root, text="Refresh Attendance", command=load_attendance, bg="blue", fg="white", font=("Helvetica", 12))
refresh_button.pack(pady=10)

# Load attendance on startup
load_attendance()

root.mainloop()