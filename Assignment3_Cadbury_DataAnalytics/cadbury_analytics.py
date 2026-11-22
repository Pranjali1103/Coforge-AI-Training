import pandas as pd
import numpy as np

# P01. Load the sales CSV into a DataFrame. 
df=pd.read_csv("Cadbury_Dairy_Milk_Sales_2025_Synthetic.csv")

# Pandas A | Data loading and inspection (1-15) 

# P02. Display the first 10 records. 
print(df.head(10))

# P03. Display the last 10 records.
print(df.tail(10))

# P04. Find the number of rows and columns.
print(df.shape)

# P05. List all column names. 
print(df.columns)

# P06. Inspect column data types. 
print(df.dtypes)

# P07. Generate a concise DataFrame information summary. 
df.info() 

# P08. Calculate descriptive statistics for numeric fields. 
print(df.describe())

# P09. Calculate descriptive statistics for categorical fields
print(df.describe(include="object"))

# P10. Identify missing values by column. 
print(df.isnull().sum())

# P11. Count duplicate Order_ID values. 
print(df["Order_ID"].duplicated().sum())

# P12. Find unique product names and their count. 
print(df["Product_Name"].unique())
print(df["Product_Name"].nunique()) 

# P13. Find unique cities and regions. 
print(df["City"].unique())
print(df["Region"].unique())

# P14. Convert Order_Date to datetime and verify the result. 
df["Order_Date"]=pd.to_datetime(df["Order_Date"])
print(df["Order_Date"].dtype)

# P15. Create a data dictionary listing every field and its business meaning
data_dictionary = {
    "Order_ID": "Unique order identifier",
    "Order_Date": "Date the order was placed",
    "Region": "Sales region of the order",
    "City": "City where the order was placed",
    "Store_ID": "Unique store identifier",
    "Sales_Channel": "Channel through which the sale occurred",
    "Product_ID": "Unique product identifier",
    "Product_Name": "Name of the chocolate product",
    "Pack_Size_g": "Product pack size in grams",
    "Unit_MRP_INR": "Maximum retail price per unit in INR",
    "Discount_Pct": "Discount percentage applied",
    "Unit_Selling_Price_INR": "Actual selling price per unit after discount",
    "Quantity": "Number of units sold",
    "Gross_Sales_INR": "Total sales before discounts",
    "Net_Revenue_INR": "Revenue after discounts",
    "Unit_Cost_INR": "Cost of one unit",
    "Total_Cost_INR": "Total product cost for the order",
    "Delivery_Cost_INR": "Delivery expense for the order",
    "Profit_INR": "Profit earned from the order",
    "Payment_Method": "Mode of customer payment",
    "Customer_Age": "Age of the customer",
    "Customer_Segment": "Customer category or segment",
    "Customer_Rating": "Customer satisfaction rating",
    "Promotion_Flag": "Indicates whether a promotion was applied (1=Yes, 0=No)",
    "Returned_Flag": "Indicates whether the order was returned (1=Yes, 0=No)"
}
print(data_dictionary)


# Pandas B | Cleaning and feature engineering (16-30) 

# P16. Create a working copy without modifying raw data. 
df_copy=df.copy()
print(df_copy)

# P17. Remove exact duplicate records, if any. 
df_copy=df_copy.drop_duplicates()
# duplicates=df_copy.duplicated().sum()
# print("Duplicate Records:",duplicates)
print(df_copy.shape)

# P18. Apply a consistent naming convention to columns. 
print("Before:",df_copy.columns)
df_copy.columns=df_copy.columns.str.lower().str.strip()
print(df_copy.columns)

# P19. Validate that Quantity is positive. 
print(df_copy[df_copy["quantity"]<=0])
# print((df_copy["quantity"]>0).all())

# P20. Identify records with Discount_Pct outside 0-100. 
print(df_copy[
    (df_copy["discount_pct"]<0) |
    (df_copy["discount_pct"]>100)
      ])

