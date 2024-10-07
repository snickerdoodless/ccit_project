import re
from datetime import datetime

# Validating user input
def validate_input(type, value):
    if type == "age":
        value = int(value)
        if value <= 0 or value > 100:
            raise ValueError("Invalid age, Please enter proper number!")
        else:
            return value
        
    if type == "email":
        value = value.lower()
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format!")
        else:
            return value

    elif type == "date":    
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError as e:
            print(e, "Invalid date format (YYYY-MM-DD).")
        
    elif type == "gender":
        value = value.upper()
        allowed = ["MALE", "FEMALE"]
        if value not in allowed:
            raise ValueError("GOD created 2 gender MALE or FEMALE!")
        else:
            return value
      
