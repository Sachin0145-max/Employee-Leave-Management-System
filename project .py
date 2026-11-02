from datetime import datetime

# Employee Data Dictionary storing records and leave balances
employees = {
    "E101": {
        "name": "Amit",
        "balances": {
            "Casual Leave": 12,
            "Sick Leave": 10,
            "Earned Leave": 15
        }
    }
}

def validate_employee(emp_id):
    """Confirm that the entered employee ID exists."""
    return emp_id in employees

def validate_leave_type(leave_type):
    """Accept and format supported leave types regardless of case."""
    mapping = {
        "casual leave": "Casual Leave",
        "sick leave": "Sick Leave",
        "earned leave": "Earned Leave"
    }
    cleaned_input = leave_type.strip().lower()
    return mapping.get(cleaned_input, None)

def calculate_leave_days(from_date_str, to_date_str):
    """Parse dates, handle slashes automatically, and calculate inclusive leave days."""
    # Replace slashes with hyphens so both YYYY-MM-DD and YYYY/MM/DD work
    from_date_str = from_date_str.replace('/', '-')
    to_date_str = to_date_str.replace('/', '-')
    
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        
        if from_date > to_date:
            return None, "Error: 'From-Date' cannot be later than 'To-Date'."
        
        delta = to_date - from_date
        return delta.days + 1, None
    except ValueError:
        return None, "Error: Invalid date format. Please use YYYY-MM-DD."

def view_balance():
    """Display current balance for the employee."""
    emp_id = input("Enter Employee ID (e.g., E101): ").strip()
    
    if not validate_employee(emp_id):
        print("[ERROR] Employee ID not found.")
        return

    emp = employees[emp_id]
    print(f"\n--- Leave Balance for {emp['name']} ({emp_id}) ---")
    for leave_type, balance in emp["balances"].items():
        print(f"- {leave_type}: {balance} days remaining")
    print("-" * 40)

def apply_leave():
    """Process a leave request."""
    emp_id = input("Enter Employee ID (e.g., E101): ").strip()
    if not validate_employee(emp_id):
        print("[ERROR] Employee ID not found.")
        return

    print("\nSupported Leave Types:")
    print("1. Casual Leave\n2. Sick Leave\n3. Earned Leave")
    raw_leave_type = input("Enter Leave Type (Casual Leave / Sick Leave / Earned Leave): ")
    
    leave_type_choice = validate_leave_type(raw_leave_type)
    if not leave_type_choice:
        print("[ERROR] Invalid leave category selected.")
        return

    from_date_str = input("Enter From-Date (YYYY-MM-DD): ").strip()
    to_date_str = input("Enter To-Date (YYYY-MM-DD): ").strip()

    days, error_msg = calculate_leave_days(from_date_str, to_date_str)
    if error_msg:
        print(f"[ERROR] {error_msg}")
        return

    current_balance = employees[emp_id]["balances"][leave_type_choice]

    print(f"\nRequested Days: {days}")
    print(f"Available Balance: {current_balance}")

    if days <= current_balance:
        employees[emp_id]["balances"][leave_type_choice] -= days
        print(f"[SUCCESS] Leave Approved! {days} day(s) deducted.")
        print(f"Remaining {leave_type_choice}: {employees[emp_id]['balances'][leave_type_choice]} days.")
    else:
        print(f"[REJECTED] Insufficient leave balance. You requested {days} days, but only have {current_balance} days left.")

def main():
    """Control the console application."""
    while True:
        print("\n==============================")
        print(" EMPLOYEE LEAVE MANAGEMENT SYSTEM ")
        print("==============================")
        print("1. View Leave Balance")
        print("2. Apply for Leave")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            view_balance()
        elif choice == '2':
            apply_leave()
        elif choice == '3':
            print("Exiting application. Thank you!")
            break
        else:
            print("[INVALID] Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()