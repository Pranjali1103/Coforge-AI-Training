import pandas as pd
import numpy as np

df=pd.read_csv("Assignment2_HSBC_Banking_Analytics/HSBC_Synthetic_Banking_Customers.csv")

balances=df["Account_Balance"].to_numpy()
print(balances)

# inspect array
print(balances.ndim)
print(balances.shape)
print(balances.dtype)

print("Min Balance:",np.min(balances))
print("Max Balance:",np.max(balances))

print("Sum:", np.sum(balances))
print("Mean:", np.mean(balances))
print("Median:", np.median(balances))
print("Standard Deviation:", np.std(balances))

print(np.percentile(balances,25))
print(np.percentile(balances,50))
print(np.percentile(balances,75))

res=balances[balances>500000]
print("Balance above 500000:",res)

res=df[df["Credit_Score"]<650];
print(res)

asc=np.sort(balances)
desc=np.sort(balances)[::-1]
print(asc)
print(desc)

total_deposits = df["Monthly_Deposit"].sum()
total_withdrawals = df["Monthly_Withdrawal"].sum()
print("Total Deposits:", total_deposits)
print("Total Withdrawals:", total_withdrawals)


new_balances = balances * 1.05
print(new_balances)

df["Bal_Class"] = np.where(
    df["Account_Balance"] > 500000,"High","Low"
    
)
# print(df)
print(df[["Account_Balance", "Bal_Class"]])


categories=np.select(
    [balances<100000,(balances >= 100000) & (balances <= 500000),
        balances > 500000],["Low","Mesium","High"], default="Unknown"
)
print(categories)

 
df["Deposit_Income_Ratio"]=np.where(
    df["Monthly_Income"]!=0,
    df["Monthly_Deposit"]/df["Monthly_Income"],0
)
print(df[["Customer_ID","Deposit_Income_Ratio"]])

# //using numpy
deposits = df["Monthly_Deposit"].to_numpy()
withdrawals = df["Monthly_Withdrawal"].to_numpy()
result = withdrawals > deposits
print(df[result])

credit_scores = df["Credit_Score"].to_numpy()
scores, counts = np.unique(
    credit_scores,
    return_counts=True
)
print(scores)
print(counts)

five_largest_balnces= np.argsort(balances)[-5:][::-1]
print(balances[five_largest_balnces])
min_balance = balances.min()
max_balance = balances.max()
if min_balance == max_balance:
    normalized_balances = np.zeros_like(balances, dtype=float)
else:
    normalized_balances = (balances - min_balance) / (max_balance - min_balance)
print(normalized_balances)

mean_bal = np.mean(balances)
std_bal = np.std(balances)

if std_bal== 0:
    z_scores = np.zeros_like(balances, dtype=float)
else:
    z_scores = (balances - mean_bal) / std_bal

print(z_scores)

banking_data = np.column_stack((
    df["Account_Balance"],
    df["Monthly_Deposit"],
    df["Monthly_Withdrawal"]
))

print(np.sum(banking_data, axis=0))
print(np.sum(banking_data, axis=1))

correlation = np.corrcoef(
    df["Monthly_Income"],
    df["Account_Balance"]
)[0, 1]
print("Pearson Correlation:", correlation)


# 22. Display first and last ten rows. 
print(df.head(10))
print(df.tail(10))

# 23. Inspect shape, columns, dtypes and info(). 
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())

# 24. Generate numerical descriptive statistics using describe(). 
print(df.describe())

# 25. Check missing values and duplicate Customer_ID values. 
print(df.isnull().sum())
print(df["Customer_ID"].duplicated().sum())

# 26. Select customer name, city, balance and credit score columns. 
print(df[["Customer_Name","City","Account_Balance","Credit_Score"]])

# 27. Filter customers aged 25 through 40 inclusive. 
print(df[(df["Age"]>=25)& (df["Age"]<=40)]["Age"])

# 28. Find active Savings accounts. 
print(df[(df["Account_Type"]=="Savings")&(df["Account_Status"]=="Active")])
# print(df[(df["Account_Type"]=="Savings")&(df["Account_Status"]=="Active")]["Account_Type"])
# print(df[(df["Account_Type"]=="Savings")&(df["Account_Status"]=="Active")][["Account_Type","Account_Status"]])

# 29. Sort by balance and monthly income, descending. 
print(df.sort_values(by=["Account_Balance","Monthly_Income"],ascending=False))
# print(df.sort_values(by=["Account_Balance","Monthly_Income"],ascending=False)[["Account_Balance","Monthly_Income"]])

df["Net_Monthly_Flow"]=df["Monthly_Deposit"]-df["Monthly_Withdrawal"]
print(df["Net_Monthly_Flow"])

# 31. Group by City and calculate total Account_Balance.
print(df.groupby("City")["Account_Balance"].sum())

# 32. Group by Account_Type and calculate average Monthly_Income. 
print(df.groupby("Account_Type")["Monthly_Income"].mean()) 

# 33. Compute branch-wise deposit and withdrawal totals. 
print(df.groupby("Branch")[["Monthly_Deposit","Monthly_Withdrawal"]].sum())

# 34. Use agg to report minimum, maximum, mean and median balances by branch.
print(df.groupby("Branch")["Account_Balance"].agg(["min","max","mean","median"])) 

# 35. Create a pivot table of total balance by City and Account_Type.
pv=pd.pivot_table(
    df,
    values="Account_Balance",
    index="City",
    columns="Account_Type",
    aggfunc="sum"
)
print(pv)

# 36. Use pd.cut to create age groups: 18–25, 26–40, 41–60 and 61+
df["Age_Group"]=pd.cut(
   df["Age"],
   bins=[18,25,40,60,100],
   labels=["18-25","26-40","41-60","61+"]
)
print(df[["Age","Age_Group"]])

# 37. Use groupby().transform() to calculate each customer’s balance minus branch average. 
df["Balance_Minus_Branch_Avg"]=df["Account_Balance"]-df.groupby("Branch")["Account_Balance"].transform("mean")
print(df[["Branch","Account_Balance","Balance_Minus_Branch_Avg"]])

# 38. Create a separate Branch_Details DataFrame with Branch and Region; merge it on Branch and validate the join. 
# print(df["Branch"].unique())
Branch_Details=pd.DataFrame({
    "Branch":["Pune Main", "Mumbai Main","Bengaluru Main","Delhi Main","Hyderabad Main"],
    "Region": ["West","West","South","North","South"]
})
merged_df=df.merge(
    Branch_Details,
    on="Branch",
    how="left",
    validate="many_to_one"
)
print(merged_df[["Branch","Region"]])

# 39. Find the top three customers by balance within each City.
# print(df.groupby("City")["Account_Balance"].nlargest(3))

print(df.groupby("City").apply(lambda x:x.nlargest(3,"Account_Balance")))


# 40. Create a branch summary with total balance, mean credit score, counts by account status and total net monthly flow. 
branch_summary=df.groupby("Branch").agg(
    Total_Bal=("Account_Balance","sum"),
    Mean_Credit_Score=("Credit_Score","mean"),
    Active_Count=("Account_Status",
                  lambda x:(x == "Active").sum()),
    Inactive_count=("Account_Status",
                    lambda x:(x=="Inactive").sum()) ,
    
    Total_Net_Monthly_Flow=("Net_Monthly_Flow","sum")
)
print(branch_summary[["Total_Bal","Mean_Credit_Score","Active_Count","Inactive_count","Total_Net_Monthly_Flow"]])
















