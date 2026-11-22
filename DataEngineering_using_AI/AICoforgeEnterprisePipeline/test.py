import pandas as pd

# CSV Loading and DataFrame Operations
it_employees_df=pd.read_csv("AICoforgeEnterprisePipeline/data/employees/finance_employees.csv")
hr_employees_df=pd.read_csv("AICoforgeEnterprisePipeline/data/employees/hr_employees.csv")
finance_employees_df=pd.read_csv("AICoforgeEnterprisePipeline/data/employees/finance_employees.csv")
sales_employees_df=pd.read_csv("AICoforgeEnterprisePipeline/data/employees/sales_employees.csv")
operations_employees_df=pd.read_csv("AICoforgeEnterprisePipeline/data/employees/operations_employees.csv")

employee_df=pd.concat([it_employees_df,hr_employees_df,
                       finance_employees_df,sales_employees_df,
                       operations_employees_df])

print(employee_df)

print(employee_df.head(20))
print(employee_df.tail(20))

result=employee_df.groupby("department").size()
print(result)

print("Total Employeees across all departments:",employee_df.shape[0])
print("Total Employeees across all departments:",len(employee_df))

print(employee_df.columns)
print(employee_df.dtypes)

print("column contains missing values.")
print(employee_df.isnull().sum())

print("Duplicate records based on employee id")
result=employee_df["emp_id"].duplicated()
print(result)

print("Duplicate records based on employee id")
duplicated_records=employee_df[employee_df["emp_id"].duplicated()]
print(duplicated_records)

duplicated_records=employee_df[employee_df["emp_id"].duplicated(keep=False)]
print(duplicated_records.sort_values("emp_id"))

print(employee_df["emp_id"].value_counts())
duplicates = employee_df[employee_df.duplicated(subset=["emp_id"], keep=False)]

print(duplicates.head(4))
print(employee_df[employee_df["emp_id"] == 401])
# duplicates = employee_df[employee_df.duplicated(subset=["emp_id"], keep=False)]

print(duplicates.sort_values("emp_id"))


print(employee_df.groupby("department")["emp_id"].size())

print(f"Total unique cities:{employee_df["city"].nunique()}")


# Section 2: Basic Filtering and Selection 
 
print("++++++Display all employees working in the IT department.++++++")
result=employee_df[employee_df["department"]=="IT"]
print(result.head(5))

result=employee_df[employee_df["department"]=="Finance"]
print(result.head(10))

result=employee_df[employee_df["salary"]>100000]
print(result.head(10))

result=employee_df[employee_df["salary"].between(50000,90000)]
print(result)

print(employee_df[employee_df["city"]=="Pune"])
print(employee_df[
    (employee_df["department"]=="IT") &
    (employee_df["city"]=="Bangalore")
])

print(employee_df[
    (employee_df["department"]=="Finance") &
    (employee_df["salary"]>80000)
])

res=employee_df[employee_df["department"].isin(["HR","Sales"])]
print(res)

res=employee_df[
    (employee_df["salary"]<40000) &
    (employee_df["city"]=="Chennai") 
]
print(res)

res=employee_df[~(employee_df["city"]=="Mumbai")]
print(res)

#  SUM and Total Salary Calculations
result=employee_df["salary"].sum()
print(result)

res=employee_df[employee_df["department"]=="IT"]["salary"].sum()
print(result)

res=employee_df[employee_df["department"]=="HR"]["salary"].sum()
print(res)

res=employee_df[employee_df["department"]=="Sales"]["salary"].sum()
print(res)

res=employee_df[employee_df["department"]=="Operations"]["salary"].sum()
print(res)

res=employee_df.groupby("department")["salary"].sum()
print(res)

res=employee_df.groupby("city")["salary"].sum()
print(res)

result=employee_df[employee_df.isin(["IT","Finance"])]["salary"].sum()
print(result)


# MAX, MIN and AVG Operations 
print("*****************************************")
print(employee_df["salary"].max())

print(employee_df["salary"].min())

print(employee_df["salary"].mean())

res=employee_df.groupby("department")["salary"].max()
print(res)

res=employee_df.groupby("department")["salary"].min()
print(res)

avg_sal=employee_df.groupby("department")["salary"].mean()
print(avg_sal)

print(employee_df.groupby("city")["salary"].max())

print("****** Minimum salary in each city. ************")
print(employee_df.groupby("city")["salary"].min())

result=employee_df[employee_df["city"]=="Pune"]["salary"].mean()
print(result)

max_Sal=employee_df.groupby("department")["salary"].max()
min_Sal=employee_df.groupby("department")["salary"].min()
print("Difference:")
print(max_Sal-min_Sal)

#  GROUP BY – Department and City Analysis
result=