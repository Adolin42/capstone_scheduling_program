"""
Shift Scheduling Software - Main GUI Application
Author: Ptolemy Linden
Description: Professional scheduling software with Tkinter GUI
"""

import tkinter as tk # basic Tkinter widgets (Label, Button, etc.)
from tkinter import ttk, messagebox, simpledialog # themed widgets (sexy, sleek, modern widgets)
from datetime import datetime, date, timedelta
import json
import os

from modules.employee import Employee
from modules.shift import Shift
from modules.schedule import Schedule


class SchedulingApp:
    def __init__(self, root):
        self.root = root # Main window passed from main()
        self.root.title("Luigi Mangione's Italian Restaurant - Shift Scheduling Software")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configure style
        self.setup_styles()
        
        # Data storage
        self.employees = []
        self.schedules = []
        self.current_schedule = None
        
        # Load data if exists
        self.load_data()
        
        # Create GUI
        self.setup_gui()
        
        # Load sample data if no data exists
        if not self.employees:
            self.load_sample_data()

    def setup_styles(self):
        """Configure ttk styles for a professional look"""
        style = ttk.Style()
        
        # Configure colors and fonts
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    def setup_gui(self):
        """Create the main GUI layout"""
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="🍝 Luigi Mangione's Italian Restaurant - Shift Scheduling System", 
                 style='Title.TLabel').pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_employees_tab()
        self.create_schedule_tab()
        self.create_shifts_tab()
        
        # Status bar
        self.create_status_bar()

    def create_dashboard_tab(self):
        """Create dashboard/overview tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Quick Statistics", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        # Stats variables
        self.stats_employees = tk.StringVar(value="0")
        self.stats_schedules = tk.StringVar(value="0")
        self.stats_shifts = tk.StringVar(value="0")
        
        # Stats display
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x')
        
        ttk.Label(stats_grid, text="👥 Total Employees:").grid(row=0, column=0, sticky='w', padx=5)
        ttk.Label(stats_grid, textvariable=self.stats_employees, style='Heading.TLabel').grid(row=0, column=1, sticky='w', padx=5)
        
        ttk.Label(stats_grid, text="📅 Active Schedules:").grid(row=0, column=2, sticky='w', padx=20)
        ttk.Label(stats_grid, textvariable=self.stats_schedules, style='Heading.TLabel').grid(row=0, column=3, sticky='w', padx=5)
        
        ttk.Label(stats_grid, text="⏰ Total Shifts:").grid(row=0, column=4, sticky='w', padx=20)
        ttk.Label(stats_grid, textvariable=self.stats_shifts, style='Heading.TLabel').grid(row=0, column=5, sticky='w', padx=5)
        
        # Recent activity frame
        activity_frame = ttk.LabelFrame(dashboard_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Activity listbox with scrollbar
        activity_scroll_frame = ttk.Frame(activity_frame)
        activity_scroll_frame.pack(fill='both', expand=True)
        
        self.activity_listbox = tk.Listbox(activity_scroll_frame, font=('Arial', 10))
        activity_scrollbar = ttk.Scrollbar(activity_scroll_frame, orient='vertical', command=self.activity_listbox.yview)
        self.activity_listbox.config(yscrollcommand=activity_scrollbar.set)
        
        self.activity_listbox.pack(side='left', fill='both', expand=True)
        activity_scrollbar.pack(side='right', fill='y')
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(dashboard_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack()
        
        ttk.Button(actions_grid, text="➕ Add Employee", 
                  command=self.show_add_employee_dialog, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(actions_grid, text="📅 New Schedule", 
                  command=self.create_new_schedule, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(actions_grid, text="⏰ Add Shift", 
                  command=self.show_add_shift_dialog, style='Action.TButton').pack(side='left', padx=5)

    def create_employees_tab(self):
        """Create employee management tab"""
        employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(employees_frame, text="👥 Employees")
        
        # Employee list frame
        list_frame = ttk.LabelFrame(employees_frame, text="Employee List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Employee treeview
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Name', 'Role', 'Wage', 'Max Hours', 'Status')
        self.employee_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.employee_tree.heading(col, text=col)
            self.employee_tree.column(col, width=100)
        
        # Scrollbars
        emp_v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.employee_tree.yview)
        emp_h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.employee_tree.xview)
        self.employee_tree.config(yscrollcommand=emp_v_scroll.set, xscrollcommand=emp_h_scroll.set)
        
        self.employee_tree.pack(side='left', fill='both', expand=True)
        emp_v_scroll.pack(side='right', fill='y')
        emp_h_scroll.pack(side='bottom', fill='x')
        
        # Employee actions frame
        emp_actions_frame = ttk.Frame(employees_frame)
        emp_actions_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(emp_actions_frame, text="➕ Add Employee", 
                  command=self.show_add_employee_dialog).pack(side='left', padx=5)
        ttk.Button(emp_actions_frame, text="✏️ Edit Employee", 
                  command=self.edit_selected_employee).pack(side='left', padx=5)
        ttk.Button(emp_actions_frame, text="🗑️ Delete Employee", 
                  command=self.delete_selected_employee).pack(side='left', padx=5)
        ttk.Button(emp_actions_frame, text="👁️ View Details", 
                  command=self.view_employee_details).pack(side='left', padx=5)

    def create_schedule_tab(self):
        """Create schedule management tab"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="📅 Schedules")
        
        # Schedule selection frame
        selection_frame = ttk.LabelFrame(schedule_frame, text="Schedule Selection", padding=10)
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(selection_frame, text="Current Schedule:").pack(side='left', padx=5)
        
        self.schedule_var = tk.StringVar()
        self.schedule_combo = ttk.Combobox(selection_frame, textvariable=self.schedule_var, 
                                          state='readonly', width=30)
        self.schedule_combo.pack(side='left', padx=5)
        self.schedule_combo.bind('<<ComboboxSelected>>', self.on_schedule_selected)
        
        ttk.Button(selection_frame, text="📅 New Schedule", 
                  command=self.create_new_schedule).pack(side='left', padx=10)
        ttk.Button(selection_frame, text="🗑️ Delete Schedule", 
                  command=self.delete_current_schedule).pack(side='left', padx=5)
        
        # Schedule view frame
        view_frame = ttk.LabelFrame(schedule_frame, text="Weekly Schedule View", padding=10)
        view_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Days of week tabs
        self.schedule_notebook = ttk.Notebook(view_frame)
        self.schedule_notebook.pack(fill='both', expand=True)
        
        self.day_frames = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            day_frame = ttk.Frame(self.schedule_notebook)
            self.schedule_notebook.add(day_frame, text=day)
            self.day_frames[day] = day_frame
            
            # Create day view
            self.create_day_view(day_frame, day)

    def create_day_view(self, parent, day):
        """Create view for a specific day"""
        # Day shifts listbox
        shifts_frame = ttk.LabelFrame(parent, text=f"{day} Shifts", padding=10)
        shifts_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Shifts treeview for this day
        columns = ('Time', 'Role', 'Assigned', 'Status')
        day_tree = ttk.Treeview(shifts_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            day_tree.heading(col, text=col)
            day_tree.column(col, width=150)
        
        day_tree.pack(fill='both', expand=True)
        
        # Store reference to day tree
        setattr(self, f'{day.lower()}_tree', day_tree)

    def create_shifts_tab(self):
        """Create shift management tab"""
        shifts_frame = ttk.Frame(self.notebook)
        self.notebook.add(shifts_frame, text="⏰ Shifts")
        
        # Shift list frame
        shift_list_frame = ttk.LabelFrame(shifts_frame, text="All Shifts", padding=10)
        shift_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Shifts treeview
        tree_frame = ttk.Frame(shift_list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Date', 'Day', 'Time', 'Role', 'Assigned', 'Status')
        self.shifts_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.shifts_tree.heading(col, text=col)
            self.shifts_tree.column(col, width=100)
        
        # Scrollbars for shifts
        shift_v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.shifts_tree.yview)
        self.shifts_tree.config(yscrollcommand=shift_v_scroll.set)
        
        self.shifts_tree.pack(side='left', fill='both', expand=True)
        shift_v_scroll.pack(side='right', fill='y')
        
        # Shift actions
        shift_actions_frame = ttk.Frame(shifts_frame)
        shift_actions_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(shift_actions_frame, text="➕ Add Shift", 
                  command=self.show_add_shift_dialog).pack(side='left', padx=5)
        ttk.Button(shift_actions_frame, text="✏️ Edit Shift", 
                  command=self.edit_selected_shift).pack(side='left', padx=5)
        ttk.Button(shift_actions_frame, text="👤 Assign Employee", 
                  command=self.assign_employee_to_shift).pack(side='left', padx=5)
        ttk.Button(shift_actions_frame, text="🗑️ Delete Shift", 
                  command=self.delete_selected_shift).pack(side='left', padx=5)

    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', side='bottom')
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.status_frame, textvariable=self.status_var, 
                 style='Status.TLabel').pack(side='left', padx=10, pady=2)
        
        # Current schedule indicator
        self.current_schedule_var = tk.StringVar(value="No schedule selected")
        ttk.Label(self.status_frame, textvariable=self.current_schedule_var, 
                 style='Status.TLabel').pack(side='right', padx=10, pady=2)

    def show_add_employee_dialog(self):
        """Show dialog to add new employee"""
        dialog = EmployeeDialog(self.root, "Add Employee")
        if dialog.result:
            emp_data = dialog.result
            try:
                employee = Employee(
                    name=emp_data['name'],
                    phone_number=emp_data['phone'],
                    email=emp_data['email'],
                    role=emp_data['role'],
                    wage=float(emp_data['wage']),
                    max_hours=int(emp_data['max_hours']),
                    is_minor=emp_data['is_minor']
                )
                self.employees.append(employee)
                self.refresh_employee_list()
                self.update_stats()
                self.add_activity(f"Added employee: {employee.name}")
                self.status_var.set(f"Employee {employee.name} added successfully")
                self.save_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add employee: {str(e)}")

    def edit_selected_employee(self):
        """Edit selected employee"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to edit")
            return
        
        # Get employee data from tree
        item = self.employee_tree.item(selection[0])
        emp_id = int(item['values'][0])
        
        # Find employee object
        employee = next((emp for emp in self.employees if emp.id == emp_id), None)
        if not employee:
            messagebox.showerror("Error", "Employee not found")
            return
        
        # Show edit dialog with current data
        dialog = EmployeeDialog(self.root, "Edit Employee", employee)
        if dialog.result:
            emp_data = dialog.result
            try:
                # Update employee data
                employee.name = emp_data['name']
                employee.phone_number = emp_data['phone']
                employee.email = emp_data['email']
                employee.role = emp_data['role']
                employee.wage = float(emp_data['wage'])
                employee.max_hours = int(emp_data['max_hours'])
                employee.is_minor = emp_data['is_minor']
                
                self.refresh_employee_list()
                self.add_activity(f"Updated employee: {employee.name}")
                self.status_var.set(f"Employee {employee.name} updated successfully")
                self.save_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update employee: {str(e)}")

    def delete_selected_employee(self):
        """Delete selected employee"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to delete")
            return
        
        item = self.employee_tree.item(selection[0])
        emp_id = int(item['values'][0])
        employee = next((emp for emp in self.employees if emp.id == emp_id), None)
        
        if employee:
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete {employee.name}?"):
                self.employees.remove(employee)
                self.refresh_employee_list()
                self.update_stats()
                self.add_activity(f"Deleted employee: {employee.name}")
                self.status_var.set(f"Employee {employee.name} deleted")
                self.save_data()

    def view_employee_details(self):
        """Show detailed employee information"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to view")
            return
        
        item = self.employee_tree.item(selection[0])
        emp_id = int(item['values'][0])
        employee = next((emp for emp in self.employees if emp.id == emp_id), None)
        
        if employee:
            EmployeeDetailsDialog(self.root, employee)

    def show_add_shift_dialog(self):
        """Show dialog to add new shift"""
        if not self.current_schedule:
            messagebox.showwarning("No Schedule", "Please select or create a schedule first")
            return
        
        dialog = ShiftDialog(self.root, "Add Shift")
        if dialog.result:
            shift_data = dialog.result
            try:
                shift = Shift(
                    date=shift_data['date'],
                    start_time=shift_data['start_time'],
                    end_time=shift_data['end_time'],
                    roles_required=[shift_data['role']]
                )
                self.current_schedule.add_shift(shift)
                self.refresh_schedule_view()
                self.update_stats()
                self.add_activity(f"Added shift: {shift.get_day_name()} {shift.format_time(shift.start_time)}")
                self.status_var.set("Shift added successfully")
                self.save_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add shift: {str(e)}")

    def create_new_schedule(self):
        """Create new weekly schedule"""
        # Get start date
        start_date_str = simpledialog.askstring("New Schedule", 
                                               "Enter start date (YYYY-MM-DD, should be Monday):")
        if not start_date_str:
            return
        
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=6)  # Sunday
            
            schedule = Schedule(start_date, end_date)
            self.schedules.append(schedule)
            self.current_schedule = schedule
            
            self.refresh_schedule_combo()
            self.refresh_schedule_view()
            self.add_activity(f"Created schedule: {start_date} to {end_date}")
            self.status_var.set(f"New schedule created for week of {start_date}")
            self.save_data()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {str(e)}")

    def refresh_employee_list(self):
        """Refresh the employee list display"""
        # Clear existing items
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
        
        # Add employees
        for employee in self.employees:
            status = "Minor" if employee.is_minor else "Regular"
            if employee.is_manager:
                status = "Manager"
            
            self.employee_tree.insert('', 'end', values=(
                employee.id,
                employee.name,
                employee.role,
                f"${employee.wage:.2f}",
                employee.max_hours,
                status
            ))

    def refresh_schedule_combo(self):
        """Refresh schedule selection combobox"""
        schedule_names = [f"Week of {sched.start_date} (ID: {sched.id})" 
                         for sched in self.schedules]
        self.schedule_combo['values'] = schedule_names
        
        if self.current_schedule:
            current_name = f"Week of {self.current_schedule.start_date} (ID: {self.current_schedule.id})"
            self.schedule_var.set(current_name)
            self.current_schedule_var.set(f"Current: {current_name}")

    def refresh_schedule_view(self):
        """Refresh the weekly schedule view"""
        if not self.current_schedule:
            return
        
        # Clear all day trees
        for day in self.day_frames:
            day_tree = getattr(self, f'{day.lower()}_tree')
            for item in day_tree.get_children():
                day_tree.delete(item)
        
        # Populate with shifts
        for shift in self.current_schedule.get_all_shifts():
            day = shift.get_day_name()
            day_tree = getattr(self, f'{day.lower()}_tree')
            
            # Get assigned employee names
            assigned_names = []
            for emp_id in shift.assigned_employees:
                emp = next((e for e in self.employees if e.id == emp_id), None)
                if emp:
                    assigned_names.append(emp.name)
            
            assigned_str = ", ".join(assigned_names) if assigned_names else "UNASSIGNED"
            status = "✅ Filled" if shift.is_filled else "❌ Need Staff"
            
            time_str = f"{shift.format_time(shift.start_time)}-{shift.format_time(shift.end_time)}"
            
            day_tree.insert('', 'end', values=(
                time_str,
                shift.roles_required[0] if shift.roles_required else "Any",
                assigned_str,
                status
            ))

    def on_schedule_selected(self, event=None):
        """Handle schedule selection change"""
        selection = self.schedule_var.get()
        if not selection:
            return
        
        # Extract schedule ID from selection
        try:
            schedule_id = int(selection.split("ID: ")[1].split(")")[0])
            self.current_schedule = next((s for s in self.schedules if s.id == schedule_id), None)
            self.refresh_schedule_view()
            self.current_schedule_var.set(f"Current: {selection}")
        except (ValueError, IndexError):
            pass

    def update_stats(self):
        """Update dashboard statistics"""
        self.stats_employees.set(str(len(self.employees)))
        self.stats_schedules.set(str(len(self.schedules)))
        
        total_shifts = sum(len(sched.get_all_shifts()) for sched in self.schedules)
        self.stats_shifts.set(str(total_shifts))

    def add_activity(self, activity):
        """Add activity to recent activity list"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_listbox.insert(0, f"[{timestamp}] {activity}")
        
        # Keep only last 50 activities
        if self.activity_listbox.size() > 50:
            self.activity_listbox.delete(50, tk.END)

    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Create sample employees
        sample_employees = [
            ("Shane van Boening", "555-0001", "alice@luigis.com", "server", 16.00, 40, False),
            ("Jayson Shaw", "555-0002", "bob@luigis.com", "server", 15.50, 40, False),
            ("Magnus Carlsen", "555-0003", "charlie@luigis.com", "cook", 18.50, 40, False),
            ("Anatoly Karpov", "555-0004", "diana@luigis.com", "cook", 19.00, 40, False),
            ("Luigi Mangione", "555-0005", "luigi@luigis.com", "manager", 25.00, 50, False),
            ("Chad Thunderstud", "555-0006", "emma@luigis.com", "server", 14.50, 20, True),
        ]
        
        for emp_data in sample_employees:
            employee = Employee(*emp_data)
            # Add some availability
            employee.add_availability("Monday", 1000, 1800)
            employee.add_availability("Tuesday", 1000, 1800)
            employee.add_availability("Wednesday", 1000, 1800)
            employee.add_availability("Friday", 1700, 2200)
            employee.add_availability("Saturday", 1000, 2200)
            
            self.employees.append(employee)
        
        self.refresh_employee_list()
        self.update_stats()
        self.add_activity("Loaded sample data")

    def save_data(self):
        """Save data to JSON file"""
        # This is a placeholder - implement actual JSON serialization
        pass

    def load_data(self):
        """Load data from JSON file"""
        # This is a placeholder - implement actual JSON deserialization
        pass

    # Additional methods for shift management, employee assignment, etc.
    def edit_selected_shift(self):
        """Edit selected shift"""
        messagebox.showinfo("Coming Soon", "Shift editing will be implemented in next version")

    def assign_employee_to_shift(self):
        """Assign employee to selected shift"""
        messagebox.showinfo("Coming Soon", "Employee assignment dialog will be implemented in next version")

    def delete_selected_shift(self):
        """Delete selected shift"""
        messagebox.showinfo("Coming Soon", "Shift deletion will be implemented in next version")

    def delete_current_schedule(self):
        """Delete current schedule"""
        if self.current_schedule:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the current schedule?"):
                self.schedules.remove(self.current_schedule)
                self.current_schedule = None
                self.refresh_schedule_combo()
                self.refresh_schedule_view()
                self.add_activity("Deleted schedule")
                self.save_data()


