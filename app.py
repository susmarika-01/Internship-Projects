import streamlit as st
import pandas as pd
from datetime import date
import os
import glob

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    .attendance-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    .attendance-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .employee-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.2rem;
    }
    .employee-details {
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .stRadio > div {
        flex-direction: row !important;
        gap: 1rem !important;
    }
    .stRadio > div > label {
        background: #f8f9fa !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
        transition: all 0.3s ease !important;
        margin-right: 1rem !important;
    }
    .stRadio > div > label:hover {
        border-color: #667eea !important;
        background: #f0f4ff !important;
    }
    .stRadio > div > label[data-testid="stRadio"]:has(input[value="Present"]:checked) {
        background: #d1fae5 !important;
        border-color: #10b981 !important;
        color: #065f46 !important;
    }
    .stRadio > div > label[data-testid="stRadio"]:has(input[value="Absent"]:checked) {
        background: #fee2e2 !important;
        border-color: #ef4444 !important;
        color: #991b1b !important;
    }
    .save-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        width: 100%;
        margin-top: 2rem;
        transition: all 0.3s ease !important;
    }
    .save-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    .success-message {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        color: #065f46;
        font-weight: 600;
        margin-top: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem;
    }
    .present-stat {
        border-left: 4px solid #10b981;
    }
    .absent-stat {
        border-left: 4px solid #ef4444;
    }
    .total-stat {
        border-left: 4px solid #667eea;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .sidebar-section {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .quick-stats {
        font-size: 0.9rem;
        color: #6b7280;
    }
    .stat-value {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-header">🏢 Company Dashboard</div>', unsafe_allow_html=True)
    st.subheader("📅 Today's Date")
    today = date.today()
    st.write(f"**{today.strftime('%B %d, %Y')}**")
    st.write(f"*{today.strftime('%A')}*")
    st.subheader("📊 Quick Stats")
    
    try:
        employees = pd.read_csv("data/employees.csv")
        total_employees = len(employees)
        attendance_files = glob.glob("data/*.csv")
        date_files = []
        for file in attendance_files:
            filename = os.path.basename(file)
            if filename != "employees.csv" and filename.endswith('.csv'):
                try:
                    date_str = filename.replace('.csv', '')
                    file_date = pd.to_datetime(date_str).date()
                    date_files.append((file_date, file))
                except:
                    continue
        
        total_records = len(date_files)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="quick-stats">Total Employees<br><span class="stat-value">{total_employees}</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="quick-stats">Attendance Records<br><span class="stat-value">{total_records}</span></div>', unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.warning("No employee data found")
    
    data_dir_exists = os.path.exists("data")
    employees_file_exists = os.path.exists("data/employees.csv")
    
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.markdown(f'<div class="quick-stats">Data Directory<br><span class="stat-value" style="color: {"#10b981" if data_dir_exists else "#ef4444"}">{"✅" if data_dir_exists else "❌"}</span></div>', unsafe_allow_html=True)
    with status_col2:
        st.markdown(f'<div class="quick-stats">Employee Data<br><span class="stat-value" style="color: {"#10b981" if employees_file_exists else "#ef4444"}">{"✅" if employees_file_exists else "❌"}</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    

st.markdown('<div class="main-header">🎓 Attendance Management System</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Mark Today's Attendance", "📊 View Past Attendance"])

with tab1:
    try:
        employees = pd.read_csv("data/employees.csv")
        today = date.today()
        filename = f"data/{today}.csv"

        attendance = {}

        for _, row in employees.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="attendance-card">
                    <div class="employee-name">{row['Name']}</div>
                    <div class="employee-details">
                        ID: {row['EmployeeID']} | Department: {row['Department']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                attendance[row['EmployeeID']] = st.radio(
                    f"Attendance for {row['Name']}",
                    ["Present", "Absent"],
                    key=row['EmployeeID'],
                    label_visibility="collapsed"
                )

        if st.button("💾 Save Attendance", key="save_attendance"):
            df = pd.DataFrame([{
                "date": today,
                "employee_id": emp_id,
                "employee_name": employees.loc[employees['EmployeeID']==emp_id, 'Name'].values[0],
                "status": status
            } for emp_id, status in attendance.items()])

            df.to_csv(filename, index=False)
            st.markdown(f"""
            <div class="success-message">
                ✅ Attendance saved for {len(attendance)} employees for {today}
            </div>
            """, unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error("❌ Employee data file not found. Please make sure 'data/employees.csv' exists.")
        st.info("💡 Create a CSV file with columns: EmployeeID, Name, Department")

with tab2:
    st.markdown('<div class="section-header">📊 View Past Attendance</div>', unsafe_allow_html=True)
    
    os.makedirs("data", exist_ok=True)
    
    attendance_files = glob.glob("data/*.csv")

    date_files = []
    for file in attendance_files:
        filename = os.path.basename(file)
        if filename != "employees.csv" and filename.endswith('.csv'):
            try:
                date_str = filename.replace('.csv', '')
                file_date = pd.to_datetime(date_str).date()
                date_files.append((file_date, file))
            except:
                continue
    
    date_files.sort(reverse=True)
    
    if not date_files:
        st.info("📝 No attendance records found. Mark attendance to see historical data.")
    else:
        # Create dropdown with formatted dates
        date_options = {date.strftime("%B %d, %Y"): file_path for date, file_path in date_files}
        selected_date_str = st.selectbox(
            "📅 Select Date to View Attendance",
            options=list(date_options.keys()),
            index=0
        )
        
        if selected_date_str:
            selected_file = date_options[selected_date_str]
            
            try:
                attendance_df = pd.read_csv(selected_file)
                
                st.markdown("### 📈 Attendance Summary")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_employees = len(attendance_df)
                    st.markdown(f"""
                    <div class="stats-card total-stat">
                        <h3>Total Employees</h3>
                        <h2>{total_employees}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    present_count = len(attendance_df[attendance_df['status'] == 'Present'])
                    st.markdown(f"""
                    <div class="stats-card present-stat">
                        <h3>Present</h3>
                        <h2 style="color: #10b981;">{present_count}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    absent_count = len(attendance_df[attendance_df['status'] == 'Absent'])
                    st.markdown(f"""
                    <div class="stats-card absent-stat">
                        <h3>Absent</h3>
                        <h2 style="color: #ef4444;">{absent_count}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                attendance_rate = (present_count / total_employees * 100) if total_employees > 0 else 0
                st.metric("📊 Attendance Rate", f"{attendance_rate:.1f}%")
                
                st.markdown("### 👥 Employee Attendance Details")
            
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Present", "Absent"],
                    key="status_filter"
                )
     
                filtered_df = attendance_df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df['status'] == status_filter]
                
                sort_by = st.selectbox(
                    "Sort by",
                    ["Name", "Status", "Employee ID"],
                    key="sort_by"
                )
                
                if not filtered_df.empty:
                    display_df = filtered_df[['employee_id', 'employee_name', 'status']].copy()
                    display_df.columns = ['Employee ID', 'Name', 'Status']
                    
                    def style_status(val):
                        if val == 'Present':
                            return 'color: #10b981; font-weight: bold;'
                        else:
                            return 'color: #ef4444; font-weight: bold;'
                    
                    st.dataframe(
                        display_df.style.applymap(style_status, subset=['Status']),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Attendance Data",
                        data=csv,
                        file_name=f"attendance_{selected_date_str.replace(',', '').replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No records found for the selected filters.")
                    
            except Exception as e:
                st.error(f"❌ Error reading attendance file: {str(e)}")