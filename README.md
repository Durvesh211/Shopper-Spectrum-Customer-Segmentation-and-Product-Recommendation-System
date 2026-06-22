#  Shopper Spectrum: Customer Segmentation and Product Recommendation System

##  Project Overview

This project analyzes customer purchasing behavior using transaction data from an e-commerce retail business. The objective is to identify meaningful customer segments using RFM (Recency, Frequency, Monetary) analysis and provide personalized product recommendations using Item-Based Collaborative Filtering.

The project combines data analytics, machine learning, and recommendation systems to help businesses improve customer retention, targeted marketing, and customer experience.

---

##  Objectives

* Analyze customer purchasing behavior.
* Perform customer segmentation using RFM analysis.
* Identify high-value, loyal, regular, occasional, and at-risk customers.
* Build an item-based product recommendation system.
* Generate actionable business insights from transaction data.

---

##  Dataset Features

| Feature     | Description                |
| ----------- | -------------------------- |
| InvoiceNo   | Transaction Number         |
| StockCode   | Product Code               |
| Description | Product Name               |
| Quantity    | Quantity Purchased         |
| InvoiceDate | Transaction Date           |
| UnitPrice   | Product Price              |
| CustomerID  | Unique Customer Identifier |
| Country     | Customer Country           |

---

##  Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Joblib
* Streamlit

---

##  Project Workflow

### 1. Data Preprocessing

* Removed missing Customer IDs
* Removed cancelled invoices
* Removed invalid quantities and prices
* Removed duplicate records

### 2. Exploratory Data Analysis

* Country-wise transaction analysis
* Top-selling products
* Sales trend analysis
* Customer spending analysis

### 3. RFM Analysis

* Recency
* Frequency
* Monetary

### 4. Customer Segmentation

* Standardized RFM values
* Applied K-Means Clustering
* Used Elbow Method and Silhouette Score for cluster selection
* Created customer segments:

  * VIP Customers
  * Loyal Customers
  * Regular Customers
  * Occasional Customers
  * At-Risk Customers

### 5. Product Recommendation System

* Created Customer-Product Matrix
* Applied Cosine Similarity
* Implemented Item-Based Collaborative Filtering
* Generated Top 5 product recommendations

---

##  Model Evaluation

### Clustering Metrics

* Elbow Method
* Silhouette Score
* Cluster Distribution Analysis

---

##  Project Structure

``
Shopper-Spectrum/
│
├── main.py
├── online_retail.csv
├── kmeans_model.pkl
├── scaler.pkl
├── product_similarity.pkl
├── requirements.txt
├── README.md
├── .gitignore
├── venv/
├── Lib/
└── Scripts/
```

##  Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run main.py
```

---

##  Application Features

### Customer Segmentation

* Input Recency, Frequency, and Monetary values
* Predict customer segment

### Product Recommendation

* Enter a product name
* Receive top 5 similar product recommendations

---

##  Conclusion

This project demonstrates the use of machine learning and recommendation systems in e-commerce analytics. By combining RFM-based customer segmentation with collaborative filtering, businesses can better understand customer behavior and deliver personalized experiences that drive growth and customer loyalty.
