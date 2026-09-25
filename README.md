# Shopper Spectrum --- Customer Segmentation & Product Recommendation System

## Live Application

**Try the deployed application:**\
https://customer-segmentation-recommendation.streamlit.app/

------------------------------------------------------------------------

## Project Overview

Shopper Spectrum is an end-to-end machine learning application for
analyzing e-commerce customer purchasing behavior.

The application provides two main capabilities:

1.  **Customer Segmentation** --- identifies a customer's purchasing
    segment using RFM analysis and a trained K-Means clustering model.
2.  **Product Recommendation** --- recommends products similar to a
    selected product using precomputed product-similarity results stored
    in SQLite.

The project is designed as a lightweight, deployable ML application
rather than only a notebook-based analysis.

------------------------------------------------------------------------

## Key Features

### Customer Segmentation

Users enter a **Customer ID** rather than manually entering RFM values.

The application:

1.  Finds the customer's precomputed RFM profile.
2.  Displays:
    -   Recency
    -   Frequency
    -   Monetary value
3.  Applies the trained `StandardScaler`.
4.  Uses the trained K-Means model to predict the customer cluster.
5.  Displays the corresponding customer segment.

### Product Recommendation

Users can:

-   Browse available products.
-   Search for a product using the Streamlit selector.
-   Choose how many recommendations to receive.
-   Retrieve up to **20 recommendations**.
-   View the similarity score for each recommendation.

Recommendations are stored in a compact **SQLite database** for fast
lookup instead of loading the original full product-similarity matrix
into the Streamlit application.

------------------------------------------------------------------------

## Application Architecture

``` text
                    ┌─────────────────────┐
                    │   E-commerce Data   │
                    │  online_retail.csv  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌──────────────────┐
        │   RFM Analysis  │        │ Product Similarity│
        │ Recency         │        │                  │
        │ Frequency       │        │ Cosine Similarity│
        │ Monetary        │        │                  │
        └────────┬────────┘        └────────┬─────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ StandardScaler  │        │ Top-20 Results   │
        └────────┬────────┘        │ SQLite Database  │
                 │                 └────────┬─────────┘
                 ▼                          │
        ┌─────────────────┐                 │
        │ K-Means Model   │                 │
        │ 5 Clusters      │                 │
        └────────┬────────┘                 │
                 │                          │
                 └────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │     Streamlit       │
                    │    Web Application  │
                    └─────────────────────┘
```

------------------------------------------------------------------------

## Customer Segmentation

### RFM Analysis

RFM represents three customer-behavior features:

  -----------------------------------------------------------------------
  Feature                             Meaning
  ----------------------------------- -----------------------------------
  **Recency**                         Number of days since the customer's
                                      most recent purchase

  **Frequency**                       Number of purchase transactions

  **Monetary**                        Total amount spent by the customer
  -----------------------------------------------------------------------

The RFM values are standardized using `StandardScaler` and passed to the
trained K-Means model.

### Customer Segments

The application maps the five K-Means clusters to business-oriented
segments:

-   VIP Customer
-   Loyal Customer
-   Regular Customer
-   Occasional Customer
-   At Risk Customer

The segment names are business labels assigned to the existing clusters;
they are not additional machine-learning classes.

------------------------------------------------------------------------

## Product Recommendation System

The recommendation module uses product-level similarity generated from
historical transaction data.

### Recommendation workflow

``` text
Historical Transactions
          ↓
Customer-Product Data
          ↓
Product Similarity
          ↓
Cosine Similarity
          ↓
Top-20 Similar Products
          ↓
SQLite Database
          ↓
Streamlit Lookup
```

The original product similarity matrix contains thousands of products
and is relatively large. Instead of loading the complete matrix during
application startup, the project stores only the **Top 20
recommendations for each product** in SQLite.

This reduces the runtime memory requirement and makes recommendation
retrieval a simple database lookup.

------------------------------------------------------------------------

## Dataset

The project uses an e-commerce transaction dataset containing fields
such as:

  Column          Description
  --------------- ----------------------------
  `InvoiceNo`     Transaction/invoice number
  `StockCode`     Product code
  `Description`   Product description
  `Quantity`      Quantity purchased
  `InvoiceDate`   Transaction date
  `UnitPrice`     Unit price
  `CustomerID`    Customer identifier
  `Country`       Customer country

The original transaction CSV is used locally for data preparation and is
intentionally excluded from Git through `.gitignore`.

A derived `customer_rfm.csv` file is used by the deployed application
for Customer ID-based segmentation.

------------------------------------------------------------------------

## Data Preparation

The transaction data is processed before model usage.

Typical preprocessing includes:

-   Removing records without a valid `CustomerID`.
-   Removing cancelled transactions.
-   Removing invalid quantities or prices.
-   Removing duplicate records.
-   Calculating customer-level RFM features.
-   Preparing product-level purchase information for recommendations.

The RFM dataset contains **4,339 customers**.

------------------------------------------------------------------------

## Machine Learning

### Customer Segmentation Model

**Algorithm:** K-Means Clustering

**Number of clusters:** 5

**Input features:**

``` text
Recency
Frequency
Monetary
```

