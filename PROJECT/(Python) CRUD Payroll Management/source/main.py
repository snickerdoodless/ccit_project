from getpass import getpass as hide
import mysql.connector
import account
import manage_employee
import manage_salaries
import view
from generate_csv import generate_payroll_report

# Connection & Cursor setup
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="reds",
    database="payroll"
)

cursor = connection.cursor()

# Employee Dashboard
def employee_dashboard(user_id):
    while True:
        print("==================================================")
        print("===        Welcome to Salary Dashboard         ===")
        print("==================================================")
        print("1. View Personal Information")
        print("2. View Payroll Information")
        print("3. Logout")
        
        option = input("Option: ")
        
        if option == "1":
            view.view_employees(cursor, specific=True, employee_id=user_id)
        
        elif option == "2":
            query_position = """
            SELECT ep.id 
            FROM employee_position ep 
            JOIN employees e ON ep.employee_id = e.id 
            WHERE e.user_id = %s
            """
            try:
                cursor.execute(query_position, (user_id,))
                result = cursor.fetchone()
                if result:
                    employee_position_id = result[0]
                    view.view_specific_salary(cursor, employee_position_id)
                else:
                    print("No position record found for this user.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
        
        elif option == "3":
            print("Logging out...")
            from time import sleep
            sleep(2)
            break
        
        else:
            print("Invalid choice! Please select a valid option.")



# Admin Dashboard
# todo: 1. fixed the generate_csv and ask for prompt (see desktop), 2. test each features and function, 3. debugging
# CREATE PAPERWORK!!
def admin_dashboard():
    while True:
        print("==================================================")
        print("=== Welcome to Employee Payroll Management 1.0 ===")
        print("==================================================")
        print("1. Manage Employee")
        print("2. Manage Salary & Contract")
        print("3. Generate Payroll Report")
        print("4. Create Account")
        print("5. View Records")
        print("6. Logout")
        
        choice = input("Option: ")

        if choice == "1":
            menu_employee()
        
        elif choice == "2":
            menu_salaries_contract()
        
        elif choice == "3":
            print("=== Generate Payroll Report ===")
            file_path = input("Enter file path (or press Enter to use default): ").strip()
            
            if file_path:
                generate_payroll_report(cursor, export_path=file_path)
            else:
                generate_payroll_report(cursor)
        
        elif choice == "4":
            create_account()
        
        elif choice == "5":
            print("=== View Records ===")
            print("1. View All Employees Record")
            print("2. View Specific Employee Record")
            print("3. View All Salaries Record")
            print("4. View Specific Salary Record")
            print("5. Back to Menu")
            
            option = input("Option: ")
            
            if option == "1":
                view.view_employees(cursor, specific=False)

            elif option == "2":
                employee_id = input("Enter Employee ID: ")
                print("\n")
                view.view_employees(cursor, specific=True, employee_id=employee_id)

            elif option == "3":
                view.view_all_salaries(cursor) 
            
            elif option == "4":
                employee_position_id = input("Enter Employee Position ID: ")
                view.view_specific_salary(cursor, employee_position_id)  
            
            elif option == "5":
                continue  
            
            else:
                print("Invalid option! Please choose a valid record option.")
        
        elif choice == "6":
            from time import sleep
            print("Logging out...")
            sleep(2)
            break
        
        else:
            print("Invalid option! Please choose a valid option.")


# Function to manage employees
def menu_employee():
    while True:
        print("==================================================")
        print("===            Managing Employees              ===")
        print("==================================================")
        print("1. Add Employees")
        print("2. Edit Employees")
        print("3. Delete Employees")
        print("4. Assign Position")
        print("5. Re-Assign Position")
        print("6. Create New Position")
        print("7. Back to Menu")
        
        option = input("Option: ")
        
        if option == "1":
            print("=== Add Employees ===")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (MALE/FEMALE): ").upper()
            address = input("Enter Address: ")
            phone = input("Enter Phone: ")
            email = input("Enter Email: ").lower()
            last_education = input("Enter Last Education: ")
            user_id = input("Enter User ID (Leave it blank if employees do not have account yet): ")

            manage_employee.add_employee(cursor, connection, name, age, gender, address, phone, email, last_education, user_id)
        
        elif option == "2":
            print("=== Modify Employee ===")
            emp_id = input("Enter Employee ID: ")
            print("Which field do you want to edit?")
            print("1. Name\n2. Age\n3. Gender\n4. Address\n5. Phone\n6. Email\n7. Last Education")
            field = input("Choose a field number: ")
            new_value = input("Enter the new value: ")
            
            manage_employee.edit_employee(cursor, connection, emp_id, field, new_value)
        
        elif option == "3":
            print("=== Resign Employee ===")
            emp_id = input("Enter Employee User ID to delete: ")
            manage_employee.delete_employee(cursor, connection, emp_id)

        elif option == "4":
            print("=== Assign Employee ===")
            employee_id = input("Enter Employee ID to assign a position: ")
            
            query_fetch = "SELECT id, position_name FROM positions"
            cursor.execute(query_fetch,)
            list_position = cursor.fetchall()
            print(f"Position List:")
            print("-----------------")
            for position in list_position:
                print(position)
                
            position_id = input("Enter Position ID: ")
            confirm = input(f"Are you sure you want to assign Employee ID {employee_id} to Position ID {position_id}? (yes/no): ").lower()
            
            if confirm == "yes":
                manage_employee.add_employee_position(cursor, connection, employee_id, position_id)
            else:
                print("Position assignment canceled.")
                return
        
        elif option == "5":  
            print("=== Promote/Demote Employee ===")
            employee_id = input("Enter Employee ID to re-assign position: ")
            
            query_fetch = "SELECT id, position_name FROM positions"
            cursor.execute(query_fetch,)
            list_position = cursor.fetchall()
            print(f"Position List:")
            print("-----------------")
            for position in list_position:
                print(position)
                
            new_position_id = input("Enter New Position ID: ")
            confirm = input(f"Are you sure you want to re-assign Employee ID {employee_id} to Position ID {new_position_id}? (yes/no): ").lower()
            
            if confirm == "yes":
                manage_employee.edit_employee_position(cursor, connection, employee_id, new_position_id)
            else:
                print("Position re-assignment canceled.")
                return
        
        elif option == "6":  
            print("=== Create New Position ===")
            position_name = input("Enter New Position Name: ")
            range_salary = input("Enter Salary Range (e.g., $50.000-$70.000): ")
            confirm = input("Are you sure you want to create this new position? (yes/no): ").lower()
            
            if confirm == "yes":
                manage_employee.add_position(cursor, connection, position_name, range_salary)
            else:
                print("Position creation canceled.")
                return

        elif option == "7":
            return admin_dashboard()

# Function to manage salaries and contract
def menu_salaries_contract():
    while True:
        print("==================================================")
        print("===       Managing Salaries & Contracts        ===")
        print("==================================================")
        print("1. Add Salary Record")
        print("2. Edit Salary Record")
        print("3. Delete Salary Record")
        print("4. Add Contract")
        print("5. Update/Delete Contract")
        print("6. Back to Main Menu")
        
        option = input("Option: ")

        if option == "1":
            print("=== Add Salary Record ===")
            try:
                employee_id = int(input("Enter Employee ID: "))

                view.display_salary_range(cursor, employee_id)

                salary = input("Enter salary: ")
                bonuses = input("Enter bonuses: ")
                deduction = int(input("Enter deduction (tax): "))
                due_date = input("Enter due date (YYYY-MM-DD): ")

                cursor.execute("SELECT id FROM employee_position WHERE employee_id = %s", (employee_id,))
                position_info = cursor.fetchone()
                if not position_info:
                    print("Error: No position found for this Employee ID.")
                    return

                employee_position_id = position_info[0]
                
                manage_salaries.add_salary(cursor, connection, salary, bonuses, deduction, due_date, employee_position_id)

            except ValueError:
                print("Invalid input. Please enter numbers for salary, bonuses, and deduction.")

        
        elif option == "2":
            print("=== Edit Salary Record ===")
            try:
                employee_id = int(input("Enter Employee ID: "))
                
                view.display_salary_range(cursor, employee_id)
            
                employee_position_id = int(input("Enter employee position ID to update: "))
                
                if employee_position_id:
                    new_salary = float(input("Enter New Salary: "))
                    new_bonuses = (input("Enter New Bonuses (press Enter to keep current): "))
                    new_deduction = (input("Enter new deduction (press Enter to keep current): "))

                    manage_salaries.edit_salary(cursor, connection, employee_position_id, new_salary, new_bonuses, new_deduction)
                    
                else:
                    print("Employee Position ID is required.")
                    
            except ValueError as e:
                print(f"Error: {e}")
        
        elif option == "3":
            print("=== Delete Salary Record ===")
            try:
        
                employee_position_id = int(input("Enter employee position ID to remove: "))
                manage_salaries.del_employees_salary(cursor, connection, employee_position_id)
            except ValueError:
                print("Invalid ID input.")
        
        elif option == "4":
            print("=== Add Contract ===")
            try:
                employee_id = int(input("Enter Employee ID: "))
                
                view.display_salary_range(cursor, employee_id)
                
                employee_position_id = int(input("Enter employee position ID: "))
                
                query_check = "SELECT id FROM employee_position WHERE id = %s"
                cursor.execute(query_check, (employee_position_id,))
                is_exist = cursor.fetchone()
                
                if is_exist:
                    pass
                else:
                    print("Employee Position ID Does Not Exist")
                    return
                
                hire_date = input("Enter hire date (YYYY-MM-DD): ")
                status = input("Enter contract status (fixed/contracted): ").lower()
                if status not in ["fixed", "contracted"]:
                    print("Invalid Option!")
                    return
                
                end_contract_date = None
                if status == "contracted":
                    end_contract_date = input("Enter contract end date (YYYY-MM-DD): ")
                
                manage_salaries.add_contract(cursor, connection, employee_position_id, hire_date, status, end_contract_date)
            except ValueError:
                print("Invalid input.")
        
        elif option == "5":
            print("=== Update/Delete Contract ===")
            action = input("Choose 'update' or 'delete': ").lower()
            if action not in ["update", "delete"]:
                print("Invalid Action!")
            else:
                try:
                    employee_position_id = int(input("Enter Employee Position ID: "))
                    if action == "update":
                        hire_date = input("Re-Enter Hire Date: ")
                        status = input("Enter New Status (fixed/contracted): ").lower()
                        end_contract_date = None
                        if status == "contracted":
                            end_contract_date = input("Enter New End Date (YYYY-MM-DD): ")
                        
                        manage_salaries.manage_contract(cursor, connection, employee_position_id, action, hire_date, status, end_contract_date)
                        
                    elif action == "delete":
                        
                        manage_salaries.manage_contract(cursor, connection, employee_position_id, action)
                        
                except ValueError:
                    print("Invalid Input.")
        
        elif option == "6":
            break
        else:
            print("Invalid Choice. Please Try Again.")

    
# Function to create a new user account
def create_account():
    print("==================================================")
    print("===            Create New Account              ===")
    print("==================================================")
    
    username = input("Enter Username: ").lower()
    roles = input("Enter User Roles (admin/employee): ").lower()
    
    if roles not in ["admin", "employee"]:
        print("Choose Valid Roles!")
        return
    
    if roles == "admin":
        is_admin = True
    else:
        is_admin = False
         
    password = hide("Enter Password: ")
    re_enter_pw = hide("Re-Enter Password: ")
    
    if password != re_enter_pw:
        print("Passwords do not match, please try again!")
    else:
        account.regist_user(cursor, connection, username, password, is_admin)


def main():
    username = input("Enter Username: ")
    password = hide("Enter Password: ")
    
    account.login_user(cursor, username, password)

if __name__ == "__main__":
    main()
