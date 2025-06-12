import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title('Library Book Sign-Out System')

# Upload Excel file
uploaded_file = st.file_uploader("Upload the library log Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Input for ISBN
    isbn_input = st.text_input('Enter ISBN to sign out a book:')

    if isbn_input:
        if isbn_input in df['ISBN NUMBER'].values:
            borrow_date = datetime.now().date()
            return_date = borrow_date + timedelta(days=14)

            df.loc[df['ISBN NUMBER'] == isbn_input, 'Date Borrowed'] = borrow_date
            df.loc[df['ISBN NUMBER'] == isbn_input, 'Return By'] = return_date

            # Display confirmation
            st.success(f'Book with ISBN {isbn_input} signed out successfully!')
            st.write(f'Date Borrowed: {borrow_date}')
            st.write(f'Return By: {return_date}')

            # Provide download button for updated file
            st.download_button(
                label="Download updated log",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="LibraryBooks.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error('ISBN not found in the library records.')