**Preprocessing:**

``` text
StandardScaler
```

The trained model and scaler are stored as:

``` text
kmeans_model.pkl
scaler.pkl
```

The application loads these artifacts and performs inference when a
customer ID is entered.

------------------------------------------------------------------------

## Technology Stack

### Machine Learning & Data

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   Joblib

### Recommendation System

-   Cosine similarity
-   SQLite
-   Pandas

### Application

-   Streamlit

### Development & Deployment

-   Git
-   GitHub
-   Streamlit Community Cloud

------------------------------------------------------------------------

## Project Structure

``` text
Shopper-Spectrum-Customer-Segmentation-and-Product-Recommendation-System/
│
├── main.py
├── create_customer_rfm.py
├── create_recommendations.py
│
├── customer_rfm.csv
├── kmeans_model.pkl
├── scaler.pkl
├── top20_recommendations.db
│
├── requirements.txt
├── .gitignore
├── README.md
└── Shopper_Spectrum.ipynb
```

### Important files

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `main.py`                           Streamlit application

  `customer_rfm.csv`                  Customer-level RFM dataset used by
                                      the application

  `kmeans_model.pkl`                  Trained K-Means model

  `scaler.pkl`                        Fitted StandardScaler

  `top20_recommendations.db`          SQLite database containing Top-20
                                      product recommendations

  `create_customer_rfm.py`            Generates customer-level RFM data

  `create_recommendations.py`         Generates the compact SQLite
                                      recommendation database

  `requirements.txt`                  Python dependencies

  `Shopper_Spectrum.ipynb`            Original analysis and modelling
                                      notebook
  -----------------------------------------------------------------------

The original raw transaction dataset and the full product-similarity
matrix are kept out of Git because they are used as source/intermediate
artifacts rather than runtime application files.

------------------------------------------------------------------------

## Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/Durvesh211/Shopper-Spectrum-Customer-Segmentation-and-Product-Recommendation-System.git
cd Shopper-Spectrum-Customer-Segmentation-and-Product-Recommendation-System
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it on Windows:

``` powershell
venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start the application

``` bash
streamlit run main.py
```

The application will open in your browser.

------------------------------------------------------------------------

## Requirements

The project pins Scikit-learn to version `1.6.1` because the serialized
model artifacts were created with that version.

Current core dependencies include:

``` text
scikit-learn==1.6.1
streamlit
pandas
numpy
matplotlib
seaborn
joblib
```

------------------------------------------------------------------------

## How to Use the Application

### Customer Segmentation

1.  Open **Customer Segmentation** from the sidebar.
2.  Enter a valid **Customer ID**.
3.  Click **Find Customer**.
4.  The application retrieves the customer's RFM profile.
5.  Review the RFM metrics.
6.  View the predicted customer segment.

### Product Recommendation

1.  Open **Product Recommendation** from the sidebar.
2.  Search or browse for a product.
3.  Select the number of recommendations.
4.  Click **Get Recommended Products**.
5.  Review the recommended products and similarity scores.

------------------------------------------------------------------------

## Example Workflow

``` text
Customer ID
    ↓
Customer RFM Profile
    ↓
StandardScaler
    ↓
K-Means Prediction
    ↓
Customer Segment
```

and:

``` text
Selected Product
    ↓
SQLite Lookup
    ↓
Top-K Similar Products
    ↓
Similarity Scores
```

------------------------------------------------------------------------

## Limitations

-   The customer segments depend on the trained K-Means model and the
    RFM features used during training.
-   Customer segmentation is based on historical purchasing behavior and
    does not incorporate demographic or real-time behavioral
    information.
-   Product recommendations are based on historical product similarity
    and therefore do not represent real-time personalization.
-   The current application is intended as a portfolio/demo system
    rather than a production retail platform.
-   The recommendation database contains precomputed Top-20 results
    rather than recalculating similarity for every request.

------------------------------------------------------------------------

## Future Improvements

Potential future engineering improvements include:

-   Automated unit and integration tests.
-   GitHub Actions CI.
-   Code quality checks with Ruff.
-   Structured application logging.
-   Docker containerization.
-   MLflow experiment/model tracking.
-   Data and model validation.
-   Model monitoring and drift detection.
-   API deployment using FastAPI.
-   Periodic model/recommendation refresh pipelines.

These improvements can be added incrementally without changing the core
application architecture.

------------------------------------------------------------------------

## Project Goal

The goal of Shopper Spectrum is to demonstrate an end-to-end machine
learning workflow:

``` text
Data
 ↓
Preprocessing
 ↓
Feature Engineering
 ↓
Machine Learning
 ↓
Recommendation System
 ↓
Model Artifacts
 ↓
Application
 ↓
Cloud Deployment
```

The project combines **customer analytics, unsupervised machine
learning, recommendation systems, and application deployment** into a
single working application.

------------------------------------------------------------------------

## Live Demo

**Streamlit Application:**\
https://customer-segmentation-recommendation.streamlit.app/

**GitHub Repository:**\
https://github.com/Durvesh211/Shopper-Spectrum-Customer-Segmentation-and-Product-Recommendation-System
