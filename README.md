# Chronos - Employee Scheduling System

A professional shift scheduling application designed for restaurants and other shift-based businesses. Built with Python and Tkinter, Chronos provides an intuitive GUI for managing employees, creating schedules, and tracking payroll costs.

## Features

### Employee Management
- Add, edit, and delete employees with detailed profiles
- Track employee roles, wages, and contact information
- Set maximum hours and minor status for compliance
- Define employee availability by day and time
- View comprehensive employee details and availability

### Schedule Management
- Create weekly schedules (Monday-Sunday)
- Visual schedule view with daily tabs
- Track schedule dates and periods
- Support for multiple concurrent schedules
- Easy schedule selection and navigation

### Shift Management
- Create shifts with specific dates, times, and role requirements
- Assign employees to shifts with automatic validation
- Conflict detection (availability checking, role matching)
- View all shifts across all schedules in one place
- Track shift fill status (filled/unfilled)

### Payroll Calculation
- Automatic payroll cost calculation per shift
- Total payroll calculation per schedule
- Real-time cost updates when employees are assigned
- Display costs in schedule and shift views
- Support for varying wage rates

### Data Persistence
- JSON-based data storage
- Automatic backup creation on save
- Auto-save on application exit
- Load existing data on startup
- Maintains ID counters across sessions

### User Interface
- Clean, modern Tkinter-based GUI
- Tabbed interface for easy navigation
- Dashboard with quick statistics and recent activity
- Color-coded status indicators
- Professional styling with ttk widgets

## 📋 Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- No additional dependencies required!

## 🚀 Installation

1. Clone or download this repository:
```bash
git clone https://github.com/Adolin42/capstone_scheduling_program.git
cd capstone_scheduling_program
```

2. Ensure Python 3.7+ is installed:
```bash
python --version
```

3. Run the application:
```bash
python chronos.py
```

## 💡 Usage

### Getting Started

When you first run Chronos, sample data will be automatically loaded to demonstrate the system. You can delete this sample data and start fresh.

### Managing Employees

1. Navigate to the **👥 Employees** tab
2. Click **➕ Add Employee** to create new employee profiles
3. Fill in employee details:
   - Name, phone, email
   - Role (server, cook, host, manager, etc.)
   - Hourly wage
   - Maximum hours per week
   - Minor status (under 18)
4. Edit or delete employees using the action buttons
5. Click **👁️ View Details** to see full employee information including availability

### Creating Schedules

1. Navigate to the **📅 Schedules** tab
2. Click **📅 New Schedule**
3. Enter the start date (should be a Monday)
4. The system automatically creates a week-long schedule (Monday-Sunday)
5. Select schedules from the dropdown to switch between them

### Adding Shifts

1. Select a schedule in the **📅 Schedules** tab
2. Click **⏰ Add Shift**
3. Enter shift details:
   - Date (must be within schedule range)
   - Start time (24-hour format, e.g., 0900)
   - End time (24-hour format, e.g., 1700)
   - Required role
4. The shift will appear in the appropriate day tab

### Assigning Employees

Currently, employees must be assigned to shifts programmatically or through the test scripts. A GUI-based assignment feature is planned for future releases.

**Automatic Validation:**
- Employee must be available during shift hours
- Employee role must match shift requirements (or be a manager)
- No double-booking on the same shift
- Respects maximum staff limits per shift

### Viewing Payroll Costs

- **Schedule View**: Each shift displays its cost, and the total schedule payroll appears at the top
- **Shifts Tab**: All shifts show individual payroll costs
- Costs are automatically calculated as: `Wage × Shift Duration × Number of Assigned Employees`
- Unassigned shifts show $0.00 cost

### Saving Data

- Data is automatically saved when you:
  - Add, edit, or delete employees
  - Create or delete schedules
  - Add shifts
  - Close the application (with confirmation)
- Data is stored in `data/scheduling_data.json`
- Backups are created at `data/scheduling_data.backup.json`

## 📁 Project Structure