class EmployeeDialog:
    def __init__(self, parent, title, employee=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Form fields
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar(value=employee.name if employee else "")
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Phone:").grid(row=1, column=0, sticky='w', pady=5)
        self.phone_var = tk.StringVar(value=employee.phone_number if employee else "")
        ttk.Entry(main_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.email_var = tk.StringVar(value=employee.email if employee else "")
        ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Role:").grid(row=3, column=0, sticky='w', pady=5)
        self.role_var = tk.StringVar(value=employee.role if employee else "server")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, 
                                 values=['server', 'cook', 'host', 'manager', 'assistant manager'])
        role_combo.grid(row=3, column=1, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Wage ($):").grid(row=4, column=0, sticky='w', pady=5)
        self.wage_var = tk.StringVar(value=str(employee.wage) if employee else "15.00")
        ttk.Entry(main_frame, textvariable=self.wage_var, width=30).grid(row=4, column=1, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Max Hours:").grid(row=5, column=0, sticky='w', pady=5)
        self.max_hours_var = tk.StringVar(value=str(employee.max_hours) if employee else "40")
        ttk.Entry(main_frame, textvariable=self.max_hours_var, width=30).grid(row=5, column=1, pady=5, sticky='ew')
        
        self.is_minor_var = tk.BooleanVar(value=employee.is_minor if employee else False)
        ttk.Checkbutton(main_frame, text="Is Minor (under 18)", 
                       variable=self.is_minor_var).grid(row=6, column=1, pady=5, sticky='w')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save_employee).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side='left', padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Wait for dialog to close
        self.dialog.wait_window()

    def save_employee(self):
        """Save employee data"""
        try:
            self.result = {
                'name': self.name_var.get().strip(),
                'phone': self.phone_var.get().strip(),
                'email': self.email_var.get().strip(),
                'role': self.role_var.get().strip(),
                'wage': self.wage_var.get().strip(),
                'max_hours': self.max_hours_var.get().strip(),
                'is_minor': self.is_minor_var.get()
            }
            
            # Basic validation
            if not all([self.result['name'], self.result['phone'], self.result['email'], 
                       self.result['role'], self.result['wage'], self.result['max_hours']]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Validate numeric fields
            float(self.result['wage'])
            int(self.result['max_hours'])
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for wage and max hours")


class ShiftDialog:
    def __init__(self, parent, title):
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky='w', pady=5)
        self.date_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.date_var, width=25).grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Start Time (24hr):").grid(row=1, column=0, sticky='w', pady=5)
        self.start_var = tk.StringVar(value="0900")
        ttk.Entry(main_frame, textvariable=self.start_var, width=25).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="End Time (24hr):").grid(row=2, column=0, sticky='w', pady=5)
        self.end_var = tk.StringVar(value="1700")
        ttk.Entry(main_frame, textvariable=self.end_var, width=25).grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Role Required:").grid(row=3, column=0, sticky='w', pady=5)
        self.role_var = tk.StringVar(value="server")
        ttk.Combobox(main_frame, textvariable=self.role_var, 
                    values=['server', 'cook', 'host', 'manager']).grid(row=3, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save_shift).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side='left', padx=5)
        
        self.dialog.wait_window()

    def save_shift(self):
        """Save shift data"""
        try:
            self.result = {
                'date': self.date_var.get().strip(),
                'start_time': int(self.start_var.get().strip()),
                'end_time': int(self.end_var.get().strip()),
                'role': self.role_var.get().strip()
            }
            
            # Basic validation
            if not all([self.result['date'], self.result['role']]):
                messagebox.showerror("Error", "Date and role are required")
                return
            
            # Validate date format
            datetime.strptime(self.result['date'], "%Y-%m-%d")
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")


