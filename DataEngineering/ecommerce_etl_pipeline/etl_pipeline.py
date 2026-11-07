from pathlib import Path
import sqlite3
import pandas as pd

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
extract_data()

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
    customers["gender"] = (
          customers["gender"]
          .fillna("unknown")
          .astype(str)
          .str.strip()
          .str.title()
       )
    return customers
def clean_orders(orders:pd.DataFrame)->pd.DataFrame:
    orders=orders.copy()
    orders=orders.drop.duplicates(
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
            "metric":{"Total Orders"},
            "value":{total_orders}
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


    