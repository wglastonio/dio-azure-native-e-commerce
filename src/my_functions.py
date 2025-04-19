# Function to upload product details to SQL Server
import os
import uuid
import pyodbc
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
blobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

# Load SQL Server connection details from environment variables
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")


def upload_product_to_blob_storage(product_image):
    if product_image is not None:
        # Generate a unique filename for the image
        image_filename = str(uuid.uuid4()) + "_" + product_image.name

        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)

        # Create a container client
        container_client = blob_service_client.get_container_client(blobContainerName)

        # Upload the image to Azure Blob Storage
        blob_client = container_client.get_blob_client(image_filename)
        blob_client.upload_blob(product_image.read(), overwrite=True)
        return image_filename
    else:
        return_message = "No image uploaded."


# Function to save product details to SQL Server
def save_product_to_sql_server(product_name, product_description, product_price, product_image):
    try:
        image_filename = upload_product_to_blob_storage(product_image)
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USERNAME};"
            f"PWD={SQL_PASSWORD}"
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Products (ProductName, ProductDescription, ProductPrice, ImageFilename)
            VALUES (?, ?, ?, ?)
            """,
            (product_name, product_description, product_price, image_filename),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
    

# Function to list products from SQL Server
def list_products_from_sql_server():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USERNAME};"
            f"PWD={SQL_PASSWORD}"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        conn.close()
        return products
    except Exception as e:
        return []