# P21. Detect negative revenue, cost, or profit values and explain their meaning. 
print(df_copy[
    (df_copy["net_revenue_inr"]<0)|
    (df_copy["unit_cost_inr"]<0)|
    (df_copy["profit_inr"]<0)
])

# P22. Recalculate Net_Revenue_INR from Quantity and Unit_Selling_Price_INR. 
df_copy["recalculated_net_revenue_inr"]=(
    df_copy["quantity"] * df_copy["unit_selling_price_inr"]
)
print(df_copy[["quantity","unit_selling_price_inr","net_revenue_inr","recalculated_net_revenue_inr"]].head())

# P23. Compare recorded and recomputed revenue with a tolerance. 
tolerance=0.01
difference=abs(df_copy["net_revenue_inr"] - df_copy["recalculated_net_revenue_inr"])
print(df_copy[difference>tolerance])

# P24. Recalculate Profit_INR using revenue, costs, and delivery. 
df_copy["recalculated_profit_inr"] = (
    df_copy["net_revenue_inr"] - df_copy["total_cost_inr"] - df_copy["delivery_cost_inr"]
)
print(df_copy[["net_revenue_inr", "total_cost_inr", "delivery_cost_inr","profit_inr","recalculated_profit_inr"]].head())

# P25. Create Profit_Margin_Pct with safe division. 
df_copy["profit_margin_pct"]=np.where(
    df_copy["net_revenue_inr"]!=0,
    (df_copy["profit_inr"]/df_copy["net_revenue_inr"])*100,
    0
)
print(df_copy[["profit_inr","net_revenue_inr",
               "profit_margin_pct"]].head())


# P26. Create Year, Month, and Month_Name fields from Order_Date. 
df_copy["year"]=df_copy["order_date"].dt.year
df_copy["month"]=df_copy["order_date"].dt.month
df_copy["month_name"]=df_copy["order_date"].dt.month_name()
print(df_copy[["order_date","year","month","month_name"]].head())


# P27. Create Quarter and Weekday fields. 
df_copy["quarter"]=df_copy["order_date"].dt.quarter
df_copy["weekday"]=df_copy["order_date"].dt.day_name()

print(df_copy[["order_date" , "quarter" ,"weekday"]].head())


# P28. Create Weekend_Flag from Order_Date. 
df_copy["weekend_flag"]=df_copy["order_date"].dt.dayofweek>=5
print(df_copy[["order_date","weekend_flag"]])

# P29. Create Discount_Band categories (none, low, medium, high). 
df_copy["discount_band"]=pd.cut(
    df_copy["discount_pct"],
    bins=[-1,0,10,20,100],
    labels=["None","Low","Medium","High"]
)
print(df_copy[["discount_pct","discount_band"]].head())

# P30. Create Order_Value_Band using quantiles or defined thresholds. 
df_copy["order_value_band"]=pd.qcut(
    df_copy["net_revenue_inr"],
    q=4,
    labels=["Low","Medium","High","Very High"]
)
print(df_copy[["net_revenue_inr","order_value_band"]].head())

# P31. Select Order_ID, Product_Name, City, Quantity and Net_Revenue_INR.
print(df_copy[["order_id","product_name","city","quantity","net_revenue_inr"]])

# P32. Filter transactions from Mumbai. 
res=df_copy[df_copy["city"]=="Mumbai"]
print(res)       

# P33. Filter orders for Dairy Milk Silk. 
res=df_copy[df_copy["product_name"]=="Dairy Milk Silk"]
print(res)

# P34. Filter transactions with Quantity >= 10. 
print(df_copy[df_copy["quantity"]>=10].head())

# P35. Filter orders with Discount_Pct >= 15. 
print(df_copy[df_copy["discount_pct"]>=15])


# P36. Find loss-making orders where Profit_INR < 0
print(df_copy[df_copy["profit_inr"]<0])

