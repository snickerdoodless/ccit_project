import mysql.connector
from validate import validate_input

# MANAGE EMPLOYEES

# Adding Employee Record
def add_employee(cursor, connection, name, age, gender, address, phone, email, last_education, user_id=None):
    query = """
    INSERT INTO employees
    (name, age, gender, address, phone, email, last_education, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        email = validate_input("email", email)
        gender = validate_input("gender", gender)
        
        if user_id == '':
            user_id = None
        
        cursor.execute(query, (name, age, gender, address, phone, email, last_education, user_id))
        connection.commit()
        print(f"Employee {name} Successfully Added!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")



# Editing Employee Record
def edit_employee(cursor, connection, id, field, new_value):
    
    query_check = "SELECT id FROM employees WHERE id = %s"
    cursor.execute(query_check, (id,))
    fetch = cursor.fetchone()
    
    if not fetch:
        print(f"Employee of ID: {fetch} does not exist!")
        return
    
    field_map = {
        "1": "name",
        "2": "age",
        "3": "gender",
        "4": "address",
        "5": "phone",
        "6": "email",
        "7": "last_education"
    }

    if field not in field_map:
        print("Invalid Field Options!")
        return

    query = f"UPDATE employees SET {field_map[field]} = %s WHERE id = %s"

    try:
        if field == "3":
            new_value = validate_input("gender", new_value)
        elif field == "6":
            new_value = validate_input("email", new_value)
        elif field == "2":
            new_value = validate_input("age", new_value)

        cursor.execute(query, (new_value, id))
        connection.commit()
        print(f"Employee Information of ID: {id} Successfully Updated!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Deleting Emplooyee Record 
def delete_employee(cursor, connection, id):
    confirmation = input(f"Are you sure you want to delete the Employee with ID {id}? This action cannot be undone! (yes/no): ").lower()
    
    if confirmation == "yes":
        try:
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (id,))
            
            connection.commit()
            print(f"Employee of ID: {id} Successfully Resign!")
        except mysql.connector.Error as e:
            print(e)
    elif confirmation == "no":
        print("Action Canceled.")
        return
    else:
        print("Please Choose (yes/no)!")
        return

# Adding New Position Name
def add_position(cursor, connection, position_name, range_salary):
    query = "INSERT INTO positions (position_name, range_salary) VALUES (%s, %s)"
    
    try:
        cursor.execute(query, (position_name, range_salary))
        connection.commit()  
        print(f"Position '{position_name}' Successfully Added!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Assign Employee Position
def add_employee_position(cursor, connection, employee_id, position_id):
    query = "INSERT INTO employee_position (employee_id, position_id, status) VALUES (%s, %s, %s)"
    try:
        cursor.execute("SELECT id FROM positions WHERE id = %s", (position_id,))
        position_exists = cursor.fetchone()
        
        if position_exists:
            status = input("Enter Employment Status (INTERN/EMPLOYMENT): ").upper()
            if status not in ["INTERN", "EMPLOYMENT"]:
                print("Invalid Status! Please enter either 'INTERN' or 'EMPLOYMENT'.")
                return 
            
            cursor.execute(query, (employee_id, position_id, status))
            connection.commit()
            print(f"Employee ID {employee_id} assigned to Position Number {position_id} with status '{status}'.")
        else:
            print("Error: Position ID does not exist.")
            
    except mysql.connector.Error as e:
        print(f"Error: {e}")

        
# Re-Assign Existing Employee Position
def edit_employee_position(cursor, connection, employee_id, new_position_id):
    query_check_existing = "SELECT * FROM employee_position WHERE employee_id = %s"
    
    try:
        cursor.execute(query_check_existing, (employee_id,))
        existing_position = cursor.fetchone()
        
        if not existing_position:
            print(f"Error: Employee ID {employee_id} has no position assigned yet.")
            return
        
        cursor.execute("SELECT id FROM positions WHERE id = %s", (new_position_id,))
        position_exists = cursor.fetchone()
        
        if position_exists:
            query_update_position = "UPDATE employee_position SET position_id = %s WHERE employee_id = %s"
            cursor.execute(query_update_position, (new_position_id, employee_id))
            connection.commit()
            print(f"Employee ID {employee_id} successfully re-assigned to Position ID {new_position_id}.")
        else:
            print("Error: Position ID does not exist.")
            
    except mysql.connector.Error as e:
        print(f"Error: {e}")



