import json
from crewai.tools import tool

employees=[
    {
    "employee_id":101,
    "employee_name":"Pranjali",
    "leave_balance":12
    },
    {
    "employee_id":102,
    "employee_name":"Akash",
    "leave_balance":10
    },
    {
    "employee_id":103,
    "employee_name":"Sahil",
    "leave_balance":10
    },
    {
    "employee_id":104,
    "employee_name":"Shiv",
    "leave_balance":10
    },
    {
    "employee_id":105,
    "employee_name":"Prince",
    "leave_balance":7
    },
    {
    "employee_id":106,
    "employee_name":"Hitesh",
    "leave_balance":9
    },
    {
    "employee_id":107,
    "employee_name":"Shreyans",
    "leave_balance":11
    },

]


@tool("check_leave_balance")
def check_leave_balance(employee_id:int)->str:
    """Find an employee and return their leave balance"""
    for employee in employees:
        if employee["employee_id"]==employee_id:
            return json.dumps(employee)
        return json.dumps({
            "status":"not_found",
            "message":"Employee does not exist"
        })