# P37. Find orders from North region placed in Q4. 
print(df_copy[
    (df_copy["region"]=="North") &
    (df_copy["quarter"]==4)
])

# P38. Filter e-commerce orders paid by UPI. 
print(df_copy[
    (df_copy["sales_channel"]=="E-commerce") &
    (df_copy["payment_method"]=="UPI")
])

# P39. Find orders between two user-selected dates.
start_date="2025-01-01"
end_date="2025-03-31"

print(df_copy[df_copy["order_date"].
              between(start_date,end_date)])


# P40. Find orders where Product_Name contains Dairy Milk. 
print(df_copy[df_copy["product_name"].str.contains("Dairy Milk")])


# P41. Find transactions with Customer_Rating <= 2. 
print(df_copy[df_copy["customer_rating"]<=2])

# P42. Sort orders by Net_Revenue_INR descending. 
print(df_copy.sort_values(by="net_revenue_inr",ascending=False))

# P43. Show the top 20 orders by Profit_INR. 
print(df_copy.sort_values(by="profit_inr",ascending=False).head(20))

# P44. Sort by Region ascending then Quantity descending. 
print(df_copy.sort_values(by=["region","quantity"],ascending=[True,False]))

# P45. Select transactions meeting three simultaneous business conditions.
print(df_copy[
    (df_copy["quantity"]>=10) &
    (df_copy["discount_pct"]>=15) &
    (df_copy["profit_inr"]>0)
])

# Pandas D | Aggregation and business metrics (46-60) 

# P46. Calculate total net revenue. 
print(df_copy["net_revenue_inr"].sum())

# P47. Calculate total profit. 
print(df_copy["profit_inr"].sum())

# P48. Calculate total quantity sold. 
print(df_copy["quantity"].sum())

# P49. Calculate overall profit margin percentage. 
profit_margin=(
    df_copy["profit_inr"].sum()/
    df_copy["net_revenue_inr"].sum()
)*100
print(profit_margin)

# P50. Calculate average order value. 
print(df_copy["net_revenue_inr"].mean()) 

# P51. Count orders by Sales_Channel. 
print(df_copy["sales_channel"].value_counts())

# P52. Calculate revenue by Product_Name. 
print(df_copy.groupby("product_name")["net_revenue_inr"].sum())

# P53. Calculate profit by Region.
print(df_copy.groupby("region")["profit_inr"].sum()) 

# P54. Calculate units sold by City. 
print(df_copy.groupby("city")["quantity"].sum())

# P55. Find the top five products by revenue.
print(df_copy.groupby("product_name")["net_revenue_inr"].sum()
      .sort_values(ascending=False).head(5)
      )

# P56. Find the bottom five cities by profit. 
print(df_copy.groupby("city")["profit_inr"].sum()
      .sort_values().head(5))

# P57. Calculate mean and median discount by channel. 
print(df_copy.groupby("sales_channel")["discount_pct"].agg(["mean","median"]))


# P58. Calculate revenue and profit grouped by Region and Product_Name. 
print(df_copy.groupby(["region","product_name"])
      [["net_revenue_inr","profit_inr"]].sum()
      ) 


# P59. Calculate order count, revenue, and average rating by Customer_Segment. 
print(df_copy.groupby("customer_segment").
      agg(
          order_count=("order_id","count"),
          revenue=("net_revenue_inr","sum"),
          average_rating=("customer_rating","mean")
      )
      )

# P60. Calculate return rate by product using Returned_Flag
print(df_copy.groupby("product_name")["returned_flag"].mean()*100)

# Pandas E | Advanced analytics and joins (61-75) 

# P61. Build a monthly revenue trend table. 
print(df_copy.groupby(["month","month_name"])["net_revenue_inr"].sum())

# P62. Compute month-over-month revenue growth percentage. 
monthly_revenue=(
    df_copy.groupby("month")["net_revenue_inr"].sum()
)
print(monthly_revenue.pct_change()*100)


