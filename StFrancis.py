import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64

# Set the page title and icon
st.set_page_config(page_title="St. Francis Youth AGM", page_icon="SFY.png")  # Replace "SFY.png" with the correct file path

# Create a layout with two columns for the logo and title
col1, col2 = st.columns(2)

# Logo
with col1:
    logo = Image.open("SFY.png")
    st.image(logo, width=100)  # Adjust the width as needed

# Page title
# with col2:
#     st.title("St. Francis Youth AGM")

# Define the admin password
admin_password = "Sfy2023"  # Replace with your desired password

# Create a checkbox for admin access
is_admin = st.checkbox("Log In as Admin")

if is_admin:
    # If the user wants admin access, ask for the admin password
    password_input = st.text_input("Enter the admin password:", type="password")

    if password_input != admin_password:
        st.warning("Please enter the correct password to access admin privileges.")
        is_admin = False

# Define the path to the CSV file
csv_file_path = "Count.csv"

# Load the initial "Count.csv" file if it exists
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    df = pd.DataFrame(columns=["Name", "Amount"])

# Check if the user is logged in as admin
if is_admin:
    # Admin has access to data management
    # User input section to add or update data
    st.header("Add Member")

    name = st.text_input("Name:")
    amount = st.number_input("Contribution Amount:", value=0)

    if st.button("Add"):
        if name and amount > 0:
            new_data = pd.DataFrame({"Name": [name], "Amount": [amount]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(csv_file_path, index=False)
            st.success("Data added or updated successfully!")
        else:
            st.error("Please enter a valid name and a contribution amount greater than 0.")

    # User input section to delete data
    st.header("Delete Member")

    # Display the current data for deletion
    if not df.empty:
        selected_data = st.selectbox("Select data to delete", df["Name"])
        if st.button("Delete Selected Member"):
            df = df[df["Name"] != selected_data]
            df.to_csv(csv_file_path, index=False)
            st.success(f"{selected_data} deleted successfully!")

# Display the CSV data outside of the admin sections
st.header("Member Contributions")
st.dataframe(df)

# Display the CSV data and total contribution amount
st.header("Total Contribution Amount")
if "Amount" in df.columns:
    total_contributions = df["Amount"].sum()
    st.write(f"The total contribution amount is: KES{total_contributions:.2f}")

# Allow all users to download the CSV file
st.write('For copy click below⬇️')
csv_file = df.to_csv(index=False).encode()
b64 = base64.b64encode(csv_file).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64}" download="Count.csv">Download Members List</a>', unsafe_allow_html=True)

st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
# Centered and sticky footer using CSS
footer = """
<style>
.footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>
<div class="footer">
    <p>Copyright SFY 2023</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
