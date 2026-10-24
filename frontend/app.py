
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend (container name resolved by the Docker network)
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecast")
st.write("Enter the product and store details below to predict the total sales.")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027, format="%.3f")
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox(
    "Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"]
)
Product_Id_char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

# Single prediction
if st.button("Predict", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data, timeout=30)
        if response.status_code == 200:
            st.success(f"Predicted Product Store Sales Total: {response.json()['Sales']:.2f}")
        else:
            st.error(f"Prediction failed: {response.text}")
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the prediction API.")

# Batch prediction
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None and st.button("Predict for Batch", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")},
            timeout=60,
        )
        if response.status_code == 200:
            results = pd.DataFrame(
                list(response.json().items()), columns=["Row", "Predicted_Sales"]
            )
            st.success("Predictions completed successfully!")
            st.dataframe(results, use_container_width=True)
        else:
            st.error(f"Batch prediction failed: {response.text}")
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the prediction API.")
