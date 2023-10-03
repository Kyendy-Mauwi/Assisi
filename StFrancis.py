import streamlit as st
import pandas as pd
import os
from PIL import Image

# Set the page title and icon
st.set_page_config(page_title="St. Francis Youth AGM", page_icon="SFY.png")  # Replace "SFY.png" with the correct file path

# Create a layout with two columns for the logo and title
col1, col2 = st.columns(2)

# Logo
with col1:
    logo = Image.open("SFY.png")
    st.image(logo, width=100)  # Adjust the width as needed

# Page title
with col2:
    st.title("St. Francis Youth AGM")

# Define the admin password
admin_password = "Sfy2023"  # Replace with your desired password

# Create a text input for password
password = st.text_input("Enter the admin password:", type="password")

# Check if the password is correct
if password == admin_password:
    st.success("You are logged in as the admin.")
    admin_logged_in = True
else:
    admin_logged_in = False

# Define the path to the CSV file
csv_file_path = "Count.csv"

# Load the initial "Count.csv" file if it exists
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    df = pd.DataFrame(columns=["Name", "Amount"])

# Display the CSV data outside of the admin sections
st.header("CSV Data")
st.dataframe(df)

# If the admin is logged in, allow data management
if admin_logged_in:
    # User input section to add or update data
    st.header("Add or Update Data")

    name = st.text_input("Name:")
    amount = st.number_input("Contribution Amount:", value=0)

    if st.button("Add or Update"):
        if name and amount > 0:
            new_data = pd.DataFrame({"Name": [name], "Amount": [amount]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(csv_file_path, index=False)
            st.success("Data added or updated successfully!")
        else:
            st.error("Please enter a valid name and a contribution amount greater than 0.")

    # User input section to delete data
    st.header("Delete Data")

    # Display the current data for deletion
    if not df.empty:
        selected_data = st.selectbox("Select data to delete", df["Name"])
        if st.button("Delete Selected Data"):
            df = df[df["Name"] != selected_data]
            df.to_csv(csv_file_path, index=False)
            st.success(f"{selected_data} deleted successfully!")

# Display the CSV data and total contribution amount
st.header("Total Contribution Amount")
if "Amount" in df.columns:
    total_contributions = df["Amount"].sum()
    st.write(f"The total contribution amount is: ${total_contributions:.2f}")
