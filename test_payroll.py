# test_payroll.py
from modules.employee import Employee
from modules.shift import Shift
from modules.schedule import Schedule

# Create employees with different wages
emp1 = Employee("Alice", "555-0001", "alice@email.com", "server", 16.00)
emp2 = Employee("Bob", "555-0002", "bob@email.com", "cook", 20.00)
emp1.add_availability("Monday", 900, 1800)
emp2.add_availability("Monday", 900, 1800)

employees = [emp1, emp2]

# Create shifts
shift1 = Shift("2025-12-01", 1000, 1400, ["server"])  # 4 hours
shift2 = Shift("2025-12-01", 1000, 1800, ["cook"])    # 8 hours

shift1.assign_employee(emp1)
shift2.assign_employee(emp2)

# Calculate costs
cost1 = shift1.calculate_payroll(employees)
cost2 = shift2.calculate_payroll(employees)

print(f"Shift 1 (4 hours @ $16/hr): ${cost1:.2f}")  # Should be $64.00
print(f"Shift 2 (8 hours @ $20/hr): ${cost2:.2f}")  # Should be $160.00

# Test schedule total
schedule = Schedule("2025-12-01", "2025-12-07")
schedule.add_shift(shift1)
schedule.add_shift(shift2)

total = schedule.calculate_payroll(employees)
print(f"Schedule total: ${total:.2f}")  # Should be $224.00