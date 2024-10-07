import mysql.connector
from validate import validate_input

# MANAGING SALARIES

# Add Salary Record
def add_salary(cursor, connection, salary, bonuses=0, deduction=0, due_date=None, employee_position_id=None):
    try:
        due_date = validate_input("date", due_date)
        
        salary = int(salary)
        bonuses = int(bonuses)
        deduction = int(deduction)
        
        gross_salary = salary + bonuses
        deduction_amount = (gross_salary * deduction) / 100
        total_salary = gross_salary - deduction_amount
        print(f"Calculated Net Salary: {total_salary}")

        query_salary = """
        INSERT INTO employees_salaries (salary, bonuses, deduction, net_salary, due_date, employee_position_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query_salary, (salary, bonuses, deduction, total_salary, due_date, employee_position_id))
        connection.commit()
        print("Salary record successfully added!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")


# Updating Salary Record
def edit_salary(cursor, connection, employee_position_id, new_salary, new_bonuses=None, new_deduction=None):
    query_check = "SELECT bonuses, deduction FROM employees_salaries WHERE employee_position_id = %s"

    try:
        cursor.execute(query_check, (employee_position_id,))
        output = cursor.fetchone()

        if output:
            current_bonuses, current_deduction = output

            bonuses = new_bonuses if new_bonuses else current_bonuses
            deduction = new_deduction if new_deduction else current_deduction

            gross_salary = new_salary + bonuses
            deductions_amount = (gross_salary * deduction) / 100
            net_salary = gross_salary - deductions_amount
            
            query_update = """
            UPDATE employees_salaries
            SET salary = %s, bonuses = %s, deduction = %s, net_salary = %s 
            WHERE employee_position_id = %s
            """
            
            cursor.execute(query_update, (new_salary, bonuses, deduction, net_salary, employee_position_id))
            connection.commit()
            print(f"Salary for Employee Position ID: {employee_position_id} Updated Successfully!")
        
        else:
            print(f"No Salary Record Found For Employee Position ID: {employee_position_id}")
            
    except mysql.connector.Error as e:
        print(f"Error: {e}")

        
# Deleting Salary Record
def del_employees_salary(cursor, connection, employee_position_id):
    query_check = "SELECT id FROM employee_position WHERE id = %s"
    query = "DELETE FROM employees_salaries WHERE employee_position_id = %s"
    
    try:
        cursor.execute(query_check, (employee_position_id,))
        result = cursor.fetchone()
        
        if result is not None:  
            is_exist = result[0]
            if is_exist:
                cursor.execute(query, (employee_position_id,))
                connection.commit()
                print(f"Salary record for Employee Position ID: {employee_position_id} Successfully Deleted!")
        else:
            print("Employee Position ID Not Exist!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        

# MANAGE CONTRACT

# Adding Contract Record
def add_contract(cursor, connection, employee_position_id, hire_date, status, end_contract_date=None):
    hire_date = validate_input("date", hire_date)
    
    if status == "contracted":
        if not end_contract_date:
            print("Contracted employees must have an end contract date.")
            return
        else:
            end_contract_date = validate_input("date", end_contract_date)
            if not end_contract_date:
                print("Invalid end contract date.")
                return
    
    try:
        query = """
        INSERT INTO contract (employee_position_id, hire_date, status, end_contract_date)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (employee_position_id, hire_date, status, end_contract_date))
        connection.commit()
        print("Contract successfully added!")
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")


# Update/Delete Contract Record
def manage_contract(cursor, connection, employee_position_id, action, hire_date=None, status=None, end_contract_date=None):
    try:
        if action == "update":
            if hire_date:
                hire_date = validate_input("date", hire_date)
            if status == "fixed":
                end_contract_date = None
            elif status == "contracted" and end_contract_date:
                end_contract_date = validate_input("date", end_contract_date)
            
            query_update = """
            UPDATE contract
            SET hire_date = %s, status = %s, end_contract_date = %s
            WHERE employee_position_id = %s
            """
            cursor.execute(query_update, (hire_date, status, end_contract_date, employee_position_id))
            connection.commit()
            print(f"Contract for Employee Position ID: {employee_position_id} Updated Successfully!")

        elif action == "delete":
            query_delete = "DELETE FROM contract WHERE employee_position_id = %s"
            cursor.execute(query_delete, (employee_position_id,))
            connection.commit()
            print(f"Contract for Employee Position ID: {employee_position_id} Deleted Successfully!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
