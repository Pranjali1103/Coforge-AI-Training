import pandas as pd
import numpy as np

emp_df = pd.read_csv("Assignment1_Coforge_Pandas_CaseStudy/coforge_employees_50.csv")
prj_df = pd.read_csv("Assignment1_Coforge_Pandas_CaseStudy/coforge_projects.csv")

print(emp_df.head())

print(emp_df.head(5))
print(emp_df.tail(5))

print(emp_df.shape)
print(emp_df.columns)
print(emp_df.dtypes)

emp_df.info()
print(emp_df.describe())

print(emp_df[["EmployeeName","Department","Salary","PerformanceRating"]])

print(emp_df["Salary"].min())
print(emp_df["Salary"].max())
print(emp_df["Salary"].mean())

print(emp_df["Salary"].sum())

mn_age = emp_df["Age"].min()
mx_age = emp_df["Age"].max()

print(emp_df[emp_df["Age"] == mn_age])
print(emp_df[emp_df["Age"] == mx_age])

print(emp_df.groupby("Department")["EmployeeID"].count())

print(emp_df.groupby("Location")["EmployeeID"].count())

print(emp_df["Designation"].value_counts())
print(emp_df["Designation"].nunique())

print(emp_df[emp_df["Salary"] > 1000000])

print(emp_df[emp_df["PerformanceRating"] >= 4])

print(emp_df.sort_values(by="Salary", ascending=False))

print(
    emp_df.sort_values(
        by="Salary",
        ascending=False
    ).head(5)
)

print(
    emp_df.groupby("Department")
    ["Salary"]
    .mean()
)

print(
    emp_df.groupby("Designation")
    ["Salary"]
    .agg(["min","max"])
)

print(
    emp_df.groupby("Location")
    ["PerformanceRating"]
    .mean()
)

print(
    emp_df.groupby(
        ["Department","Gender"]
    )["EmployeeID"]
    .count()
)

res = emp_df[
    (emp_df["ExperienceYears"] > 5) &
    (emp_df["PerformanceRating"] >= 4)
]

print(res)

print(
    emp_df[
        emp_df["Location"].isin(
            ["Pune","Mumbai","Noida"]
        )
    ]
)

def sal_cat(x):
    if x < 700000:
        return "Low"
    elif x < 1200000:
        return "Medium"
    else:
        return "High"

emp_df["SalaryCategory"] = emp_df["Salary"].apply(sal_cat)

print(
    emp_df[
        ["EmployeeName","Salary","SalaryCategory"]
    ]
)

def perf_cat(x):
    if x < 3:
        return "Low"
    elif x < 4:
        return "Medium"
    else:
        return "High"

emp_df["PerformanceCategory"] = (
    emp_df["PerformanceRating"]
    .apply(perf_cat)
)

print(
    emp_df[
        ["EmployeeName",
         "PerformanceRating",
         "PerformanceCategory"]
    ]
)

emp_df["SalPerExp"] = np.where(
    emp_df["ExperienceYears"] > 0,
    emp_df["Salary"] /
    emp_df["ExperienceYears"],
    np.nan
)

print(
    emp_df[
        ["EmployeeName",
         "Salary",
         "ExperienceYears",
         "SalPerExp"]
    ]
)

print(
    emp_df.groupby("Department")
    [["Salary","Bonus"]]
    .sum()
)

print(
    emp_df.groupby("Department")
    ["TrainingHours"]
    .mean()
)

print(
    emp_df[
        emp_df["LeaveDays"] > 15
    ]
)

print(
    emp_df["Salary"]
    .corr(emp_df["ExperienceYears"])
)

print(
    emp_df["TrainingHours"]
    .corr(emp_df["PerformanceRating"])
)

print(
    emp_df.groupby(
        ["Department","Designation"]
    ).agg(
        HeadCount=("EmployeeID","count"),
        MeanSalary=("Salary","mean")
    )
)

print(
    emp_df.groupby("Department")
    .agg(
        Count=("Salary","count"),
        MinSalary=("Salary","min"),
        MaxSalary=("Salary","max"),
        MeanSalary=("Salary","mean"),
        MedianSalary=("Salary","median")
    )
)

pvt = pd.pivot_table(
    emp_df,
    values="Salary",
    index="Department",
    columns="Location",
    aggfunc="mean"
)

print(pvt)

ct = pd.crosstab(
    emp_df["Department"],
    emp_df["WorkMode"]
)

print(ct)

emp_df["JoiningDate"] = pd.to_datetime(
    emp_df["JoiningDate"]
)

tdy = pd.Timestamp.today()

emp_df["TenureYears"] = (
    (tdy - emp_df["JoiningDate"]).dt.days / 365
).round(2)

print(
    emp_df[
        ["EmployeeName",
         "JoiningDate",
         "TenureYears"]
    ]
)

