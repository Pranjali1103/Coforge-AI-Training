import pandas as pd
import numpy as np

#step2-Create panda series
salary_series=pd.Series([65000,58000,72000,80000,85000,68000,90000,76000])
print("=====================salary_series===========================") 
print(salary_series)
print("=====================Defining Properties=====================")
#check properties
print(salary_series.index)
print(salary_series.values)
print(salary_series.dtype)
#Step3-Series with Custom Index
employee_series=pd.Series(
    [
        "Shiv","Atharva","Sahil","Shreyansh","Prince","Hitesh","Akash","Pranjali"
    ],
    index=[
        "E101","E102","E103","E104","E105","E106","E107","E108"
    ]
)
print("===========Series with Custome Index=============")
print(employee_series)
#Retrieve employees:
print("===========Employee Name with E103=========================")
print(employee_series["E103"])
print("=========================Employee Name with E106==================================")
print(employee_series["E106"])
employee_data={
    "Employee_ID":[ "E101","E102","E103","E104","E105","E106","E107","E108"],
    "Employee_Name":["Shiv","Atharva","Sahil","Shreyansh","Prince","Hitesh","Akash","Pranjali"],
    "Department":["Sales","HR","Sales","Finance","IT","Sales","IT","Finance"],
    "City":["Delhi","Mumbai","Pune","Pune","Pune","Pune","Pune","Pune"],
    "Salary":[65000,89000,56000,67000,34000,56000,89000,340000],
    "Experience":[2,4,5,2,4,3,5,2],
    "Rating":[4,5,6,7,2,5,6,8]
}
employees_df=pd.DataFrame(employee_data)
print(employees_df)

#Step-5 Inspect Dataframe
print("===================DataFrame Shapes=======================")
print(employees_df.shape)
print(employees_df.columns)
print(employees_df.dtypes)

#Step-5- head()
print(employees_df.head())
print(employees_df.head(3))

#tail()
print(employees_df.tail())
print(employees_df.tail(3))

#describe
employees_df.info()
print(employees_df.describe())

#select one column
print("================Select One Column=====================")
print(employees_df["Employee_Name"])

#select multiple columns
print("========================Select Multiple Columns==============================")
print(employees_df[["Employee_Name","Salary"]])
# print(employees_df["Employee_Name","Salary"])
res=employees_df[employees_df["Salary"]>80000]
print(res)
res=employees_df[employees_df["Rating"]>4.5] 
print(res)
print(employees_df[employees_df["Department"] =="Sales"])
res_dept_sales=(employees_df[employees_df["Department"]=="Sales"])
print(res_dept_sales)
res_city_delhi=employees_df[
    employees_df["City"]=="Delhi"
]
print(res_city_delhi)

#multiple conditions
res=employees_df[
    (employees_df["Rating"]>4.5) &
    (employees_df["Salary"]>20000)
]
print(res)
res=employees_df[
    (employees_df["Department"]=="IT") |
    (employees_df["Department"]=="Finance")
]
print(res)

#isin
res=employees_df["Department"].isin(["IT","Finance"])

employees_df["Annual_salary"]=employees_df["Salary"]*12
print(employees_df)


employees_df["revised_salary"]=employees_df["Salary"]*1.08
print(employees_df)

employees_df["performance_bonus"]=employees_df["revised_salary"]*0.1
print(employees_df)

employees_df["compensation"]=employees_df["Salary"]+employees_df["performance_bonus"]
print(employees_df)
print("Avg salary:",employees_df["revised_salary"].mean())
print("Max salary:",employees_df["revised_salary"].max())
print("Min salary:",employees_df["revised_salary"].min())
print("Sum of total salary:",employees_df["revised_salary"].sum())
print("Average Rating::",employees_df["Rating"].mean())

#value_counts
count=employees_df["Department"].value_counts()
print(count)
print(len(employees_df["Department"]))

#nunique
un=employees_df["Department"].nunique()
print(un)