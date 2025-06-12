import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from streamlit_msal import Msal

# Azure Entra ID config
client_id = "7937bad2-44a4-4f3c-9574-52c303300c74"
authority = "https://login.microsoftonline.com/cd236fe6-adf6-481b-becd-f37fd7186558"
scopes = ["User.Read"]

# Authenticate user
with st.sidebar:
    auth_data = Msal.initialize_ui(
        client_id=client_id,
        authority=authority,
        scopes=scopes
    )

if not auth_data:
    st.warning("Please sign in to access the system.")
    st.stop()

user_name = auth_data["account"]["name"]
user_email = auth_data["account"]["username"]

st.title(f"Welcome, {user_name}!")

# Upload Excel file
uploaded_file = st.file_uploader("Upload the library log Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    isbn_input = st.text_input('Enter ISBN to sign out a book:')

    if isbn_input:
        if isbn_input in df['ISBN NUMBER'].values:
            borrow_date = datetime.now().date()
            return_date = borrow_date + timedelta(days=14)

            df.loc[df['ISBN NUMBER'] == isbn_input, 'Date Borrowed'] = borrow_date
            df.loc[df['ISBN NUMBER'] == isbn_input, 'Return By'] = return_date
            df.loc[df['ISBN NUMBER'] == isbn_input, 'Borrowed By'] = user_name
            df.loc[df['ISBN NUMBER'] == isbn_input, 'Borrower Email'] = user_email

            st.success(f'Book with ISBN {isbn_input} signed out successfully!')
            st.write(f'Date Borrowed: {borrow_date}')
            st.write(f'Return By: {return_date}')

            # Convert DataFrame to Excel in memory
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="Download updated log",
                data=output,
                file_name="LibraryBooks.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error('ISBN not found in the library records.')