print(emp_df.isnull().sum())

dup = emp_df.duplicated().sum()

print(dup)

emp_clean = emp_df.drop_duplicates()

print(emp_clean.shape)

mrg = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="left"
)

print(mrg.head())

inn = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="inner"
)

lft = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="left"
)

rgt = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="right"
)

otr = pd.merge(
    emp_df,
    prj_df,
    on="ProjectID",
    how="outer"
)

print(len(inn))
print(len(lft))
print(len(rgt))
print(len(otr))

print(
    mrg[
        mrg["ProjectBudgetINR"] > 10000000
    ][[
        "EmployeeName",
        "ProjectName",
        "ProjectBudgetINR"
    ]]
)

emp_df["SalRank"] = (
    emp_df.groupby("Department")
    ["Salary"]
    .rank(ascending=False)
)

print(
    emp_df[
        ["EmployeeName",
         "Department",
         "Salary",
         "SalRank"]
    ]
)

top3 = (
    emp_df.sort_values(
        ["Department","Salary"],
        ascending=[True,False]
    )
    .groupby("Department")
    .head(3)
)

print(
    top3[
        ["EmployeeName",
         "Department",
         "Salary"]
    ]
)

emp_df["SalDiff"] = (
    emp_df["Salary"]
    -
    emp_df.groupby("Department")
    ["Salary"]
    .transform("mean")
)

print(
    emp_df[
        ["EmployeeName",
         "Department",
         "SalDiff"]
    ]
)

pct = emp_df["Salary"].quantile(
    [0.25,0.50,0.75,0.90]
)

print(pct)

q1 = emp_df["Salary"].quantile(0.25)
q3 = emp_df["Salary"].quantile(0.75)

iqr = q3 - q1

low = q1 - (1.5 * iqr)
up = q3 + (1.5 * iqr)

out = emp_df[
    (emp_df["Salary"] < low)
    |
    (emp_df["Salary"] > up)
]

print(out)

emp_df["npr"] = (
    emp_df["PerformanceRating"]
    -
    emp_df["PerformanceRating"].min()
) / (
    emp_df["PerformanceRating"].max()
    -
    emp_df["PerformanceRating"].min()
)

emp_df["nth"] = (
    emp_df["TrainingHours"]
    -
    emp_df["TrainingHours"].min()
) / (
    emp_df["TrainingHours"].max()
    -
    emp_df["TrainingHours"].min()
)

emp_df["npc"] = (
    emp_df["ProjectsCompleted"]
    -
    emp_df["ProjectsCompleted"].min()
) / (
    emp_df["ProjectsCompleted"].max()
    -
    emp_df["ProjectsCompleted"].min()
)

emp_df["WScore"] = (
      0.5 * emp_df["npr"]
    + 0.2 * emp_df["nth"]
    + 0.3 * emp_df["npc"]
)

print(
    emp_df[
        ["EmployeeName","WScore"]
    ]
)

mi = emp_df.set_index(
    ["Department","Location"]
)

print(mi.head())

print(mi.loc["IT"])

emp_df["Year"] = (
    emp_df["JoiningDate"].dt.year
)

emp_df["Quarter"] = (
    emp_df["JoiningDate"].dt.quarter
)

print(
    emp_df.groupby("Year")
    ["EmployeeID"]
    .count()
)

print(
    emp_df.groupby(
        ["Year","Quarter"]
    )
    ["EmployeeID"]
    .count()
)

emp_df = emp_df.sort_values(
    ["Department","Salary"]
)

emp_df["CumSal"] = (
    emp_df.groupby("Department")
    ["Salary"]
    .cumsum()
)

print(
    emp_df[
        ["Department",
         "Salary",
         "CumSal"]
    ]
)

def promo(r):
    if (
        r["PerformanceRating"] >= 4 and
        r["ExperienceYears"] >= 3 and
        r["ProjectsCompleted"] >= 5
    ):
        return "Eligible"
    return "Not Eligible"

emp_df["Promotion"] = emp_df.apply(
    promo,
    axis=1
)

print(
    emp_df[
        ["EmployeeName",
         "Promotion"]
    ]
)

scr = (
    emp_df.groupby("Department")
    .agg(
        EmpCnt=("EmployeeID","count"),
        AvgSal=("Salary","mean"),
        AvgPerf=("PerformanceRating","mean"),
        AvgTrain=("TrainingHours","mean"),
        TotProj=("ProjectsCompleted","sum")
    )
    .sort_values(
        by="AvgPerf",
        ascending=False
    )
)

print(scr)

emp_clean.to_csv(
    "cleaned_employees.csv",
    index=False
)

mrg.to_csv(
    "project_enriched_data.csv",
    index=False
)

scr.to_csv(
    "department_scorecard.csv"
)

top3.to_csv(
    "top_performers.csv",
    index=False
)
