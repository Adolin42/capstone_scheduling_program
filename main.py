from modules.employee import Employee

def main():
    """Main function to test the scheduling software"""
    print("=== Shift Scheduling Software ===")
    
    # Create some example employees
    emp1 = Employee("John Smith", "555-1234", "john@email.com", "server", 15.50)
    emp2 = Employee("Jane Doe", "555-5678", "jane@email.com", "cook", 18.00, max_hours=35, is_minor=True)
    emp3 = Employee("Bob Johnson", "555-9999", "bob@email.com", "manager", 25.00)
    
    # Add availability
    emp1.add_availability("Monday", 900, 1700)
    emp1.add_availability("Tuesday", 1000, 1800)
    
    # Test methods
    print(f"\n{emp1}")
    print(f"Is emp1 available Monday 9-5? {emp1.is_available('Monday', 900, 1700)}")
    print(f"Is emp1 available Monday 8-4? {emp1.is_available('Monday', 800, 1600)}")
    
    print(f"\nAll employees:")
    for emp in [emp1, emp2, emp3]:
        print(f"  {emp}")

if __name__ == "__main__":
    main()
