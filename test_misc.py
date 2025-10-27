from modules.employee import Employee
from modules.shift import Shift
from modules.schedule import Schedule
import json

def main():
    """Main application entry point"""
    # Save an employee to dictionary
    emp1 = Employee("Alice", "555-1234", "alice@email.com", "server", 16.00)
    emp1.add_availability("Monday", 900, 1700)

    # Convert to dict (instance method - called on emp1)
    data = emp1.to_dict()

    # Later... load employee from dictionary
    # Class method - called on Employee class itself, creates new object
    emp2 = Employee.from_dict(data)

    # emp1 and emp2 should have the same data!
    print(emp1.name)  # Alice
    print(emp2.name)  # Alice
    print(emp1.id == emp2.id)  # True


if __name__ == "__main__":
    main()