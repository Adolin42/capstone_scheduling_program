from datetime import datetime, date
# from .shift import Shift  # Import removed to avoid circular dependency
# from .employee import Employee

class Schedule:
    
    # Class variable to track the next schedule ID
    _next_id = 1000
    
    def __init__(self, start_date, end_date, shifts=None):
        """
        Initialize a new Schedule
        
        Args:
            start_date (date or str): The start date, should be Monday (YYYY-MM-DD format if string)
            end_date (date or str): The end date, should be Sunday (YYY-MM-DD format if string)
            shifts (list of Shift objects):
        """

        # Auto-generate schedule ID
        self.id = Schedule._next_id
        Schedule._next_id += 1

        # Convert string date to date object if needed
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            self.start_date = start_date
        
        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            self.end_date = end_date

        # Handle the shifts list
        if shifts is None:
            self.shifts = []
        else:
            self.shifts = shifts

    # METHODS
    def add_shift(self, shift):
        """
        Add a shift to the schedule

        Args:
            shift (Shift object): The shift object being added to the schedule
        
        Returns:
            bool: True if shift is valid, raise ValueError otherwise
        """
        if shift is None:
            raise ValueError("Cannot add None shift to schedule")
        
        # Check if shift date is within schedule range
        if shift.date < self.start_date or shift.date > self.end_date:
            raise ValueError(f"Shift date {shift.date} is outside schedule range")
        
        self.shifts.append(shift)
        return True
    
    def get_all_shifts(self):
        """Return all shifts in the schedule"""
        return self.shifts
    
    def get_shifts_by_date(self, date):
        """
        Get all shifts for a specific date

        Args:
            date (date or str): The date to search for
        
        Returns:
            list: List of shifts on that date
        """
        # Convert string to date if needed
        if isinstance(date, str):
            search_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            search_date = date
        
        return [shift for shift in self.shifts if shift.date == search_date]
    
    def get_shifts_by_employee(self, employee_id):
        """
        Get all shifts assigned to a specific employee

        Args: 
            employee_id (int): The employee ID to search for

        Returns:
            list: List of shifts assigned to that employee
        """
        return [shift for shift in self.shifts if employee_id in shift.assigned_employees]
    
    def has_conflicts(self):
        """
        Check if any shifts in the schedule conflict with each other

        Returns:
            bool: True if conflicts exist, False otherwise
        """
        for i, shift1 in enumerate(self.shifts):
            for shift2 in self.shifts[i+1:]:
                if shift1.conflicts_with(shift2):
                    return True
        return False
    
    def calculate_payroll(self, employees_list):
        """
        Calculate total payroll cost for entire schedule

        Args:
            employees_list: List of all Employee objects
        
        Returns:
            float: Total payroll cost for all shifts
        """

        total_cost = 0.0

        for shift in self.shifts:
            shift_cost = shift.calculate_payroll(employees_list)
            total_cost += shift_cost
        
        return total_cost
    
    def to_dict(self):
        """Convert schedule to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat(),  # Convert date to string
            'end_date': self.end_date.isoformat(),      # Convert date to string
            'shifts': [shift.to_dict() for shift in self.shifts]  # Recursively convert shifts
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create schedule from dictionary (JSON deserialization)"""
        # Create schedule without shifts first
        schedule = cls(
            start_date=data['start_date'],
            end_date=data['end_date'],
            shifts=None
        )
        
        # Restore the original ID
        schedule.id = data['id']
        
        # Import Shift here to avoid circular dependency
        from .shift import Shift
        
        # Recursively recreate shift objects
        schedule.shifts = [Shift.from_dict(shift_data) for shift_data in data.get('shifts', [])]
        
        return schedule