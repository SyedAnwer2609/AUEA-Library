import requests
import streamlit as st
import pandas as pd

# Azure AD App credentials
TENANT_ID = 'cd236fe6-adf6-481b-becd-f37fd7186558'
CLIENT_ID = '7937bad2-44a4-4f3c-9574-52c303300c74'
CLIENT_SECRET = 'your-client-secret'

# Get access token
def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': zJK8Q~k_XLP5gj5IpRm3Y54sucVi844sy5O3za8z,
        'client_secret': 35094de8-bce3-40f7-8e54-bba43b136cb0,
        'scope': 'https://graph.microsoft.com/.default'
    }
    r = requests.post(url, data=data)
    return r.json().get('access_token')

# Search users by name
def search_users(first_name, last_name, token):
    url = f"https://graph.microsoft.com/v1.0/users?$filter=startswith(givenName,'{first_name}') and startswith(surname,'{last_name}')"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    return r.json().get('value', [])

# Streamlit UI
st.title("Azure Entra ID Book Assignment")

isbn = st.text_input("Enter ISBN")
first_name = st.text_input("User First Name")
last_name = st.text_input("User Last Name")

if st.button("Search User"):
    token = get_access_token()
    users = search_users(first_name, last_name, token)
    if users:
        for user in users:
            st.write(f"{user['displayName']} - {user.get('mail', 'No email')}")
    else:
        st.write("No users found.")
