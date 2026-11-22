from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Project Folder Locations

BASE_DIR=Path(__file__).resolve().parent
print(f"Base directory:{BASE_DIR}")

DATA_DIR=BASE_DIR/"data"
REPORT_DIR=BASE_DIR/"reports"
DATABASE_DIR=BASE_DIR/"database"
print(f"Data directory:{DATA_DIR}")
print(f"Report directory:{REPORT_DIR}")
print(f"Database directory:{DATABASE_DIR}")

DATABASE_PATH=DATABASE_DIR/"ecommerce_warehouse.db"
print(f"Database path:{DATABASE_PATH}")

# create required folders
def create_folders()-> None:
    """ create report and database """
    REPORT_DIR.mkdir(exist_ok=True)
    DATABASE_DIR.mkdir(exist_ok=True)


def extract_data()->tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame
]:
    customers_df=pd.read_csv(
        DATA_DIR / "customers.csv",
        encoding="utf-8-sig"
    )
    orders_df=pd.read_csv(
        DATA_DIR/"orders.csv",
        encoding="utf-8-sig"
    )
    payments_df=pd.read_csv(
        DATA_DIR /"payments.csv",
        encoding="utf-8-sig"
    )
    deliveries_df=pd.read_csv(
        DATA_DIR / "deliveries.csv",
        encoding="utf-8-sig"
    )

    # clean all column headings
    for dataframe in[
        customers_df,
        orders_df,
        payments_df,
        deliveries_df

    ]:
        dataframe.columns=(
            dataframe.columns
            .astype(str)
            .str.replace("\ufeff","",regex=False)
            .str.strip()
            .str.lower()
        )
        print("Customer columns",customers_df.columns.tolist())
        print("Order columns",orders_df.columns.tolist())
        print("Payment columns",payments_df.columns.tolist())
        print("Delivery columns",deliveries_df.columns.tolist())

    return customers_df,orders_df,payments_df,deliveries_df
# extract_data()

def clean_customers(customers:pd.DataFrame) -> pd.DataFrame:

    customers=customers.copy()
    customers=customers.drop_duplicates(
        subset=["customer_id"]
    )
    customers["customer_name"]=(
        customers["customer_name"]
        .fillna("Unknown customer")
        .astype(str)
        .str.strip()
        .str.title()
    )
    customers["email"] =(
        customers["email"]
        .fillna("unknown@gmail.com")
        .astype(str)
        .str.strip()
        .str.lower()
    )
    customers["city"] =(
            customers["city"]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
        )
    # customers["gender"] = (
    #       customers["gender"]
    #       .fillna("unknown")
    #       .astype(str)
    #       .str.strip()
    #       .str.title()
    #    )
    return customers
