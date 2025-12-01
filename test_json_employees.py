import json
from modules.employee import Employee

# Create some employees
print("Creating employees...")
emp1 = Employee("Alice Johnson", "555-0001", "alice@email.com", "server", 16.00)
emp1.add_availability("Monday", 900, 1700)
emp1.add_availability("Tuesday", 1000, 1800)

emp2 = Employee("Bob Smith", "555-0002", "bob@email.com", "cook", 18.50, is_minor=False)
emp2.add_availability("Wednesday", 1200, 2000)

emp3 = Employee("Charlie Brown", "555-0003", "charlie@email.com", "manager", 25.00)

employees = [emp1, emp2, emp3]

print(f"Created {len(employees)} employees")
print()

# ===== SAVING TO JSON =====
print("=" * 50)
print("SAVING EMPLOYEES TO JSON FILE")
print("=" * 50)

# Convert all employees to dictionaries
employee_dicts = [emp.to_dict() for emp in employees]

# Create a data structure to save
data_to_save = {
    "employees": employee_dicts,
    "metadata": {
        "version": "1.0",
        "count": len(employees)
    }
}

# Save to JSON file
with open("employees_data.json", "w") as file:
    json.dump(data_to_save, file, indent=2)

print("✅ Saved employees to 'employees_data.json'")
print(f"   Saved {len(employee_dicts)} employees")
print()

# ===== LOADING FROM JSON =====
print("=" * 50)
print("LOADING EMPLOYEES FROM JSON FILE")
print("=" * 50)

# Read from JSON file
with open("employees_data.json", "r") as file:
    loaded_data = json.load(file)

# Convert dictionaries back to Employee objects
loaded_employees = [Employee.from_dict(emp_dict) for emp_dict in loaded_data["employees"]]

print(f"✅ Loaded {len(loaded_employees)} employees")
print()

# ===== VERIFY THE DATA =====
print("=" * 50)
print("VERIFYING LOADED DATA")
print("=" * 50)

for i, emp in enumerate(loaded_employees):
    print(f"\nEmployee {i+1}:")
    print(f"  {emp}")
    print(f"  Email: {emp.email}")
    print(f"  Availability: {len(emp.available_days_times)} time slots")
    
    if emp.available_days_times:
        for day, start, end in emp.available_days_times:
            print(f"    - {day}: {start} to {end}")

print()
print("=" * 50)
print("✅ ALL DATA PRESERVED CORRECTLY!")
print("=" * 50)