import pandas as pd

# P01. Load the sales CSV into a DataFrame. 
df=pd.read_csv("Assignment3_Cadbury_DataAnalytics/Cadbury_Dairy_Milk_Sales_2025_Synthetic.csv")

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
print(df.info())

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
data_dictionary={
    "Order_ID":"unique order number",
    "Order_ID":"Unique order number",
    "Order_Date":"Date customer placed order",
    "Product_Name":"Chocolate product name",
    "Quantity":"Units sold",
    "Revenue_INR":"Sales revenue in INR",
    "Profit_INR":"Order profit in INR",
    "City":"Customer city",
    "Region":"Sales region"
}
print(data_dictionary)

# Pandas B | Cleaning and feature engineering (16-30) 