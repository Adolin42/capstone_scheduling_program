class Employee:
    # Class variable to track the next ID (shared by all instances)
    _next_id = 10000
    
    def __init__(self, name, phone_number, email, role, wage, max_hours=40, min_hours=0, is_minor=False):
        """
        Initialize a new Employee
        
        Args:
            name (str): Employee's full name
            phone_number (str): Phone number
            email (str): Email address
            role (str): Job role (e.g., "server", "cook", "host", "manager")
            wage (float): Hourly wage
            max_hours (int): Maximum hours per week (default 40)
            min_hours (int): Minimum hours per week (default 0)
            is_minor (bool): Whether employee is under 18 (default False)
        """
        # Auto-generate 5-digit ID
        self.id = Employee._next_id
        Employee._next_id += 1
        
        # Basic information
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.role = role
        self.wage = wage
        
        # Work constraints
        self.max_hours = max_hours
        self.min_hours = min_hours
        self.is_minor = is_minor
        
        # Determine manager/admin status based on role
        self.is_manager = role.lower() in ["manager", "assistant manager"]
        self.is_admin = role.lower() in ["admin", "owner", "general manager"]
        
        # Available times: List of tuples (day, start_time, end_time)
        # Example: [("Monday", 900, 1700), ("Tuesday", 1000, 1800)]
        # Times in military format as integers (900 = 9:00 AM, 1700 = 5:00 PM)
        self.available_days_times = []
    
    def add_availability(self, day, start_time, end_time):
        """
        Add available time slot for the employee
        
        Args:
            day (str): Day of the week (e.g., "Monday")
            start_time (int): Start time in military format (e.g., 900 for 9:00 AM)
            end_time (int): End time in military format (e.g., 1700 for 5:00 PM)
        """
        self.available_days_times.append((day, start_time, end_time))
    
    def is_available(self, day, start_time, end_time):
        """
        Check if employee is available during specified time
        
        Args:
            day (str): Day of the week
            start_time (int): Shift start time in military format
            end_time (int): Shift end time in military format
            
        Returns:
            bool: True if available, False otherwise
        """
        for avail_day, avail_start, avail_end in self.available_days_times:
            if (avail_day.lower() == day.lower() and 
                avail_start <= start_time and 
                avail_end >= end_time):
                return True
        return False
    
    def __str__(self):
        """String representation of the employee"""
        return f"Employee {self.id}: {self.name} ({self.role}) - ${self.wage}/hr"
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Employee(id={self.id}, name='{self.name}', role='{self.role}')"
