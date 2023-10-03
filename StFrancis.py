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
    st.image(logo, width=90) 

# Page title
with col2:
    st.title("St. Francis Youth")

# Define the path to the CSV file
csv_file_path = "Count.csv"

# Function to read and display the CSV data
def read_and_display_csv(data_frame):
    st.write("Members:")
    st.dataframe(data_frame)
    if "Amount" in data_frame.columns:
        total_contributions = data_frame["Amount"].sum()
        st.header("Figures😁")
        st.write(f"Tuko na: KES {total_contributions:.2f}")

# Load the initial "Count.csv" file if it exists
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    df = pd.DataFrame(columns=["Name", "Amount"])

# User input section to add or update data
st.header("Join sherehe na thao")

name = st.text_input("Name:")
amount = st.number_input("Contribution Amount:", value=1000)

if st.button("Weka ndani🎉"):
    if name and amount > 0:
        new_data = pd.DataFrame({"Name": [name], "Amount": [amount]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file_path, index=False)
        st.success("Data added or updated successfully!")
    else:
        st.error("Please enter a valid name and a contribution amount greater than 0.")

# User input section to delete data
st.header("Who's lefting")

# Display the current data for deletion
if not df.empty:
    selected_data = st.selectbox("Tunachuja nani?", df["Name"])
    if st.button("Baaeeh😭"):
        df = df[df["Name"] != selected_data]
        df.to_csv(csv_file_path, index=False)
        st.success(f"{selected_data} deleted successfully!")

# Display the CSV data and total contribution amount
read_and_display_csv(df)
