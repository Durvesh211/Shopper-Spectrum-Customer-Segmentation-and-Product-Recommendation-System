import streamlit as st
import pandas as pd
import joblib
import sqlite3

st.title("Shopping Spectrum")
st.markdown(
    """
    ### Customer Segmentation & Product Recommendation System

    Shopper Spectrum is a machine learning application that helps
    understand **customer purchasing behaviour** and provides
    **product recommendations** based on historical purchase patterns.

    Use the menu on the left to explore the two modules.
    """)
st.divider()

selection = st.sidebar.selectbox("Select Module",["Customer Segmentation","Product Recommendation"])

scaler = joblib.load('scaler.pkl')
kmeans = joblib.load('kmeans_model.pkl')

clusters= {
    0: 'Occassional Customer',
    1: 'At risk customer',
    2: 'Loyal customer',
    3: 'Regular customer',
    4: 'VIP customer'
}


if selection == "Customer Segmentation":
    st.header("Customer Segmentation")
    st.markdown(
        """
        ### What does this module do?

        This module uses **RFM analysis** to understand customer
        purchasing behaviour and assigns the customer to a segment
        using a trained **K-Means clustering model**.

        **RFM stands for:**

        - **Recency** → How recently the customer purchased
        - **Frequency** → How often the customer purchased
        - **Monetary** → How much the customer spent
        """
    )
    customer_rfm = pd.read_csv("customer_rfm.csv")

    st.info("Enter a Customer ID to automatically retrieve their "
            "Recency, Frequency, and Monetary values.")
    st.markdown("For example: 17850")

    customer_id = st.number_input(
        "Enter Customer ID",
        min_value=1,
        step=1,
        help="Enter the Customer ID from the transaction dataset."
    )

    if st.button("Find Customer"):
        customer = customer_rfm[customer_rfm["CustomerID"] == customer_id]
        if customer.empty:
            st.error("Customer ID not found. Please check the ID and try again.")
        else:
            customer = customer.iloc[0]
            recency = int(customer["Recency"])
            frequency = int(customer["Frequency"])
            monetary = float(customer["Monetary"])

            st.success(f"Customer {int(customer_id)} found.")
            st.subheader("Customer RFM Profile")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Recency",f"{recency} days")
            with col2:
                st.metric("Frequency", frequency)

            with col3:
                st.metric("Monetary",f"{monetary:.2f}")

            input_data = pd.DataFrame(
                [[recency, frequency, monetary]],
                columns=[ "Recency", "Frequency","Monetary"]
            )
            scaled =scaler.transform(input_data)
            cluster = kmeans.predict(scaled)[0]
            st.success(f"Predicted Cluster: {clusters[cluster]}")

    with st.expander("⚙️ Model Information"):
        st.write("**Algorithm:** K-Means Clustering")
        st.write("**Number of clusters:** 5")
        st.write("**Features:** Recency, Frequency, Monetary")
        st.write("**Preprocessing:** StandardScaler")

else:
    st.header("Product Recommendation")

    st.markdown(
        """
        ### What does this module do?

        This module recommends products that are **similar to the
        product selected by the user**.

        The recommendations were generated from the historical
        product transaction data and stored in a lightweight
        SQLite database for fast retrieval.
        """
    )

    connection = sqlite3.connect("top20_recommendations.db")

    products_df = pd.read_sql_query(
        """
        SELECT DISTINCT product
        FROM recommendations
        ORDER BY product
        """,
        connection
    )

    connection.close()

    top_k = st.slider(
        "Number of recommendations",min_value=1,max_value=20,value=5)

    product = st.selectbox("Select or Search Product", products_df["product"].tolist(),index=None,  placeholder="Click to browse products or type to search...")

    if st.button("Get Recommended Products"):
        if product is None:
            st.warning("Please select a product from the match.")
        else:
            connection = sqlite3.connect("top20_recommendations.db")

            query = """
                  SELECT recommended_product, similarity
                  FROM recommendations
                  WHERE product = ?
                  ORDER BY rank
                  LIMIT ?
              """
            recommendations = pd.read_sql_query(query,connection, params=[product, top_k])

            connection.close()

            if not recommendations.empty:

                st.subheader("Recommended Products")

                for i, row in recommendations.iterrows():
                    st.write(f"{i + 1}. {row['recommended_product']}")

            else:
                st.error("Product not found. Please enter the exact product name.")

    with st.expander(" Recommendation System Information"):
        st.write("**Method:** Product similarity")
        st.write("**Storage:** SQLite")
        st.write("**Maximum recommendations:** 20")