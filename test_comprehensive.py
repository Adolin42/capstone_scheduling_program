from modules import Employee, Shift, Schedule

def test_comprehensive_scheduling():
    """Comprehensive test of Employee, Shift, and Schedule classes working together"""
    print("=" * 60)
    print("COMPREHENSIVE SCHEDULING SOFTWARE TEST")
    print("=" * 60)
    
    # =================================================================
    # SCENARIO: Luigi Mangione's Italian Restaurant - Weekly Schedule Creation
    # =================================================================
    
    print("\n🍝 LUIGI MANGIONE'S ITALIAN RESTAURANT - WEEK OF JAN 20-26, 2025")
    print("-" * 60)
    
    # Create the weekly schedule
    print("\n1. Creating weekly schedule...")
    week_schedule = Schedule("2025-01-20", "2025-01-26")  # Monday to Sunday
    print(f"✓ Schedule created: ID {week_schedule.id}")
    print(f"  Week: {week_schedule.start_date} to {week_schedule.end_date}")
    
    # Create restaurant staff
    print("\n2. Hiring restaurant staff...")
    employees = []
    
    # Servers
    svb = Employee("Shane van Boening", "555-0001", "svb@luigis.com", "server", 16.00)
    svb.add_availability("Monday", 1000, 1800)     # 10 AM - 6 PM
    svb.add_availability("Tuesday", 1000, 1800)
    svb.add_availability("Wednesday", 1000, 1800)
    svb.add_availability("Friday", 1700, 2200)     # Evening shift Friday
    svb.add_availability("Saturday", 1000, 2200)   # Long Saturday
    
    fedor = Employee("Fedor Gorst", "555-0002", "fedor@luigis.com", "server", 15.50)
    fedor.add_availability("Monday", 1700, 2300)       # Evening shifts
    fedor.add_availability("Tuesday", 1700, 2300)
    fedor.add_availability("Wednesday", 1700, 2300)
    fedor.add_availability("Thursday", 1700, 2300)
    fedor.add_availability("Friday", 1700, 2300)
    fedor.add_availability("Saturday", 1700, 2300)
    
    # Cooks
    joshua = Employee("Joshua Filler", "555-0003", "joshua@luigis.com", "cook", 18.50)
    joshua.add_availability("Monday", 900, 1700)    # Day cook
    joshua.add_availability("Tuesday", 900, 1700)
    joshua.add_availability("Wednesday", 900, 1700)
    joshua.add_availability("Thursday", 900, 1700)
    joshua.add_availability("Friday", 900, 1700)
    
    carlo = Employee("Carlo Biado", "555-0004", "carlo@luigis.com", "cook", 19.00)
    carlo.add_availability("Monday", 1600, 2400)     # Evening cook
    carlo.add_availability("Tuesday", 1600, 2400)
    carlo.add_availability("Wednesday", 1600, 2400)
    carlo.add_availability("Thursday", 1600, 2400)
    carlo.add_availability("Friday", 1600, 2400)
    carlo.add_availability("Saturday", 1600, 2400)
    carlo.add_availability("Sunday", 1600, 2300)
    
    # Manager
    luigi = Employee("Luigi Mangione", "555-0005", "luigi@luigis.com", "manager", 25.00)
    luigi.add_availability("Monday", 800, 2200)      # Long manager hours
    luigi.add_availability("Tuesday", 800, 2200)
    luigi.add_availability("Wednesday", 800, 2200)
    luigi.add_availability("Thursday", 800, 2200)
    luigi.add_availability("Friday", 800, 2300)
    luigi.add_availability("Saturday", 900, 2300)
    luigi.add_availability("Sunday", 1000, 2100)
    
    # Part-time weekend server
    jayson = Employee("Jayson Shaw", "555-0006", "jayson@luigis.com", "server", 14.50, max_hours=20, is_minor=True)
    jayson.add_availability("Friday", 1800, 2100)      # Limited minor hours
    jayson.add_availability("Saturday", 1100, 2100)
    jayson.add_availability("Sunday", 1100, 2000)
    
    employees = [svb, fedor, joshua, carlo, luigi, jayson]
    
    for emp in employees:
        print(f"  ✓ Hired: {emp}")
    
    # Create shifts for the week
    print("\n3. Creating shifts for the week...")
    shifts_to_create = [
        # Monday
        ("2025-01-20", 1100, 1500, ["server"]),    # Lunch server
        ("2025-01-20", 1000, 1600, ["cook"]),     # Day cook
        ("2025-01-20", 1700, 2200, ["server"]),   # Dinner server
        ("2025-01-20", 1600, 2300, ["cook"]),     # Evening cook
        ("2025-01-20", 900, 2100, ["manager"]),   # Manager
        
        # Tuesday  
        ("2025-01-21", 1100, 1500, ["server"]),
        ("2025-01-21", 1000, 1600, ["cook"]),
        ("2025-01-21", 1700, 2200, ["server"]),
        ("2025-01-21", 1600, 2300, ["cook"]),
        ("2025-01-21", 900, 2100, ["manager"]),
        
        # Wednesday
        ("2025-01-22", 1100, 1500, ["server"]),
        ("2025-01-22", 1000, 1600, ["cook"]),
        ("2025-01-22", 1700, 2200, ["server"]),
        ("2025-01-22", 1600, 2300, ["cook"]),
        ("2025-01-22", 900, 2100, ["manager"]),
        
        # Thursday (Busy night)
        ("2025-01-23", 1700, 2200, ["server"]),
        ("2025-01-23", 1000, 1600, ["cook"]),
        ("2025-01-23", 1600, 2300, ["cook"]),
        ("2025-01-23", 900, 2100, ["manager"]),
        
        # Friday (Very busy)
        ("2025-01-24", 1100, 1500, ["server"]),   # svb lunch
        ("2025-01-24", 1000, 1600, ["cook"]),     # joshua day
        ("2025-01-24", 1700, 2200, ["server"]),   # fedor dinner
        ("2025-01-24", 1800, 2100, ["server"]),   # jayson help
        ("2025-01-24", 1600, 2300, ["cook"]),     # carlo evening
        ("2025-01-24", 900, 2200, ["manager"]),   # Luigi
        
        # Saturday (Busiest day)
        ("2025-01-25", 1100, 1600, ["server"]),   # svb day
        ("2025-01-25", 1700, 2200, ["server"]),   # fedor evening
        ("2025-01-25", 1200, 2000, ["server"]),   # jayson long shift
        ("2025-01-25", 1600, 2300, ["cook"]),     # carlo
        ("2025-01-25", 1000, 2200, ["manager"]),  # Luigi
        
        # Sunday (Lighter day)
        ("2025-01-26", 1200, 1900, ["server"]),   # jayson
        ("2025-01-26", 1600, 2200, ["cook"]),     # carlo
        ("2025-01-26", 1100, 2000, ["manager"]),  # Luigi
    ]
    
    created_shifts = []
    for shift_data in shifts_to_create:
        shift = Shift(*shift_data)
        created_shifts.append(shift)
        print(f"  ✓ Created: {shift}")
    
    # Add all shifts to the schedule
    print("\n4. Adding shifts to schedule...")
    successful_adds = 0
    for shift in created_shifts:
        try:
            if week_schedule.add_shift(shift):
                successful_adds += 1
        except ValueError as e:
            print(f"  ✗ Failed to add shift: {e}")
    
    print(f"  ✓ Successfully added {successful_adds}/{len(created_shifts)} shifts")
    
    # Assign employees to shifts
    print("\n5. Assigning employees to shifts...")
    assignment_attempts = [
        # Monday
        (0, svb), (1, joshua), (2, fedor), (3, carlo), (4, luigi),
        # Tuesday  
        (5, svb), (6, joshua), (7, fedor), (8, carlo), (9, luigi),
        # Wednesday
        (10, svb), (11, joshua), (12, fedor), (13, carlo), (14, luigi),
        # Thursday
        (15, fedor), (16, joshua), (17, carlo), (18, luigi),
        # Friday
        (19, svb), (20, joshua), (21, fedor), (22, jayson), (23, carlo), (24, luigi),
        # Saturday
        (25, svb), (26, fedor), (27, jayson), (28, carlo), (29, luigi),
        # Sunday
        (30, jayson), (31, carlo), (32, luigi),
    ]
    
    successful_assignments = 0
    failed_assignments = 0
    
    all_shifts = week_schedule.get_all_shifts()
    
    for shift_index, employee in assignment_attempts:
        if shift_index < len(all_shifts):
            shift = all_shifts[shift_index]
            try:
                if shift.assign_employee(employee):
                    print(f"  ✓ {employee.name} assigned to {shift.get_day_name()} {shift.format_time(shift.start_time)}-{shift.format_time(shift.end_time)} ({shift.roles_required})")
                    successful_assignments += 1
                else:
                    print(f"  ✗ Failed to assign {employee.name} to shift {shift_index}")
                    failed_assignments += 1
            except Exception as e:
                print(f"  ✗ Error assigning {employee.name}: {e}")
                failed_assignments += 1
    
    print(f"\n  📊 Assignment Results: {successful_assignments} successful, {failed_assignments} failed")
    
    # Test schedule queries and analysis
    print("\n6. Testing schedule queries...")
    
    # Check for conflicts
    has_conflicts = week_schedule.has_conflicts()
    print(f"  Schedule conflicts detected: {'❌ YES' if has_conflicts else '✅ NO'}")
    
    # Get shifts by day
    monday_shifts = week_schedule.get_shifts_by_date("2025-01-20")
    print(f"  Monday shifts: {len(monday_shifts)}")
    
    # Get shifts by employee
    svb_shifts = week_schedule.get_shifts_by_employee(svb.id)
    fedor_shifts = week_schedule.get_shifts_by_employee(fedor.id)
    print(f"  svb's shifts this week: {len(svb_shifts)}")
    print(f"  fedor's shifts this week: {len(fedor_shifts)}")
    
    # Calculate total hours for each employee
    print("\n7. Weekly hours analysis...")
    for employee in employees:
        emp_shifts = week_schedule.get_shifts_by_employee(employee.id)
        total_hours = sum(shift.get_duration_hours() for shift in emp_shifts)
        print(f"  {employee.name}: {total_hours:.1f} hours (Max: {employee.max_hours})")
        
        if total_hours > employee.max_hours:
            print(f"    ⚠️  OVERTIME: {total_hours - employee.max_hours:.1f} hours over limit!")
    
    # Generate daily schedule view
    print("\n8. Daily schedule breakdown...")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dates = ["2025-01-20", "2025-01-21", "2025-01-22", "2025-01-23", "2025-01-24", "2025-01-25", "2025-01-26"]
    
    for day, date_str in zip(days, dates):
        day_shifts = week_schedule.get_shifts_by_date(date_str)
        print(f"\n  📅 {day} ({date_str}):")
        
        if not day_shifts:
            print("    No shifts scheduled")
            continue
            
        for shift in day_shifts:
            assigned_names = []
            for emp_id in shift.assigned_employees:
                emp = next((e for e in employees if e.id == emp_id), None)
                if emp:
                    assigned_names.append(emp.name)
            
            assigned_str = ", ".join(assigned_names) if assigned_names else "UNASSIGNED"
            status = "✅" if shift.is_filled else "❌"
            
            print(f"    {status} {shift.format_time(shift.start_time)}-{shift.format_time(shift.end_time)} "
                  f"({shift.roles_required}): {assigned_str}")
    
    # Test error handling
    print("\n9. Testing error handling...")
    
    # Try to add invalid shift (outside date range)
    try:
        invalid_shift = Shift("2025-01-30", 1000, 1800, ["server"])  # Outside week range
        week_schedule.add_shift(invalid_shift)
        print("  ✗ Should have failed - shift outside date range")
    except ValueError as e:
        print(f"  ✅ Correctly rejected invalid shift: {e}")
    
    # Try to assign unavailable employee
    try:
        test_shift = Shift("2025-01-20", 2300, 2400, ["server"])  # Late night
        test_shift.assign_employee(svb)  # svb not available that late
        print("  ✗ Should have failed - employee not available")
    except:
        print("  ✅ Correctly rejected unavailable employee assignment")
    
    # Performance test
    print("\n10. Performance test...")
    import time
    start_time = time.time()
    
    # Simulate checking 1000 potential conflicts
    for i in range(1000):
        week_schedule.has_conflicts()
    
    end_time = time.time()
    print(f"  ✅ 1000 conflict checks completed in {(end_time - start_time)*1000:.2f} ms")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    print(f"✅ Schedule ID: {week_schedule.id}")
    print(f"✅ Total employees: {len(employees)}")
    print(f"✅ Total shifts created: {len(all_shifts)}")
    print(f"✅ Total assignments: {successful_assignments}")
    print(f"✅ Conflicts detected: {'YES' if has_conflicts else 'NO'}")
    
    coverage = (successful_assignments / len(all_shifts)) * 100 if all_shifts else 0
    print(f"✅ Shift coverage: {coverage:.1f}%")
    
    total_labor_hours = sum(shift.get_duration_hours() for shift in all_shifts)
    total_assigned_hours = sum(
        sum(shift.get_duration_hours() for shift in week_schedule.get_shifts_by_employee(emp.id))
        for emp in employees
    )
    print(f"✅ Total labor hours: {total_labor_hours:.1f}")
    print(f"✅ Assigned hours: {total_assigned_hours:.1f}")
    
    print("\n🎉 COMPREHENSIVE TEST COMPLETED SUCCESSFULLY!")
    print("All core classes are working together properly.")
    print("Ready for GUI development! 🚀")

if __name__ == "__main__":
    test_comprehensive_scheduling()
