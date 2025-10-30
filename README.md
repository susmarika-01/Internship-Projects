## QR Attendance System
A modern web-based attendance management system using QR code technology. Built with Flask, OpenCV, and Python.

🚀 Quick Start
bash
# Install dependencies
pip install flask qrcode opencv-python

# Run the application
python app.py

# Access at: http://localhost:5000
🔧 How It Works
Employee Registration: Add employee details (name, ID, department) to generate personalized QR codes
QR Code Distribution: Employees receive their unique QR codes (printable or digital)
Attendance Scanning: Use the built-in scanner to read QR codes - system automatically records timestamps
Data Management: View attendance records, track late arrivals, and generate reports
Export Options: Download attendance data as CSV files for further analysis

💡 Key Features
Real-time QR Code Scanning with live camera feed
Automatic Duplicate Prevention - prevents multiple check-ins
Responsive Web Interface - works on desktop, tablet, and mobile
CSV Export - download attendance data for record-keeping
Employee Management - easy registration and QR code generation
No External Dependencies - runs completely offline after setup

🏢 Use Cases
Office Attendance - Employee daily check-ins/check-outs
School/College - Student attendance tracking
Events - Participant registration and tracking
Workshops - Session attendance monitoring
Construction Sites - Worker time tracking

📁 Project Structure
text
qr-attendance-system/
├── app.py                 # Main Flask application
├── templates/            # Web interface pages
│   ├── index.html        # Dashboard
│   ├── register_employee.html
│   ├── scanner.html      # QR scanning interface
│   ├── view_attendance.html
│   └── qrcodes_list.html
└── static/
    ├── qrcodes/          # Generated QR code images
    └── attendance/       # Attendance records (CSV files)
    
🛠 Technology Stack
Backend: Python, Flask
QR Processing: OpenCV, qrcode
Frontend: HTML5, CSS3, JavaScript
Data Storage: CSV files
Computer Vision: Real-time camera processing
This system provides a cost-effective, efficient alternative to expensive biometric systems while maintaining accuracy and ease of use. Perfect for small to medium businesses, educational institutions, and organizations looking to digitize their attendance tracking process.
