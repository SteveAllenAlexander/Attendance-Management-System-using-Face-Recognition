# Attendance-Management-System-using-Face-Recognition
This project is an Attendance Management System that utilizes Face Recognition to mark and record student attendance. Built with Python, it uses the Tkinter library for a colorful graphical user interface (GUI) and OpenCV for real-time face capture and recognition.

Key Features:
Student Registration: Allows adding students by capturing their face, along with essential details like roll number, name, and branch. Each student's unique facial encoding is stored, ensuring accurate identification during attendance marking.

Face Recognition Attendance: Using a live camera feed, the system compares real-time face encodings with registered student data, marking attendance if a match is found. Each attendance record includes the student's roll number, name, branch, date, and time.

Data Display and Management:
Attendance Records: A table within the GUI displays daily attendance records, with a refresh option for real-time updates.
Student Database Viewing: Students already in the system can be viewed with a single button click.
Automatic Duplicate Check: Prevents duplicate entries for both registration and attendance marking.
