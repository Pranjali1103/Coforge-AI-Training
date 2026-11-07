import pandas as pd
import numpy as np
emp_df=pd.read_csv("Assignment1_Coforge_Pandas_CaseStudy/coforge_employees_50.csv")
prj_df = pd.read_csv("Assignment1_Coforge_Pandas_CaseStudy/coforge_projects.csv") 
print(emp_df.head())
merged = emp_df.merge(prj_df, on="ProjectID", how="left") 

print(emp_df.head(5))
print(emp_df.tail(5))

print(emp_df.shape)
print(emp_df.columns)
print(emp_df.dtypes)

print(emp_df.info())
print(emp_df.describe())

print(emp_df["Salary"].min())
print(emp_df["Salary"].max())
print(emp_df["Salary"].mean())

sum_salary=emp_df["Salary"].sum()
# print(sum)
total_annual_salary_expenditure=sum_salary*12
print(total_annual_salary_expenditure)

#youngest employees
min_age=emp_df["Age"].min()
# print(young)
youngest_emps=emp_df[emp_df["Age"]==min_age]
print(youngest_emps)

#oldest
max_age=emp_df["Age"].max()
oldest_emps=emp_df[emp_df["Age"]==max_age]
print(oldest_emps)

emp_df.groupby("Department")["EmployeeID"].count()

emp_df.groupby("Location")["EmployeeID"].count()

unique_desg=emp_df["Designation"].value_counts()
print(unique_desg)
unique_desg=emp_df["Designation"].nunique()
print(unique_desg)

res=emp_df[emp_df["Salary"]>1000000]
print(res)

res=emp_df[emp_df["PerformanceRating"] >= 4]
print(res)

emp_df.sort_values(by="Salary",ascending=False)

emp_df.sort_values(by="Salary",ascending=False).head(5)

emp_df.groupby("Department")["Salary"].mean()

emp_df.groupby("Designation")["Salary"].min()
emp_df.groupby("Designation")["Salary"].max()

emp_df.groupby("Location")["PerformanceRating"].mean()

emp_df.groupby(["Department" , "Gender"])["EmployeeID"].count()

res=emp_df[
    (emp_df["ExperienceYears"]>5) &
    (emp_df["PerformanceRating"]>=4)
]
print(res)

res=emp_df[emp_df["Location"].isin(["Pune","Mumbai","Noida"])]
print(res)

#22.
def categorize_salary(salary):
    if salary<200000:
        return "Low"
    elif salary<=500000:
        return "Medium"
    else:
        return "High"
emp_df["SalaryCategory"]=emp_df["Salary"].apply(categorize_salary)
print(emp_df)

#23
def performance_category(rating):
    if rating<3:
         return "Low"
    elif rating<=4:
          return "Medium"
    else:
         return "High"
emp_df["PerformanceCategory"]=emp_df["PerformanceRating"].apply(performance_category)
print(emp_df)

#25.
res=emp_df.groupby("Department")[["Salary", "Bonus"]].sum()
print(res)

#26
res=emp_df.groupby("Department")["TrainingHours"].mean()
print(res)

#27.
res=emp_df[emp_df["LeaveDays"] > 15]
print(res)

correlation = emp_df["Salary"].corr(emp_df["ExperienceYears"])
print(correlation)

corr=emp_df["TrainingHours"].corr(emp_df["PerformanceRating"])
print(corr)

res = emp_df.groupby(["Department", "Designation"]).agg(
    Headcount=("EmployeeID", "count"),
    MeanSalary=("Salary", "mean")
)
print(res)

count=emp_df.groupby("Department")["Salary"].count()
print(count)
min=emp_df.groupby("Department")["Salary"].min()
print(min)
max=emp_df.groupby("Department")["Salary"].min()
print(max)
mean=emp_df.groupby("Department")["Salary"].mean()
print(mean)

#32
salary_pivot = pd.pivot_table(
    emp_df,
    values="Salary",
    index="Department",
    columns="Location",
    aggfunc="mean"
)
print(salary_pivot)

#33
dept_wrkmode = pd.crosstab(
    emp_df["Department"],
    emp_df["WorkMode"]
)
print(dept_wrkmode)

#35
# Null values
print("Null values:",emp_df.isnull().sum())

# Duplicate rows
duplicates = emp_df.duplicated().sum()
print("\nDuplicate rows:", duplicates)

# Remove duplicate rows if aby
employees_clean = emp_df.drop_duplicates()

print("Shape after cleaning:", employees_clean.shape)

employee_project = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="inner"
)
print(employee_project.head())

inner_join = pd.merge(emp_df, prj_df, on="ProjectID", how="inner")
left_join = pd.merge(emp_df, prj_df, on="ProjectID", how="left")
right_join = pd.merge(emp_df, prj_df, on="ProjectID", how="right")
outer_join = pd.merge(emp_df, prj_df, on="ProjectID", how="outer")

print("Inner Join Rows :", len(inner_join))
print("Left Join Rows  :", len(left_join))
print("Right Join Rows :", len(right_join))
print("Outer Join Rows :", len(outer_join))