def clean_orders(orders:pd.DataFrame)->pd.DataFrame:
    orders=orders.copy()
    orders=orders.drop_duplicates(
            subset=["order_id"]
        )

    orders["customer_id"] = (
            orders["customer_id"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
       )
    orders["product_name"] = (
            orders["product_name"]
            .fillna("Unknown Product")
            .astype(str)
            .str.strip()
            .str.title()
       )
    orders["quantity"] = pd.to_numeric(
            orders["quantity"],
            errors="coerce"
      ).fillna(0)

    orders["unit_price"] = pd.to_numeric(
            orders["unit_price"],
            errors="coerce"
     ).fillna(0)

    orders["order_date"]= pd.to_datetime(
           orders["order_date"],
           errors="coerce"
         )
    orders["total_amount"]= (
        orders["quantity"]* orders["unit_price"]
    )

    return orders

def clean_payment(payments:pd.DataFrame)->pd.DataFrame:
    payments=payments.drop_duplicates(
        subset=["payment_id"]
    )
    payments["payment_status"]=(
        payments["payment_status"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )
    payments["payment_method"]=(
        payments["payment_method"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )
    payments["payment_date"]=pd.to_datetime(
             payments["payment_date"],
             errors="coerce"
    )

    return payments

def clean_deliveries( deliveries:pd.DataFrame)->pd.DataFrame:
    deliveries=deliveries.copy()
    deliveries=deliveries.drop_duplicates(
        subset=["delivery_id"]
    )
    deliveries["delivery_status"]=(
        deliveries["delivery_status"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )
    deliveries["delivery_city"]=(
        deliveries["delivery_city"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )
    return deliveries

def join_data(
        customers:pd.DataFrame,
        orders:pd.DataFrame,
        payments:pd.DataFrame,
        deliveries:pd.DataFrame
)-> pd.DataFrame:

    combined_data= orders.merge(
        customers,
        on="customer_id",
        how="left"
    )
    combined_data=combined_data.merge(
        payments,
        on="order_id",
        how="left"
    )

    combined_data=combined_data.merge(
        deliveries,
        on="order_id",
        how="left"
    )
    combined_data["customer_name"]=(
         combined_data["customer_name"]
         .fillna("Unknown Customer")
    )
    combined_data["city"]=(
             combined_data["city"]
             .fillna("Unknown")
    )
    combined_data["payment_status"]=(
             combined_data["payment_status"]
             .fillna("Unknown")
        )
    combined_data["delivery_status"]=(
        combined_data["delivery_status"]
        .fillna("Unknown")
    )
    return combined_data

def generate_total_orders_report(combined_data:pd.DataFrame)-> pd.DataFrame:
    total_orders=combined_data["order_id"].nunique()
    return pd.DataFrame(
        {
            "metric":["Total Orders"],
            "value":[total_orders]
        }
    )

def generate_total_revenue_report(combined_data:pd.DataFrame)->pd.DataFrame:
    successful_orders=combined_data[
        combined_data["payment_status"] == "Success"
    ]
    total_revenue=successful_orders["total_amount"].sum()
    return pd.DataFrame(
        {
            "metric":["Total Revenue"],
            "value":[total_revenue]
        }
    )

def generate_top_products_report(combined_data:pd.DataFrame)->pd.DataFrame:
    # Find the top 10 selling products

    successful_orders=combined_data[combined_data["payment_status"]=="Success"]

    top_products=(
        successful_orders
        .groupby("product_name",as_index=False)
        .agg(
            total_quantity_sold=("quantity","sum"),
            total_product_revenue=("total_amount","sum")
        ).sort_values(by="total_quantity_sold",ascending=False).head(10)
    )
    return top_products

def generate_top_customers_report(combined_data:pd.DataFrame)->pd.DataFrame:
    """Find the top 10 customers report"""
    successful_orders=combined_data[combined_data["payment_status"]=="Success"]
    top_customers=(
        successful_orders.groupby(
            ["customer_id","customer_name"],as_index=False
        ).agg(
            total_orders=("order_id","nunique"),
            total_spent=("total_amount","sum"))
        .sort_values(
            by="total_spent",ascending=False
        ).head(10)
    )
    return top_customers

def generate_failed_payments_report(combined_data:pd.DataFrame)->pd.DataFrame:
    failed_payments=combined_data[combined_data["payment_status"]=="Failed"]
    required_columns=[
        "payment_id",
        "order_id",
        "customer_id",
        "customer_name",
        "product_name",
        "total_amount",
        "payment_method",
        "payment_status"
    ]
    return failed_payments[required_columns]

def save_reports(
        total_orders_report:pd.DataFrame,
        total_revenue_report:pd.DataFrame,
        top_products_report:pd.DataFrame,
        top_customers_report:pd.DataFrame,
        failed_payments_report:pd.DataFrame,
)->None:
    """Save all generated reports as CSV files"""

    total_orders_report.to_csv(
        REPORT_DIR/"total_orders.csv",
        index=False
    )
    total_revenue_report.to_csv(
            REPORT_DIR/"total_revenue.csv",
            index=False
    )
    top_products_report.to_csv(
            REPORT_DIR/"top_products.csv",
            index=False
    )
    top_customers_report.to_csv(
            REPORT_DIR/"top_customers.csv",
            index=False
    )
    failed_payments_report.to_csv(
            REPORT_DIR/"failed_payments.csv",
            index=False
    )

def create_sales_line_chart(combined_data):

    sales=combined_data[
        combined_data["payment_status"] == "Success"
    ].copy()

    sales=sales.dropna(subset=["order_date"])

    daily_sales=(
        sales.groupby("order_date")["total_amount"]
        .sum().sort_index()
    )

    plt.figure(figsize=(10,5))
    plt.plot(
        daily_sales.index,
        daily_sales.values,
        marker="o",
        color="blue"
    )
    plt.title("Daily Sales Revenue")
    plt.xlabel("Order Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(REPORT_DIR/"sales_line_chart.png")
    plt.close()


# without duplicates
def create_payment_pie_chart(combined_data):
    payment_counts=(
        combined_data.drop_duplicates(subset=["payment_id"])["payment_status"].value_counts()
    )

    # not removing duplicates
    payment_counts_1=(
        combined_data["payment_status"].value_counts()
    )
    print("Payment Status Counts\n",payment_counts)
    print("Payment Status Counts 1\n",payment_counts_1)

    plt.figure(figsize=(7,7)) 
    plt.pie(
        payment_counts.values,
        labels=payment_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Payment Status Distribution")
    plt.tight_layout()
    plt.savefig(REPORT_DIR/"payment_pie_chart.png")
    plt.close()


# with duplicates
def create_payment1_pie_chart(combined_data):
    payment_counts_1=(
        combined_data["payment_status"].value_counts()
    )
    print("Payment Status Counts 1\n",payment_counts_1)

    plt.figure(figsize=(7,7)) 
    plt.pie(
        payment_counts_1.values,
        labels=payment_counts_1.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Payment Status Distribution")
    plt.tight_layout()
    plt.savefig(REPORT_DIR/"payment1_pie_chart.png")
    plt.close()


# Main ETL Pipeline
def run_etl_pipeline()->None:

     """Execute the complete ETL pipeline"""

     print("Starting E-Commerce ETL pipeline....")
     create_folders()

     print("Step1:Extracting data...")
     customers,orders,payments,deliveries=extract_data()

     print("Step1: Cleaning customer data....")
     customers=clean_customers(customers)

     print("Step3: Cleaning order data...")
     orders=clean_orders(orders)

     print("Step4: Cleaning payment data... ")
     payments=clean_payment(payments)

     print("Step5: Cleaning delivery data...")
     deliveries=clean_deliveries(deliveries)

     print("Step6: Joining datasets....")
     combined_data=join_data(
         customers,
         orders,
         payments,
         deliveries
     )

     print("Step7: Generating Reports....")
     total_orders_report=generate_total_orders_report(combined_data)

     total_revenue_report=generate_total_revenue_report(combined_data)

     top_products=generate_top_products_report(combined_data)

     print("\nTotal Orders Report")
     print(total_orders_report)

     print("\nTotal Revenue Report")
     print(total_revenue_report)

     print(top_products)

     top_customers=generate_top_customers_report(combined_data)
     print(top_customers)

     failed_payments_report=generate_failed_payments_report(combined_data)
     print(failed_payments_report)


     print("/nSave Reports....")
     save_reports(total_orders_report,total_revenue_report,top_products,top_customers,failed_payments_report)

     print("\nETL Pipeline completed successfully:")
     print(f"Reports folder:{REPORT_DIR}")
     print(f"Database location:{DATABASE_PATH}")

     create_sales_line_chart(combined_data)
     create_payment_pie_chart(combined_data)
     create_payment1_pie_chart(combined_data)


if __name__=="__main__":
         run_etl_pipeline()
         






    