```
capstone_scheduling_program/
├── main.py                      # Main GUI application
├── requirements.md              # Project requirements document
├── README.md                    # This file
├── test_comprehensive.py        # Comprehensive integration tests
├── test_shift_employee.py       # Unit tests for shift-employee integration
├── test_json_employees.py       # JSON serialization tests for employees
├── test_json_complete.py        # Complete JSON serialization tests
├── test_persistence.py          # Data persistence verification tests
├── modules/
│   ├── __init__.py             # Package initialization
│   ├── employee.py             # Employee class and logic
│   ├── shift.py                # Shift class and logic
│   └── schedule.py             # Schedule class and logic
├── data/
│   ├── scheduling_data.json    # Main data file (created on first save)
│   └── scheduling_data.backup.json  # Automatic backup
└── .vscode/
    └── settings.json           # VS Code configuration
```

## 🏗️ Architecture

### Object-Oriented Design

**Employee Class** (`modules/employee.py`)
- Manages employee data and availability
- Validates availability against shift requirements
- Supports JSON serialization

**Shift Class** (`modules/shift.py`)
- Handles shift creation and employee assignment
- Calculates shift duration and payroll costs
- Detects scheduling conflicts
- Validates role requirements

**Schedule Class** (`modules/schedule.py`)
- Manages collections of shifts
- Enforces date range constraints
- Calculates total payroll for all shifts
- Provides shift lookup by date or employee

**SchedulingApp Class** (`main.py`)
- Main GUI application controller
- Manages all user interactions
- Handles data persistence
- Coordinates between UI and business logic

### Data Persistence

- **Format**: JSON
- **Location**: `data/scheduling_data.json`
- **Structure**:
  ```json
  {
    "employees": [...],
    "schedules": [...],
    "metadata": {
      "version": "1.0",
      "last_saved": "ISO timestamp",
      "next_employee_id": 10008,
      "next_shift_id": 1043,
      "next_schedule_id": 1002
    }
  }
  ```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Test basic shift-employee integration
python test_shift_employee.py

# Test comprehensive scheduling scenario
python test_comprehensive.py

# Test JSON serialization for employees
python test_json_employees.py

# Test complete JSON serialization (all classes)
python test_json_complete.py

# Test data persistence across sessions
python test_persistence.py
```

## 🔮 Future Enhancements

### Planned Features
- [ ] GUI-based employee-to-shift assignment dialog
- [ ] Drag-and-drop shift assignment
- [ ] Shift swapping between employees
- [ ] Overtime calculation (1.5x after 40 hours)
- [ ] Export schedules to PDF/CSV
- [ ] Print-friendly schedule views
- [ ] Email notifications to employees
- [ ] Schedule templates for recurring patterns
- [ ] Multi-location support
- [ ] Advanced conflict detection (double-booking across schedules)
- [ ] Labor cost budgeting and alerts
- [ ] Employee time-off requests
- [ ] Schedule history and archiving
- [ ] Reporting and analytics dashboard

### Technical Improvements
- [ ] Database backend (SQLite/PostgreSQL)
- [ ] User authentication and roles
- [ ] Web-based version
- [ ] Mobile app companion
- [ ] Automated schedule optimization
- [ ] Integration with payroll systems

## 📊 Business Rules

- Employees can only be assigned to shifts during their available hours
- Employees must have the required role for a shift (or be a manager)
- Managers can work any role
- Shifts must fall within their schedule's date range
- Each shift tracks minimum and maximum staff requirements
- Unassigned shifts display as "UNASSIGNED" with $0.00 cost

## 👥 Author

**Ptolemy Linden**  
Computer Science Student, California State University, Chico  
Capstone Project - Fall 2025

## 📝 License

This project was created as a capstone project for educational purposes.

## 🙏 Acknowledgments

- California State University, Chico - Computer Science Department
- Inspired by real-world scheduling challenges in the restaurant industry
- Sample employee names used for demonstration purposes only

## 📞 Support

For questions or issues related to this project, please contact through the repository's issue tracker.

---

**Note**: This application is designed for educational and demonstration purposes. For production use in a business environment, additional features like enhanced security, user authentication, and comprehensive error handling should be implemented.