class EmployeeDetailsDialog:
    def __init__(self, parent, employee):
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Employee Details - {employee.name}")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create content
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Employee info
        info_frame = ttk.LabelFrame(main_frame, text="Employee Information", padding=10)
        info_frame.pack(fill='x', pady=5)
        
        ttk.Label(info_frame, text=f"ID: {employee.id}", font=('Arial', 10, 'bold')).pack(anchor='w')
        ttk.Label(info_frame, text=f"Name: {employee.name}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Phone: {employee.phone_number}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Email: {employee.email}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Role: {employee.role}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Wage: ${employee.wage:.2f}/hour").pack(anchor='w')
        ttk.Label(info_frame, text=f"Max Hours: {employee.max_hours}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Status: {'Minor' if employee.is_minor else 'Regular'}").pack(anchor='w')
        
        # Availability
        avail_frame = ttk.LabelFrame(main_frame, text="Availability", padding=10)
        avail_frame.pack(fill='both', expand=True, pady=5)
        
        if employee.available_days_times:
            for day, start, end in employee.available_days_times:
                start_formatted = f"{start//100:02d}:{start%100:02d}"
                end_formatted = f"{end//100:02d}:{end%100:02d}"
                ttk.Label(avail_frame, text=f"{day}: {start_formatted} - {end_formatted}").pack(anchor='w')
        else:
            ttk.Label(avail_frame, text="No availability set").pack(anchor='w')
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack(pady=10)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SchedulingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()