# P63. Build a quarterly profit comparison. 
print(df_copy.groupby("quarter")["profit_inr"].sum())


# P64. Create a pivot table: Region by Product_Name with revenue totals. 
pivotTable=pd.pivot_table(
    df_copy,
    values="net_revenue_inr",
    index="region",
    columns="product_name",
    aggfunc="sum"
)
print(pivotTable)

# P65. Create a pivot table: Sales_Channel by Month with order counts.
pivotTable=pd.pivot_table(
    df_copy,
    values="order_id",
    index="sales_channel",
    columns="month_name",
    aggfunc="count"
)
print(pivotTable)

# P66. Create a cross-tab of Customer_Segment versus Payment_Method. 
print(pd.crosstab(
            df_copy["customer_segment"],
            df_copy["payment_method"]
        )
)

daily_rev=df_copy.groupby(
    "order_date"
)["net_revenue_inr"].sum()

print(
    daily_rev.rolling(7).mean()
)

print(
    daily_rev.cumsum()
)

reg_prod=df_copy.groupby(
    ["region","product_name"]
)["net_revenue_inr"].sum()

print(
    reg_prod.groupby(level=0)
    .rank(ascending=False)
)

prod_share=(
    df_copy.groupby("product_name")
    ["net_revenue_inr"]
    .sum()
    /
    df_copy["net_revenue_inr"].sum()
)*100

print(prod_share)

prod_df=pd.read_csv(
    "Cadbury_Product_Master.csv"
)

store_df=pd.read_csv(
    "Cadbury_Store_Master.csv"
)

prod_df.columns = prod_df.columns.str.lower().str.strip()
store_df.columns = store_df.columns.str.lower().str.strip()


sales_prod=pd.merge(
    df_copy,
    prod_df,
    on="product_id",
    how="left"
)

print(sales_prod.head())

sales_store=pd.merge(
    df_copy,
    store_df,
    on="store_id",
    how="left"
)

print(sales_store.head())

sales_prod["mrp_diff"]=(
    sales_prod["unit_mrp_inr"]
    -
    sales_prod["standard_mrp_inr"]
)

print(
    sales_prod[
        [
            "product_id",
            "unit_mrp_inr",
            "standard_mrp_inr",
            "mrp_diff"
        ]
    ]
)
store_perf=sales_store.groupby(
    "store_id"
).agg(
    revenue=("net_revenue_inr","sum"),
    profit=("profit_inr","sum"),
    orders=("order_id","count"),
    avg_order_value=("net_revenue_inr","mean")
)

print(store_perf)

top_stores=store_perf.sort_values(
    by="revenue",
    ascending=False
)

print(top_stores.head(10))

import matplotlib.pyplot as plt
import seaborn as sns 

monthly_rev=df_copy.groupby("month")["net_revenue_inr"].sum()

