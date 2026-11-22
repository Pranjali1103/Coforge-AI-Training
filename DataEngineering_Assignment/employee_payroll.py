import pandas as pd
import numpy as np

# 1. Load CSV and inspect first/last 10 records 
df=pd.read_csv("employee_payroll.csv")
print(df.head(10))
print(df.tail(10))

# 2. Inspect shape, columns, and dtypes
print(df.shape)
print(df.columns)
print(df.dtypes)
df.info()

# 3. Generate descriptive statistics 
print(df.describe())

# 4. Detect missing values
print(df.isnull().sum()) # missing values in each column
print(df.isnull().sum().sum())  #total 


# 5. Remove duplicate employee-month rows 
duplicates=df.duplicated(subset=["EmployeeID","PayrollMonth"]).sum()
df=df.drop_duplicates(
    subset=["EmployeeID","PayrollMonth"]
)

# 6. Impute missing salary and bonus values using documented rules 
df["BasicSalary"]=(
    df["BasicSalary"]
    .fillna(df["BasicSalary"].median())
)
df["Bonus"]=(
    df["Bonus"]
    .fillna(0)
)
print(df[["BasicSalary","Bonus"]].isnull().sum())

# 7. Standardize department and city names
print(df["Department"].unique())
print(df["City"].unique()) 

df["Department"]=df["Department"].str.upper().str.strip()
df["City"]=df["City"].str.title().str.strip()

print(df["Department"].unique())
print(df["City"].unique()) 

df["Department"]=df["Department"].replace({
    "IINFORMATION TECH":"IT",
    "FIN":"FINANCE",
    "OPS":"OPERATIONS",
    "HUMAN RESOURCES":"HR"
})
df["City"]=df["City"].replace({
    "Bangalore":"Bengaluru"
})

print(df["Department"].unique())
print(df["City"].unique()) 

# 8. Convert joining and payroll dates 
df["JoiningDate"]=pd.to_datetime(df["JoiningDate"])
df["PayrollMonth"]=pd.to_datetime(df["PayrollMonth"])

# 9. Filter salaries above ₹75,000 
print(df[df["BasicSalary"]>75000])

# 10. Sort by salary 
print(df.sort_values(by="BasicSalary"))
print(df.sort_values(by="BasicSalary",ascending=False))

# 11. Calculate gross salary (BasicSalary + HRA + Bonus) 
df["GrossSalary"]=df["BasicSalary"]+df["HRA"]+df["Bonus"]
print([["EmployeeName","GrossSalary"]])

# 12. Calculate net salary (GrossSalary − Deductions) 
df["NetSalary"]=df["GrossSalary"]-df["Deductions"]
print(df[["EmployeeName","NetSalary"]])

# 13. Calculate attendance percentage 
df["AttendancePct"]=(df["PresentDays"]/df["WorkingDays"])*100
print(df[["EmployeeName","AttendancePct"]])

# 14. Categorize salaries using np.where or np.select 
conditions=[
    df["BasicSalary"]<40000,
    (df["BasicSalary"]>=40000) & (df["BasicSalary"]<=60000),
    df["BasicSalary"]>60000
]
choices=["Low","Medium","High"]
df["SalaryCategory"]=np.select(conditions,choices,default="other")
print(df[["BasicSalary","SalaryCategory"]])

# 15. Group by department 
print(df.groupby("Department"))

# 16. Calculate department-wise average salary 
print(df.groupby("Department")["BasicSalary"].mean())

# 17. Identify top 10 highest-paid employees 
print(df.nlargest(10,"NetSalary"))

# 18. Build department-wise payroll pivot table 
pivot=pd.pivot_table(
    df,
    values="NetSalary",
    index="Department",
    columns="PayrollMonth",
    aggfunc="sum"
)
print(pivot)

# 19. Validate negative salaries, attendance limits and IDs 
print(df[df["BasicSalary"]<=0].head(5))
att=df[
    (df["WorkingDays"]<=0)|
    (df["PresentDays"]<0)|
    (df["PresentDays"]>df["WorkingDays"])
]
print(att.head(5))

# 20. Export cleaned/transformed CSV
df.to_csv("cleaned_employee_payroll.csv",index=False)
print("CLEANED CSV EXPORTED!")



