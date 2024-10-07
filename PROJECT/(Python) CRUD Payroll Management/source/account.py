import bcrypt
import mysql.connector
from main import admin_dashboard, employee_dashboard

# Register for new user  
def regist_user(cursor, connection, username, password, is_admin):
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    if is_admin == True:
        query = "INSERT INTO users (username, hash_pw, roles) VALUES (%s, %s, 'admin')"
    else:
        query = "INSERT INTO users (username, hash_pw, roles) VALUES (%s, %s, 'employee')"
    
    try:
        cursor.execute(query, (username, hashed_pw))
        connection.commit()
        
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        rows = cursor.fetchall()
        
        if rows:
            user_id = rows[0][0]
        else:
            print("Error: User ID not found!")
            return
        
        link_employee = input("Do you want to link this user to an employee? (yes/no): ").lower()
        
        if link_employee == "yes":
            employee_id = input("Enter Employee ID to link: ")
            update_query = "UPDATE employees SET user_id = %s WHERE id = %s"
            cursor.execute(update_query, (user_id, employee_id))
            connection.commit()
            print(f"User account successfully linked to Employee ID {employee_id}!")
        
        print("User Successfully Registered!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

        
# Login for user
def login_user(cursor, username, password):
    
    query = "SELECT id, hash_pw, roles FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    output = cursor.fetchone()
    
    if output:
        user_id, stored_hash, role = output
        
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode()):
            if role == "admin":
                print(f"Login Successful as {role}!")
                return admin_dashboard()
            else:
                print(f"Login Successful as {role}!")
                return employee_dashboard(user_id)
        else:
            print("Invalid password or username!")
    else:
        print("Username Invalid or Not Exist!")
        return 