plt.figure(figsize=(8,5))
plt.plot(monthly_rev.index,monthly_rev.values,marker="o")
plt.title("Monthly Net Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid(True)
plt.show()

print("Business Insight: Monthly revenue trend highlights peak and low performing months.")


monthly_profit=df_copy.groupby("month")["profit_inr"].sum()

plt.figure(figsize=(8,5))
plt.plot(monthly_profit.index,monthly_profit.values,marker="o",color="green")
plt.title("Monthly Profit")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.grid(True)
plt.show()

print("Business Insight: Profit trend helps identify periods of stronger profitability.")


prod_rev=df_copy.groupby("product_name")["net_revenue_inr"].sum().sort_values()

plt.figure(figsize=(8,5))
prod_rev.plot(kind="barh")
plt.title("Revenue by Product")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.show()

print("Business Insight: A few products contribute most of the revenue.")

reg_rev=df_copy.groupby("region")["net_revenue_inr"].sum()

reg_rev.plot(kind="bar",figsize=(8,5))
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.show()

print("Business Insight: Some regions outperform others in revenue generation.")

city_rev=df_copy.groupby("city")["net_revenue_inr"].sum().sort_values(ascending=False).head(10)

city_rev.plot(kind="bar",figsize=(10,5))
plt.title("Top 10 Cities by Revenue")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.show()

print("Business Insight: Top cities contribute a significant share of total sales.")

channel_rev=df_copy.groupby("sales_channel")["net_revenue_inr"].sum()

plt.figure(figsize=(6,6))
plt.pie(channel_rev,labels=channel_rev.index,autopct="%1.1f%%")
plt.title("Revenue Share by Sales Channel")
plt.show()

print("Business Insight: Revenue concentration across channels helps evaluate channel strategy.")

daily_rev=df_copy.groupby("order_date")["net_revenue_inr"].sum()

roll_avg=daily_rev.rolling(7).mean()

plt.figure(figsize=(10,5))
plt.plot(daily_rev.index,daily_rev.values,label="Revenue")
plt.plot(roll_avg.index,roll_avg.values,label="7-Day Avg")
plt.legend()
plt.title("Daily Revenue with 7 Day Moving Average")
plt.show()

print("Business Insight: The moving average smooths short-term revenue fluctuations.")


heat=df_copy.pivot_table(
    values="net_revenue_inr",
    index="region",
    columns="product_name",
    aggfunc="sum"
)

plt.figure(figsize=(10,5))
sns.heatmap(heat,cmap="YlGnBu")
plt.title("Product by Region Revenue Heatmap")
plt.show()

print("Business Insight: Heatmap highlights strongest product-region combinations.")

plt.figure(figsize=(8,5))
plt.hist(df_copy["discount_pct"],bins=20)
plt.title("Discount Percentage Distribution")
plt.xlabel("Discount")
plt.ylabel("Frequency")
plt.show()

print("Business Insight: Most discounts may be concentrated within a limited range.")

plt.figure(figsize=(8,5))
plt.hist(df_copy["quantity"],bins=20)
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Frequency")
plt.show()

print("Business Insight: Order quantity distribution reveals purchasing patterns.")


plt.figure(figsize=(8,5))
plt.scatter(
    df_copy["net_revenue_inr"],
    df_copy["profit_inr"]
)
plt.title("Revenue vs Profit")
plt.xlabel("Revenue")
plt.ylabel("Profit")
plt.show()

print("Business Insight: Higher revenue transactions generally contribute more profit.")


plt.figure(figsize=(8,5))
sns.regplot(
    x="discount_pct",
    y="quantity",
    data=df_copy
)
plt.title("Discount vs Quantity")
plt.show()

print("Business Insight: Shows whether discounts increase unit demand.")


plt.figure(figsize=(10,5))
sns.boxplot(
    x="product_name",
    y="profit_margin_pct",
    data=df_copy
)
plt.xticks(rotation=45)
plt.title("Profit Margin by Product")
plt.show()

print("Business Insight: Product profitability variability becomes easy to compare.")

qtr_rev=df_copy.groupby(
    ["quarter","region"]
)["net_revenue_inr"].sum().reset_index()

plt.figure(figsize=(10,5))
sns.barplot(
    data=qtr_rev,
    x="quarter",
    y="net_revenue_inr",
    hue="region"
)
plt.title("Quarterly Revenue by Region")
plt.show()

print("Business Insight: Quarterly comparison identifies seasonal regional performance.")


plt.figure(figsize=(10,5))
sns.countplot(
    data=df_copy,
    x="customer_rating",
    hue="sales_channel"
)
plt.title("Customer Ratings by Sales Channel")
plt.show()

<<<<<<< HEAD
print("Business Insight: Customer satisfaction patterns can be compared across channels.")
=======
print("Business Insight: Customer satisfaction patterns can be compared across channels.")
>>>>>>> 4815cfea9516beac7269297805b69865a2a3d05b
