import streamlit as st
from dotenv import load_dotenv
import my_functions as my_functions

load_dotenv()

# Form of Product Details
st.title("Azure Blob Storage and SQL Server Integration")


# Form to upload product details
product_name = st.text_input("Enter the product name:")
product_description = st.text_area("Enter the product description:")
product_price = st.number_input("Enter the product price:", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Upload product image:", type=["jpg", "jpeg", "png"])


# Function to upload image to Azure Blob Storage
if st.button("Save Product"):
    save_result = my_functions.save_product_to_sql_server(product_name, product_description, product_price, product_image)
    if save_result:
        st.success("Product details saved successfully!")
    else:
        st.error("Error saving product details.")
    return_message = "Product saved successfully!"


# Function to list products from SQL Server
st.header("Products List")
if st.button("List Products"):
    products = my_functions.list_products_from_sql_server()
    if products:
        for product in products:
            st.write(f"Product Name: {product.ProductName}")
            st.write(f"Product Description: {product.ProductDescription}")
            st.write(f"Product Price: {product.ProductPrice}")
            st.image(f"https://{my_functions.blobAccountName}.blob.core.windows.net/{my_functions.blobContainerName}/{product.ImageFilename}", caption=product.ProductName)
    else:
        st.write("No products found.")
    
    # Display success message
    return_message = "Products listed successfully!"


