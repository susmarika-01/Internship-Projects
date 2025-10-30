### QR Attendance System

## Quick Start
pip install flask qrcode opencv-python
python app.py
# Access at: http://localhost:5000

## How It Works
# 1. Employee Registration: Add details to generate QR codes
# 2. QR Code Distribution: Employees get unique QR codes  
# 3. Attendance Scanning: Scan QR codes to record timestamps
# 4. Data Management: View records and generate reports
# 5. Export Options: Download CSV files for analysis

## Key Features
# - Real-time QR Code Scanning with camera
# - Automatic Duplicate Prevention
# - Responsive Web Interface
# - CSV Export capability
# - Employee Management system
# - Offline functionality

## Use Cases
# - Office Attendance tracking
# - School/College student tracking
# - Event participant registration
# - Workshop attendance monitoring
# - Construction site worker tracking

## Project Structure
# qr-attendance-system/
# ├── app.py (Main Flask application)
# ├── templates/ (Web interface pages)
# │   ├── index.html (Dashboard)
# │   ├── register_employee.html
# │   ├── scanner.html (QR scanning)
# │   ├── view_attendance.html
# │   └── qrcodes_list.html
# └── static/
#     ├── qrcodes/ (Generated QR code images)
#     └── attendance/ (Attendance CSV records)

## Technology Stack
# Backend: Python, Flask
# QR Processing: OpenCV, qrcode
# Frontend: HTML5, CSS3, JavaScript
# Data Storage: CSV files
# Computer Vision: Real-time camera processing

# This system provides a cost-effective, efficient alternative to expensive biometric systems while maintaining accuracy and ease of use. Perfect for small to medium businesses, educational institutions, and organizations looking to digitize their attendance tracking process.
