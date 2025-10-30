from flask import Flask, render_template, request, redirect, jsonify, send_file
import qrcode
import cv2
import csv
import os
from datetime import datetime
import threading
import time
import io

app = Flask(__name__)

# Get the absolute path to avoid relative path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_CODES_DIR = os.path.join(BASE_DIR, "static", "qrcodes")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "static", "attendance")

# Ensure directories exist with absolute paths
os.makedirs(QR_CODES_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

print(f"QR Codes Directory: {QR_CODES_DIR}")
print(f"Attendance Directory: {ATTENDANCE_DIR}")

# Global variables
is_camera_running = False
current_scan_result = None
last_scan_time = 0
scanned_employee_data = None

# ---------- HOME PAGE ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- REGISTER EMPLOYEE ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        dept = request.form['dept']

        # Generate QR code
        qr_data = f"{emp_id}|{name}|{dept}"
        qr = qrcode.make(qr_data)
        
        # Save QR code with both ID and name for easy identification
        filename = f"{emp_id}_{name.replace(' ', '_')}.png"
        qr_path = os.path.join(QR_CODES_DIR, filename)
        qr.save(qr_path)

        return f"""
        <h3>QR Code generated for {name}!</h3>
        <img src='/static/qrcodes/{filename}' width='200'><br><br>
        <a href='/download_qr/{filename}'>Download QR Code</a><br><br>
        <a href='/register'>Register Another</a> | 
        <a href='/'>Home</a>
        """

    return render_template('register_employee.html')

# ---------- DOWNLOAD QR CODE ----------
@app.route('/download_qr/<filename>')
def download_qr(filename):
    """Download QR code file"""
    try:
        qr_path = os.path.join(QR_CODES_DIR, filename)
        if os.path.exists(qr_path):
            return send_file(qr_path, as_attachment=True, download_name=filename)
        else:
            return "QR code not found", 404
    except Exception as e:
        return f"Error downloading QR code: {str(e)}", 500

# ---------- DOWNLOAD ATTENDANCE CSV ----------
@app.route('/download_attendance/<filename>')
def download_attendance(filename):
    """Download attendance CSV file"""
    try:
        file_path = os.path.join(ATTENDANCE_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return "Attendance file not found", 404
    except Exception as e:
        return f"Error downloading attendance file: {str(e)}", 500

# ---------- DOWNLOAD ALL ATTENDANCE ----------
@app.route('/download_all_attendance')
def download_all_attendance():
    """Download all attendance data as a single CSV file"""
    try:
        # Create a combined CSV with all attendance data
        all_records = []
        header = ['Employee ID', 'Name', 'Department', 'Date', 'Check-in', 'Check-out', 'Status']
        
        if os.path.exists(ATTENDANCE_DIR):
            files = [f for f in os.listdir(ATTENDANCE_DIR) if f.startswith('attendance_') and f.endswith('.csv')]
            
            for file in sorted(files):
                file_path = os.path.join(ATTENDANCE_DIR, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    # Skip header for all files except first, and add all data rows
                    if not all_records:
                        all_records.append(header)
                    all_records.extend(rows[1:])  # Skip header of individual files
        
        # Create in-memory CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(all_records)
        
        # Prepare response
        output.seek(0)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"all_attendance_data_{today}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        return f"Error creating combined attendance file: {str(e)}", 500

# ---------- PROCESS ATTENDANCE ----------
def process_attendance(emp_id, name, dept, action):
    """Process check-in or check-out for an employee"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(ATTENDANCE_DIR, f"attendance_{today}.csv")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Ensure directory exists
        os.makedirs(ATTENDANCE_DIR, exist_ok=True)
        
        if action == "checkin":
            # Check if already checked in today
            if os.path.exists(file_path):
                with open(file_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    for row in rows[1:]:  # Skip header
                        if row and len(row) >= 6 and row[0] == emp_id and row[4] != '' and row[5] == '':
                            return {"success": False, "message": f"{name} is already checked in today!"}
            
            # Add check-in record
            file_exists = os.path.exists(file_path)
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header if file is new
                if not file_exists or os.path.getsize(file_path) == 0:
                    writer.writerow(['Employee ID', 'Name', 'Department', 'Date', 'Check-in', 'Check-out', 'Status'])
                
                writer.writerow([emp_id, name, dept, current_date, current_time, '', 'Present'])
            
            return {"success": True, "message": f"✅ {name} checked in successfully at {current_time}"}
        
        elif action == "checkout":
            if not os.path.exists(file_path):
                return {"success": False, "message": f"{name} has not checked in today!"}
            
            # Find check-in record to update
            updated = False
            rows = []
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            for i, row in enumerate(rows):
                if i > 0 and row and len(row) >= 6 and row[0] == emp_id and row[4] != '' and row[5] == '':
                    row[5] = current_time
                    if len(row) > 6:
                        row[6] = 'Checked Out'
                    else:
                        row.append('Checked Out')
                    updated = True
                    break
            
            if updated:
                # Write updated data back to file
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(rows)
                return {"success": True, "message": f"🏠 {name} checked out successfully at {current_time}"}
            else:
                return {"success": False, "message": f"{name} has not checked in today or already checked out!"}
        
        return {"success": False, "message": "Invalid action"}
    
    except Exception as e:
        print(f"Error processing attendance: {str(e)}")
        return {"success": False, "message": f"Error processing attendance: {str(e)}"}

# ---------- CAMERA SCANNING FUNCTION ----------
def start_scanner():
    global is_camera_running, current_scan_result, last_scan_time, scanned_employee_data
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while is_camera_running:
        success, img = cam.read()
        if not success:
            break

        data, bbox, _ = detector.detectAndDecode(img)

        # Process QR code data
        if data and (time.time() - last_scan_time > 2):
            try:
                emp_id, name, dept = data.split('|')
                current_scan_result = {
                    'emp_id': emp_id,
                    'name': name,
                    'dept': dept,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                # Store the scanned data for later use
                scanned_employee_data = current_scan_result.copy()
                last_scan_time = time.time()
                print(f"QR Scanned: {name} ({emp_id}) - {dept}")
                
            except Exception as e:
                print("Invalid QR code data:", e)
                current_scan_result = {
                    'error': 'Invalid QR code format'
                }

        # Draw bounding box if QR detected
        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i])
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                cv2.line(img, pt1, pt2, (0, 255, 0), 2)

        cv2.imshow("QR Attendance Scanner - Press Q to quit", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    is_camera_running = False
    current_scan_result = None

# ---------- SCANNER INTERFACE ----------
@app.route('/scanner')
def scanner_interface():
    return render_template('scanner.html')

# ---------- START CAMERA ----------
@app.route('/start_scan')
def start_scan():
    global is_camera_running, current_scan_result, scanned_employee_data
    if not is_camera_running:
        is_camera_running = True
        current_scan_result = None
        scanned_employee_data = None
        threading.Thread(target=start_scanner, daemon=True).start()
    return redirect('/scanner')

# ---------- STOP CAMERA ----------
@app.route('/stop_scan')
def stop_scan():
    global is_camera_running
    is_camera_running = False
    return redirect('/scanner')

# ---------- GET SCAN RESULT ----------
@app.route('/get_scan_result')
def get_scan_result():
    global current_scan_result, scanned_employee_data
    if current_scan_result:
        result = current_scan_result.copy()
        return jsonify(result)
    elif scanned_employee_data:
        return jsonify(scanned_employee_data)
    return jsonify({'status': 'no_scan'})

# ---------- CHECK IN ----------
@app.route('/checkin', methods=['POST'])
def check_in():
    global scanned_employee_data
    if scanned_employee_data and 'emp_id' in scanned_employee_data:
        result = process_attendance(
            scanned_employee_data['emp_id'],
            scanned_employee_data['name'],
            scanned_employee_data['dept'],
            "checkin"
        )
        return jsonify(result)
    return jsonify({"success": False, "message": "No QR code scanned. Please scan a QR code first."})

# ---------- CHECK OUT ----------
@app.route('/checkout', methods=['POST'])
def check_out():
    global scanned_employee_data
    if scanned_employee_data and 'emp_id' in scanned_employee_data:
        result = process_attendance(
            scanned_employee_data['emp_id'],
            scanned_employee_data['name'],
            scanned_employee_data['dept'],
            "checkout"
        )
        return jsonify(result)
    return jsonify({"success": False, "message": "No QR code scanned. Please scan a QR code first."})

# ---------- CLEAR SCAN DATA ----------
@app.route('/clear_scan')
def clear_scan():
    global scanned_employee_data, current_scan_result
    scanned_employee_data = None
    current_scan_result = None
    return jsonify({"success": True, "message": "Scan data cleared"})

# ---------- VIEW ATTENDANCE ----------
@app.route('/view')
def view_attendance():
    try:
        files = os.listdir(ATTENDANCE_DIR)
        files = [f for f in files if f.startswith('attendance_') and f.endswith('.csv')]
        files = sorted(files, reverse=True)
        
        # Get today's records if available
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = f"attendance_{today}.csv"
        today_records = []
        
        today_path = os.path.join(ATTENDANCE_DIR, today_file)
        if os.path.exists(today_path):
            with open(today_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                today_records = list(reader)
        
        return render_template('view_attendance.html', 
                             files=files, 
                             today_records=today_records,
                             today_date=today)
    except Exception as e:
        return f"Error loading attendance: {str(e)}"

# ---------- VIEW SPECIFIC ATTENDANCE FILE ----------
@app.route('/view/<filename>')
def view_specific_attendance(filename):
    try:
        file_path = os.path.join(ATTENDANCE_DIR, filename)
        records = []
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                records = list(reader)
        
        return render_template('view_specific.html', 
                             records=records, 
                             filename=filename)
    except Exception as e:
        return f"Error loading attendance file: {str(e)}"

# ---------- LIST ALL QR CODES ----------
@app.route('/qrcodes')
def list_qrcodes():
    """List all generated QR codes"""
    try:
        qr_files = []
        if os.path.exists(QR_CODES_DIR):
            qr_files = [f for f in os.listdir(QR_CODES_DIR) if f.endswith('.png')]
            qr_files.sort()
        
        return render_template('qrcodes_list.html', qr_files=qr_files)
    except Exception as e:
        return f"Error loading QR codes: {str(e)}"

if __name__ == '__main__':
    print("🚀 Starting QR Attendance System...")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"📊 Attendance files will be saved to: {ATTENDANCE_DIR}")
    print(f"📱 QR codes will be saved to: {QR_CODES_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5000)