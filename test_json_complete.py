import json
from modules.employee import Employee
from modules.shift import Shift
from modules.schedule import Schedule

print("=" * 60)
print("COMPLETE JSON SERIALIZATION TEST")
print("=" * 60)

# Create employees
print("\n1. Creating employees...")
emp1 = Employee("Alice Johnson", "555-0001", "alice@email.com", "server", 16.00)
emp1.add_availability("Monday", 900, 1700)
emp1.add_availability("Tuesday", 1000, 1800)

emp2 = Employee("Bob Smith", "555-0002", "bob@email.com", "cook", 18.50)
emp2.add_availability("Monday", 1000, 1800)

emp3 = Employee("Charlie Manager", "555-0003", "charlie@email.com", "manager", 25.00)
emp3.add_availability("Monday", 800, 2000)

employees = [emp1, emp2, emp3]
print(f"✅ Created {len(employees)} employees")

# Create schedule with shifts
print("\n2. Creating schedule and shifts...")
schedule = Schedule("2025-12-01", "2025-12-07")  # Mon-Sun

shift1 = Shift("2025-12-01", 1000, 1600, ["server"])
shift2 = Shift("2025-12-01", 1100, 1800, ["cook"])
shift3 = Shift("2025-12-01", 900, 1700, ["manager"])

# Assign employees to shifts
shift1.assign_employee(emp1)
shift2.assign_employee(emp2)
shift3.assign_employee(emp3)

schedule.add_shift(shift1)
schedule.add_shift(shift2)
schedule.add_shift(shift3)

print(f"✅ Created schedule with {len(schedule.shifts)} shifts")

# Save everything to JSON
print("\n3. Saving to JSON...")
data_to_save = {
    "employees": [emp.to_dict() for emp in employees],
    "schedules": [schedule.to_dict()],
    "metadata": {
        "version": "1.0",
        "employee_count": len(employees),
        "schedule_count": 1
    }
}

with open("complete_data.json", "w") as file:
    json.dump(data_to_save, file, indent=2)

print("✅ Saved to 'complete_data.json'")

# Load everything back
print("\n4. Loading from JSON...")
with open("complete_data.json", "r") as file:
    loaded_data = json.load(file)

loaded_employees = [Employee.from_dict(emp_data) for emp_data in loaded_data["employees"]]
loaded_schedules = [Schedule.from_dict(sched_data) for sched_data in loaded_data["schedules"]]

print(f"✅ Loaded {len(loaded_employees)} employees")
print(f"✅ Loaded {len(loaded_schedules)} schedules")

# Verify data integrity
print("\n5. Verifying data...")
print("\nEmployees:")
for emp in loaded_employees:
    print(f"  - {emp}")
    print(f"    Availability: {len(emp.available_days_times)} slots")

print("\nSchedules:")
for sched in loaded_schedules:
    print(f"  - Schedule {sched.id}: {sched.start_date} to {sched.end_date}")
    print(f"    Total shifts: {len(sched.shifts)}")
    for shift in sched.shifts:
        print(f"    - {shift}")
        print(f"      Assigned: {len(shift.assigned_employees)} employee(s)")

print("\n" + "=" * 60)
print("✅ ALL DATA SUCCESSFULLY SAVED AND LOADED!")
print("=" * 60)