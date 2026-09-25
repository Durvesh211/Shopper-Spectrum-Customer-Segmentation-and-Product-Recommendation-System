import pandas as pd

df = pd.read_csv("online_retail.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True)

df = df.dropna(subset=["CustomerID"])

df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

customer_rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
    Frequency=("InvoiceNo","nunique"),
    Monetary=("TotalAmount","sum")).reset_index()

customer_rfm.to_csv("customer_rfm.csv",index=False)

print("Customer RFM dataset created successfully.")
print(f"Customers: {len(customer_rfm)}")
print(customer_rfm.head())