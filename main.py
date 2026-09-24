import streamlit as st
import pandas as pd
import joblib
import sqlite3

st.title("Shopping Spectrum")
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
    recency = st.number_input("Recency(days)", min_value =0)
    frequency = st.number_input("Frequency",min_value = 0.0)
    monetary = st.number_input("Monetary",min_value = 0)
    if st.button("Predict Cluster"):
        input_data = pd.DataFrame([[recency, frequency, monetary]],
            columns=["Recency", "Frequency", "Monetary"])
        scaled =scaler.transform(input_data)
        cluster = kmeans.predict(scaled)[0]
        st.success(f"Predicted Cluster: {clusters[cluster]}")
else:
    st.header("Product Recommendation")

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
        "Number of recommendations",
        min_value=1,
        max_value=20,
        value=5
    )

    product_search = st.text_input("Enter Product Name", placeholder="Type part of a product name...")
    product = None
    if product_search:
        matching_products = products_df[products_df["product"].str.contains(product_search,case=False,na=False)]["product"].tolist()
        if matching_products:
            product = st.selectbox("Matching Products", matching_products)
        else:
            st.warning("No matching products found.")

    if st.button("Get Recommended Products"):
        if product is None:
            st.warning("Please select a product from the matching products.")
        else:

            connection = sqlite3.connect("top20_recommendations.db")

        query = """
              SELECT recommended_product, similarity
              FROM recommendations
              WHERE product = ?
              ORDER BY rank
              LIMIT ?
          """
        recommendations = pd.read_sql_query(    query,connection, params=[product, top_k])

        connection.close()

        if not recommendations.empty:

            st.subheader("Recommended Products")

            for i, row in recommendations.iterrows():
                st.write(f"{i + 1}. {row['recommended_product']}")

        else:
            st.error("Product not found. Please enter the exact product name.")
