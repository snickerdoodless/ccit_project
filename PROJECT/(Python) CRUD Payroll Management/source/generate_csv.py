import csv
from datetime import datetime, timedelta
import mysql.connector

# Function to generate payroll report
def generate_payroll_report(cursor, export_path=None):
    if not export_path:
        export_path = r"C:\Users\Jotun\Desktop\payroll_report.csv"
    
    today = datetime.today()
    last_month = today - timedelta(days=30)
    
    query = """
    SELECT e.id AS employee_id, e.name, s.salary AS base_salary, 
           s.bonuses, s.deduction, s.net_salary, 
           p.position_name, c.status AS employment, s.due_date
    FROM employees e
    JOIN employee_position ep ON e.id = ep.employee_id
    JOIN employees_salaries s ON ep.id = s.employee_position_id
    JOIN positions p ON ep.position_id = p.id
    JOIN contract c ON ep.id = c.employee_position_id
    WHERE s.due_date >= %s
    """
    
    try:
        cursor.execute(query, (last_month,))
        payroll_records = cursor.fetchall()
        
        if not payroll_records:
            print("No payroll records found for the last month.")
            return
    
        print("+----+-------+-------------+---------+-----------+------------+--------------+-------------+------------------+-----------------+")
        print("| ID | Name  | Base Salary | Bonuses | Deduction | Net Salary | Position     | Employment  | Last Payroll Date | Due Date        |")
        print("+----+-------+-------------+---------+-----------+------------+--------------+-------------+------------------+-----------------+")
        for record in payroll_records:
            print(f"| {record[0]:^2} | {record[1]:^5} | {record[2]:^11} | {record[3]:^7} | {record[4]:^9} | {record[5]:^10} | {record[6]:^12} | {record[7]:^11} | {today.strftime('%Y-%m-%d')} | {record[8]} |")
        print("+----+-------+-------------+---------+-----------+------------+--------------+-------------+------------------+-----------------+")

        with open(export_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Employee ID", "Name", "Base Salary", "Bonuses", "Deduction", "Net Salary", "Position", "Employment", "Last Payroll Date", "Due Date"])
            for record in payroll_records:
                writer.writerow([record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], today.strftime('%Y-%m-%d'), record[8]])

        print(f"Payroll report successfully exported to {export_path}")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

