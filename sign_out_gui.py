import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Load the Excel file
file_path = 'Copy of library books log 10TH MARCH 2.xlsx'
df = pd.read_excel(file_path)

# Streamlit app title
st.title('Library Book Sign-Out System')

# Input for ISBN
isbn_input = st.text_input('Enter ISBN to sign out a book:')

if isbn_input:
    # Check if ISBN exists in the dataframe
    if isbn_input in df['ISBN NUMBER'].values:
        # Get the current date
        borrow_date = datetime.now().date()
        return_date = borrow_date + timedelta(days=14)

        # Update the dataframe
        df.loc[df['ISBN NUMBER'] == isbn_input, 'Date Borrowed'] = borrow_date
        df.loc[df['ISBN NUMBER'] == isbn_input, 'Return By'] = return_date

        # Save the updated dataframe back to the Excel file
        df.to_excel(file_path, index=False)

        # Display confirmation message
        st.success(f'Book with ISBN {isbn_input} signed out successfully!')
        st.write(f'Date Borrowed: {borrow_date}')
        st.write(f'Return By: {return_date}')
    else:
        st.error('ISBN not found in the library records.')
