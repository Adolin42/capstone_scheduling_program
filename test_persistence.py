"""
Test script to verify JSON persistence in the main application
This simulates creating data and verifying it persists across sessions
"""

import os
import json
from modules.employee import Employee
from modules.shift import Shift
from modules.schedule import Schedule

print("=" * 70)
print("TESTING DATA PERSISTENCE")
print("=" * 70)

# Clean up any existing test data
if os.path.exists('data/scheduling_data.json'):
    print("\n1. Removing existing data file for clean test...")
    os.remove('data/scheduling_data.json')
    print("   ✅ Cleaned up")

# Create test data
print("\n2. Creating test data...")
employees = []
emp1 = Employee("Test Employee 1", "555-0001", "test1@email.com", "server", 16.00)
emp1.add_availability("Monday", 900, 1700)
emp2 = Employee("Test Employee 2", "555-0002", "test2@email.com", "cook", 18.50)
emp2.add_availability("Tuesday", 1000, 1800)
employees = [emp1, emp2]

schedule = Schedule("2025-12-01", "2025-12-07")
shift1 = Shift("2025-12-01", 1000, 1600, ["server"])
shift2 = Shift("2025-12-02", 1100, 1800, ["cook"])
shift1.assign_employee(emp1)
shift2.assign_employee(emp2)
schedule.add_shift(shift1)
schedule.add_shift(shift2)

schedules = [schedule]

print(f"   ✅ Created {len(employees)} employees")
print(f"   ✅ Created {len(schedules)} schedules with {len(schedule.shifts)} shifts")

# Save data (simulating what main.py does)
print("\n3. Saving data to JSON...")
if not os.path.exists('data'):
    os.makedirs('data')

data_to_save = {
    'employees': [emp.to_dict() for emp in employees],
    'schedules': [sched.to_dict() for sched in schedules],
    'metadata': {
        'version': '1.0',
        'employee_count': len(employees),
        'schedule_count': len(schedules),
        'next_employee_id': Employee._next_id,
        'next_shift_id': Shift._next_id,
        'next_schedule_id': Schedule._next_id
    }
}

with open('data/scheduling_data.json', 'w') as file:
    json.dump(data_to_save, file, indent=2)

print("   ✅ Data saved to 'data/scheduling_data.json'")

# Reset class IDs to simulate new session
print("\n4. Simulating new application session...")
Employee._next_id = 10000
Shift._next_id = 1000
Schedule._next_id = 1000
print("   ✅ Reset ID counters")

# Load data (simulating what main.py does)
print("\n5. Loading data from JSON...")
with open('data/scheduling_data.json', 'r') as file:
    loaded_data = json.load(file)

loaded_employees = [Employee.from_dict(emp_data) for emp_data in loaded_data['employees']]
loaded_schedules = [Schedule.from_dict(sched_data) for sched_data in loaded_data['schedules']]

# Restore ID counters
metadata = loaded_data['metadata']
Employee._next_id = metadata['next_employee_id']
Shift._next_id = metadata['next_shift_id']
Schedule._next_id = metadata['next_schedule_id']

print(f"   ✅ Loaded {len(loaded_employees)} employees")
print(f"   ✅ Loaded {len(loaded_schedules)} schedules")

# Verify data integrity
print("\n6. Verifying data integrity...")
errors = []

# Check employees
for i, (orig, loaded) in enumerate(zip(employees, loaded_employees)):
    if orig.id != loaded.id:
        errors.append(f"Employee {i}: ID mismatch ({orig.id} vs {loaded.id})")
    if orig.name != loaded.name:
        errors.append(f"Employee {i}: Name mismatch ({orig.name} vs {loaded.name})")
    if orig.wage != loaded.wage:
        errors.append(f"Employee {i}: Wage mismatch ({orig.wage} vs {loaded.wage})")
    if len(orig.available_days_times) != len(loaded.available_days_times):
        errors.append(f"Employee {i}: Availability count mismatch")

# Check schedules
for i, (orig, loaded) in enumerate(zip(schedules, loaded_schedules)):
    if orig.id != loaded.id:
        errors.append(f"Schedule {i}: ID mismatch ({orig.id} vs {loaded.id})")
    if orig.start_date != loaded.start_date:
        errors.append(f"Schedule {i}: Start date mismatch")
    if len(orig.shifts) != len(loaded.shifts):
        errors.append(f"Schedule {i}: Shift count mismatch ({len(orig.shifts)} vs {len(loaded.shifts)})")
    
    # Check shifts
    for j, (orig_shift, loaded_shift) in enumerate(zip(orig.shifts, loaded.shifts)):
        if orig_shift.id != loaded_shift.id:
            errors.append(f"Shift {j}: ID mismatch ({orig_shift.id} vs {loaded_shift.id})")
        if orig_shift.date != loaded_shift.date:
            errors.append(f"Shift {j}: Date mismatch")
        if orig_shift.assigned_employees != loaded_shift.assigned_employees:
            errors.append(f"Shift {j}: Assigned employees mismatch")

if errors:
    print("   ❌ ERRORS FOUND:")
    for error in errors:
        print(f"      - {error}")
else:
    print("   ✅ All data verified correctly!")

# Check ID counters
print("\n7. Verifying ID counters...")
print(f"   Employee._next_id: {Employee._next_id}")
print(f"   Shift._next_id: {Shift._next_id}")
print(f"   Schedule._next_id: {Schedule._next_id}")

# Create new objects to verify IDs don't conflict
new_emp = Employee("New Employee", "555-9999", "new@email.com", "server", 15.00)
print(f"   ✅ New employee created with ID: {new_emp.id} (should be > {max(emp.id for emp in loaded_employees)})")

print("\n" + "=" * 70)
if not errors:
    print("✅ DATA PERSISTENCE TEST PASSED!")
    print("The application should properly save and load data between sessions.")
else:
    print("❌ DATA PERSISTENCE TEST FAILED!")
    print("Check the errors above.")
print("=" * 70)

print("\n💡 Next steps:")
print("   1. Run the main GUI application: python main.py")
print("   2. Add some employees and schedules")
print("   3. Close the application (it will auto-save)")
print("   4. Reopen the application - data should persist")
