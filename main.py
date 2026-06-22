import streamlit as st
import pandas as pd
import joblib

st.title("Shopping")
selection = st.sidebar.selectbox("Select Module",["Customer Segmentation","Product Recommendation"])

scaler = joblib.load('scaler.pkl')
kmeans = joblib.load('kmeans_model.pkl')
similarity_df = joblib.load('product_similarity.pkl')

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

    product = st.text_input("Enter Product Name")
    if st.button("Get Recommended Products"):
        if product in similarity_df.columns:
            recommendations = similarity_df[product].sort_values(ascending=False).iloc[1:6]
            st.subheader("Recommended products are:")
            for i, product in enumerate(recommendations.index.tolist(),1):
                st.write(f"{i}. {product}")
#            for product in recommendations.index.tolist():
#                st.success(product)
        else:
            st.error("Product not found")
