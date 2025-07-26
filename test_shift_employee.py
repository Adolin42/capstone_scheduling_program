from modules import Employee, Shift
from datetime import date

def test_shift_employee_integration():
    """Test how Shift and Employee classes work together"""
    print("=== Testing Shift and Employee Integration ===\n")
    
    # Create some test employees
    print("1. Creating test employees:")
    server1 = Employee("Alice Johnson", "555-0001", "alice@restaurant.com", "server", 16.00)
    server2 = Employee("Bob Smith", "555-0002", "bob@restaurant.com", "server", 15.50)
    cook1 = Employee("Charlie Brown", "555-0003", "charlie@restaurant.com", "cook", 18.00)
    manager1 = Employee("Diana Lee", "555-0004", "diana@restaurant.com", "manager", 25.00)
    
    print(f"  {server1}")
    print(f"  {server2}")
    print(f"  {cook1}")
    print(f"  {manager1}")
    
    # Set availability for employees
    print("\n2. Setting employee availability:")
    # Alice available Monday 9-5
    server1.add_availability("Monday", 900, 1700)
    print(f"  {server1.name}: Monday 9:00 AM - 5:00 PM")
    
    # Bob available Monday 2-10
    server2.add_availability("Monday", 1400, 2200)
    print(f"  {server2.name}: Monday 2:00 PM - 10:00 PM")
    
    # Charlie available Monday 10-6
    cook1.add_availability("Monday", 1000, 1800)
    print(f"  {cook1.name}: Monday 10:00 AM - 6:00 PM")
    
    # Manager available Monday all day
    manager1.add_availability("Monday", 800, 2300)
    print(f"  {manager1.name}: Monday 8:00 AM - 11:00 PM")
    
    # Create some test shifts
    print("\n3. Creating test shifts:")
    lunch_shift = Shift("2025-01-27", 1100, 1500, "server")  # Monday lunch
    dinner_shift = Shift("2025-01-27", 1700, 2100, "server")  # Monday dinner
    cook_shift = Shift("2025-01-27", 1000, 1800, "cook")     # Monday cook
    manager_shift = Shift("2025-01-27", 900, 1700, "manager") # Monday manager
    
    print(f"  {lunch_shift}")
    print(f"  {dinner_shift}")
    print(f"  {cook_shift}")
    print(f"  {manager_shift}")
    
    # Test shift assignments
    print("\n4. Testing shift assignments:")
    
    # Try to assign Alice to lunch shift (should work)
    print(f"\nTrying to assign {server1.name} to lunch shift...")
    result = lunch_shift.assign_employee(server1)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Shift status: {lunch_shift}")
    
    # Try to assign Bob to lunch shift (should fail - not available at 11-3)
    print(f"\nTrying to assign {server2.name} to lunch shift...")
    result = lunch_shift.assign_employee(server2)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Reason: Bob is only available 2-10 PM, lunch shift is 11 AM-3 PM")
    
    # Try to assign Bob to dinner shift (should work)
    print(f"\nTrying to assign {server2.name} to dinner shift...")
    result = dinner_shift.assign_employee(server2)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Shift status: {dinner_shift}")
    
    # Try to assign Charlie to cook shift (should work)
    print(f"\nTrying to assign {cook1.name} to cook shift...")
    result = cook_shift.assign_employee(cook1)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Shift status: {cook_shift}")
    
    # Try to assign server to cook shift (should fail - wrong role)
    print(f"\nTrying to assign {server1.name} (server) to cook shift...")
    result = cook_shift.assign_employee(server1)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Reason: {server1.name} is a server, but cook shift requires a cook")
    
    # Try to assign manager to cook shift (should work - managers can work any role)
    print(f"\nTrying to assign {manager1.name} (manager) to cook shift...")
    # First remove Charlie to make room
    cook_shift.remove_employee(cook1.id)
    result = cook_shift.assign_employee(manager1)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    print(f"Reason: Managers can work any role")
    print(f"Shift status: {cook_shift}")
    
    # Test shift conflicts
    print("\n5. Testing shift conflicts:")
    overlap_shift = Shift("2025-01-27", 1200, 1600, "server")  # Overlaps with lunch
    print(f"New shift: {overlap_shift}")
    print(f"Does it conflict with lunch shift? {lunch_shift.conflicts_with(overlap_shift)}")
    print(f"Lunch: 11:00 AM - 3:00 PM")
    print(f"New:   12:00 PM - 4:00 PM")
    print(f"Overlap: 12:00 PM - 3:00 PM")
    
    # Test shift duration
    print("\n6. Testing shift duration calculations:")
    print(f"Lunch shift duration: {lunch_shift.get_duration_hours()} hours")
    print(f"Dinner shift duration: {dinner_shift.get_duration_hours()} hours")
    print(f"Cook shift duration: {cook_shift.get_duration_hours()} hours")
    
    # Test time formatting
    print("\n7. Testing time formatting:")
    print(f"900 military time = {lunch_shift.format_time(900)}")
    print(f"1500 military time = {lunch_shift.format_time(1500)}")
    print(f"1730 military time = {lunch_shift.format_time(1730)}")
    print(f"2200 military time = {lunch_shift.format_time(2200)}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_shift_employee_integration()
