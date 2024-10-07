import mysql.connector

# VIEWING RECORDS

# View Employees (All or Specific)
def view_employees(cursor, specific=None, employee_id=None):
    if specific == True:
        # View specific employee (no changes)
        query = "SELECT * FROM employees WHERE id = %s OR user_id = %s"
        try:
            cursor.execute(query, (employee_id,employee_id))
            employee = cursor.fetchone()

            if employee:
                print("Employee Details:")
                print("+---------------------------------------------+")
                print(f"ID: {employee[0]}")
                print(f"Name: {employee[1]}")
                print(f"Age: {employee[2]}")
                print(f"Gender: {employee[3]}")
                print(f"Address: {employee[4]}")
                print(f"Phone: {employee[5]}")
                print(f"Email: {employee[6]}")
                print(f"Last Education: {employee[7]}")
                print(f"User ID: {employee[8]}")
                print("+---------------------------------------------+\n")
            else:
                print(f"Employee with ID {employee_id} not found.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    else:
        # View all employees
        query = "SELECT * FROM employees"
        try:
            cursor.execute(query)
            employees = cursor.fetchall()

            if employees:
                for employee in employees:
                    print("Employee Details:")
                    print(f"ID: {employee[0]}")
                    print(f"Name: {employee[1]}")
                    print(f"Age: {employee[2]}")
                    print(f"Gender: {employee[3]}")
                    print(f"Address: {employee[4]}")
                    print(f"Phone: {employee[5]}")
                    print(f"Email: {employee[6]}")
                    print(f"Last Education: {employee[7]}")
                    print(f"User ID: {employee[8]}")
                    print("------------------------")
            else:
                print("No employees found.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")


# View All Salaries
def view_all_salaries(cursor):
    query = """
    SELECT s.id, s.salary, s.bonuses, s.deduction, s.net_salary, s.due_date, p.position_name
    FROM employees_salaries s
    JOIN positions p ON s.employee_position_id = p.id
    """
    try:
        cursor.execute(query)
        salaries = cursor.fetchall()

        if salaries:
            for salary in salaries:
                due_date_str = salary[5].strftime("%Y-%m-%d")  # Format the due date as YYYY-MM-DD
                print("Salary Details:")
                print(f"ID: {salary[0]}")
                print(f"Salary: {salary[1]}")
                print(f"Bonuses: {salary[2]}")
                print(f"Deduction: {salary[3]}")
                print(f"Net Salary: {salary[4]}")
                print(f"Due Date: {due_date_str}")
                print(f"Position: {salary[6]}")
                print("------------------------")
        else:
            print("No salary records found.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")


# View Specific Salary
def view_specific_salary(cursor, employee_position_id):
    query = """
    SELECT salary, bonuses, deduction, net_salary, due_date 
    FROM employees_salaries 
    WHERE employee_position_id = %s
    """
    try:
        cursor.execute(query, (employee_position_id,))
        salary_record = cursor.fetchone()

        if salary_record:
            print("Salary Details:")
            print("+-----------------------------------+")
            print(f"Salary: {salary_record[0]}")
            print(f"Bonuses: {salary_record[1]}")
            print(f"Deduction: {salary_record[2]}")
            print(f"Net Salary: {salary_record[3]}")
            print(f"Due Date: {salary_record[4]}")
            print("+-----------------------------------+\n")
        else:
            print(f"No salary record found for Position ID {employee_position_id}.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        

# Display Salaries Range
def display_salary_range(cursor, employee_id):
    query_employee_position_id = "SELECT id FROM employee_position WHERE employee_id = %s"
    query_employee_position = "SELECT position_id FROM employee_position WHERE employee_id = %s"
    query_position = "SELECT position_name, range_salary FROM positions WHERE id = %s"
    query_name = "SELECT name FROM employees WHERE id = %s"
    
    try:
        cursor.execute(query_employee_position, (employee_id,))
        employee_position = cursor.fetchone()
        if not employee_position:
            print("Error: No position found for this Employee ID.")
            return
        
        position_id = employee_position[0]
        
        cursor.execute(query_position, (position_id,))
        position = cursor.fetchone()
        
        cursor.execute(query_name, (employee_id,))
        name = cursor.fetchone()[0]
        
        cursor.execute(query_employee_position_id, (employee_id,))
        post_id = cursor.fetchone()[0]
        
        if position:
            print(f"Name: {name}")
            print(f"Position: {position[0]}")
            print(f"Employee Position ID: {post_id}")
            print(f"Salary Range Reference: {position[1]}")
        else:
            print("Position not found.")
            return

    except mysql.connector.Error as e:
        print(f"Error: {e}")