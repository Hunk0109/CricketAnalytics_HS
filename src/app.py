import pyodbc
import streamlit as st
import pandas as pd

# Establish a connection to Azure Data Studio database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=sportsanalytics;'
    'UID=SA;'
    'PWD=Hunk@123;'
)

cursor = conn.cursor()
st.write("Connection Established")

# Load the Venue data
def load_data():
    try:
        query = "SELECT * FROM Venue"
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error("Error loading data: {}".format(e))
        return None

# Create Streamlit App
def main():
    st.title("Cricket Analytics Database System")
    
    venue_df = load_data()  # Load Venue data here

    if venue_df is not None:
        st.sidebar.success("Data loaded successfully!")
    else:
        st.sidebar.error("Failed to load data!")

    # Display Options for CRUD Operations
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

    # Perform Selected CRUD Operations
    if option == "Create":
        create_record()

    elif option == "Read":
        read_records(venue_df)

    elif option == "Update":
        update_record(venue_df)

    elif option == "Delete":
        delete_record(venue_df)

# Function to create a new record
def create_record():
    st.subheader("Create New Venue Record")
    venue_id = st.number_input("VenueID", min_value=1, step=1)
    name = st.text_input("Name")
    capacity = st.number_input("Capacity", min_value=1, step=1)
    city = st.text_input("City")
    state = st.text_input("State")
    country = st.text_input("Country")

    if st.button("Create Record"):
        try:
            cursor.execute("INSERT INTO Venue (VenueID, [Name], Capacity, City, [State], Country) VALUES (?, ?, ?, ?, ?, ?)",
                           (venue_id, name, capacity, city, state, country))
            conn.commit()
            st.success("Record created successfully!")
        except Exception as e:
            st.error(f"Error creating record: {e}")

# Function to read existing records
def read_records(venue_df):
    st.subheader("Existing Venue Records")
    st.write(venue_df)

# Function to update an existing record
def update_record(venue_df):
    st.subheader("Update Venue Record")
    selected_id = st.number_input("Enter VenueID to Update", min_value=1, step=1)
    record_to_update = venue_df[venue_df['VenueID'] == selected_id]
    if not record_to_update.empty:
        new_name = st.text_input("Name", value=record_to_update.iloc[0]['Name'])
        new_capacity = st.number_input("Capacity", value=record_to_update.iloc[0]['Capacity'], min_value=1, step=1)
        new_city = st.text_input("City", value=record_to_update.iloc[0]['City'])
        new_state = st.text_input("State", value=record_to_update.iloc[0]['State'])
        new_country = st.text_input("Country", value=record_to_update.iloc[0]['Country'])

        if st.button("Update Record"):
            try:
                cursor.execute("UPDATE Venue SET [Name] = ?, Capacity = ?, City = ?, [State] = ?, Country = ? WHERE VenueID = ?",
                               (new_name, new_capacity, new_city, new_state, new_country, selected_id))
                conn.commit()
                st.success("Record updated successfully!")
            except Exception as e:
                st.error(f"Error updating record: {e}")
    else:
        st.warning("No record found with the provided VenueID.")

# Function to delete an existing record
def delete_record(venue_df):
    st.subheader("Delete Venue Record")
    selected_id = st.number_input("Enter VenueID to Delete", min_value=1, step=1)
    record_to_delete = venue_df[venue_df['VenueID'] == selected_id]
    if not record_to_delete.empty:
        if st.button("Delete Record"):
            try:
                cursor.execute("DELETE FROM Venue WHERE VenueID = ?", (selected_id,))
                conn.commit()
                st.success("Record deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting record: {e}")
    else:
        st.warning("No record found with the provided VenueID.")

if __name__ == "__main__":
    main()
