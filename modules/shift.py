from datetime import datetime, date

class Shift:
    # Class variable to track the next shift ID
    _next_id = 1000
    
    def __init__(self, date, start_time, end_time, roles_required, location="Main", min_staff=1, max_staff=1):
        """
        Initialize a new Shift
        
        Args:
            date (date or str): The date of the shift (YYYY-MM-DD format if string)
            start_time (int): Start time in military format (e.g., 900 for 9:00 AM)
            end_time (int): End time in military format (e.g., 1700 for 5:00 PM)
            roles_required (str): List of required roles for this shift (e.g., "server", "cook", "manager")
            location (str): Location/department (default "Main")
            min_staff (int): Minimum number of employees needed (default 1)
            max_staff (int): Maximum number of employees allowed (default 1)
        """
        # Auto-generate shift ID
        self.id = Shift._next_id
        Shift._next_id += 1
        
        # Convert string date to date object if needed
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            self.date = date
            
        # Time information
        self.start_time = start_time
        self.end_time = end_time
        
        # Shift requirements
        if roles_required == None:
            self.roles_required = []
        else:
            self.roles_required = roles_required
        self.location = location
        self.min_staff = min_staff
        self.max_staff = max_staff
        
        # Staff assignment - list of employee IDs assigned to this shift
        self.assigned_employees = []
        
        # Status tracking
        self.is_filled = False
        self.is_published = False
        
    def assign_employee(self, employee):
        """
        Assign an employee to this shift
        
        Args:
            employee (Employee): Employee object to assign
            
        Returns:
            bool: True if assignment successful, raise ValueError() otherwise
        """
        # Check if shift is already full
        if len(self.assigned_employees) >= self.max_staff:
            raise ValueError("Shift is already full")
            
        # Check if employee has the required role
        if employee.role.lower() not in [role.lower() for role in self.roles_required]:
            # Allow managers to work any role
            if not employee.is_manager:
                raise ValueError("Employee's role does not match shift requirements")
        
        # Check if employee is available
        day_name = self.date.strftime("%A")  # Get day name (Monday, Tuesday, etc.)
        if not employee.is_available(day_name, self.start_time, self.end_time):
            raise ValueError("Employee is not available for chosen day/time")
            
        # Check if employee is already assigned to this shift
        if employee.id in self.assigned_employees:
            raise ValueError("Employee is already assigned to this shift")
            
        # Assign the employee
        self.assigned_employees.append(employee.id)
        
        # Update filled status
        self.is_filled = len(self.assigned_employees) >= self.min_staff
        
        return True
    
    def remove_employee(self, employee_id):
        """
        Remove an employee from this shift
        
        Args:
            employee_id (int): ID of employee to remove
            
        Returns:
            bool: True if removal successful, False if employee not found
        """
        if employee_id in self.assigned_employees:
            self.assigned_employees.remove(employee_id)
            self.is_filled = len(self.assigned_employees) >= self.min_staff
            return True
        return False
    
    def get_duration_hours(self):
        """
        Calculate shift duration in hours
        
        Returns:
            float: Duration in hours
        """
        # Convert military time to hours
        start_hour = self.start_time // 100 + (self.start_time % 100) / 60
        end_hour = self.end_time // 100 + (self.end_time % 100) / 60
        
        # Handle shifts that cross midnight
        if end_hour < start_hour:
            end_hour += 24
            
        return end_hour - start_hour
    
    def conflicts_with(self, other_shift):
        """
        Check if this shift conflicts with another shift (same date, overlapping times)
        
        Args:
            other_shift (Shift): Another shift to check against
            
        Returns:
            bool: True if shifts conflict, False otherwise
        """
        # Different dates = no conflict
        if self.date != other_shift.date:
            return False
            
        # Check for time overlap
        return not (self.end_time <= other_shift.start_time or 
                   self.start_time >= other_shift.end_time)
    
    def get_day_name(self):
        """Get the day of the week for this shift"""
        return self.date.strftime("%A")
    
    def format_time(self, military_time):
        """
        Convert military time to readable format
        
        Args:
            military_time (int): Time in military format (e.g., 900, 1730)
            
        Returns:
            str: Formatted time (e.g., "9:00 AM", "5:30 PM")
        """
        hours = military_time // 100
        minutes = military_time % 100
        
        if hours == 0:
            return f"12:{minutes:02d} AM"
        elif hours < 12:
            return f"{hours}:{minutes:02d} AM"
        elif hours == 12:
            return f"12:{minutes:02d} PM"
        else:
            return f"{hours-12}:{minutes:02d} PM"
    
    def to_dict(self):
        """Convert shift to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'date': self.date.isoformat(),  # Convert date to string "YYYY-MM-DD"
            'start_time': self.start_time,
            'end_time': self.end_time,
            'roles_required': self.roles_required,
            'location': self.location,
            'min_staff': self.min_staff,
            'max_staff': self.max_staff,
            'assigned_employees': self.assigned_employees,
            'is_filled': self.is_filled,
            'is_published': self.is_published
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create shift from dictionary (JSON deserialization)"""
        # Create shift with basic info
        shift = cls(
            date=data['date'],  # Will be converted to date object by __init__
            start_time=data['start_time'],
            end_time=data['end_time'],
            roles_required=data['roles_required'],
            location=data.get('location', 'Main'),
            min_staff=data.get('min_staff', 1),
            max_staff=data.get('max_staff', 1)
        )
        
        # Restore the original ID and assignments
        shift.id = data['id']
        shift.assigned_employees = data.get('assigned_employees', [])
        shift.is_filled = data.get('is_filled', False)
        shift.is_published = data.get('is_published', False)
        
        return shift
    
    def __str__(self):
        """String representation of the shift"""
        start_formatted = self.format_time(self.start_time)
        end_formatted = self.format_time(self.end_time)
        status = "✓ Filled" if self.is_filled else f"Need {self.min_staff - len(self.assigned_employees)} more"
        
        return (f"Shift {self.id}: {self.get_day_name()} {self.date} "
                f"{start_formatted}-{end_formatted} ({self.roles_required}) - {status}")
    
    def __repr__(self):
        """Developer-friendly representation"""
        return (f"Shift(id={self.id}, date='{self.date}', "
                f"time={self.start_time}-{self.end_time}, role='{self.roles_required}')")
