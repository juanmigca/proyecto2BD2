import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.userFunctions import queryUsers, createUser, updateUser, deleteUser, display_user_card
from utils.models import User

st.title("Users")

menu = ["Create User", "Find Users", "Update Users", "Delete Users"]
choice = st.selectbox("Select an option", menu)

# Create User
if choice == "Create User":
    with st.form(key='create_user_form'):
        st.subheader("Create User")
        #user_id = st.number_input("User ID", min_value=1, step=1)
        username = st.text_input("Username")

        submit_button = st.form_submit_button(label='Create User')
        if submit_button:
            

            data = User(
                id=None,
                username=username
            )

            res = createUser(data)
            if res and res['status'] == 200:
                st.success(f"User '{username}' created successfully!")
            else:
                st.error(f"Error creating user: {res['message']}")

# Find Users
elif choice == "Find Users":
    st.subheader("Find Users")
    search_id = st.text_input("Search by User ID")
    search_username = st.text_input("Search by Username")
    search_num_reviews = st.text_input("Search by Number of Reviews (e.g >4 or <4)")
    search_num_orders = st.text_input("Search by Number of Orders (e.g >4 or <4)")
    search_visited = st.text_input("Search by Visited Restaurants (comma-separated ids)")
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
    sort = st.selectbox("Sort by", ["username", "numReviews", "numOrders"])

    if st.button("Find Users"):
        try:

            ids = [int(i) for i in search_id.split(",")] if "," in search_id else int(search_id) if search_id else None
            usernames = search_username.split(",") if "," in search_username else search_username or None
            
         
            if search_num_reviews.startswith(">"):
                num_reviews = int(search_num_reviews[1:])
                reviews_search_mode = "greater"
            elif search_num_reviews.startswith("<"):
                reviews_search_mode = "lesser"
                num_reviews = int(search_num_reviews[1:])
            else:
                reviews_search_mode = "equal" if search_num_reviews else None
                num_reviews = int(search_num_reviews) if search_num_reviews else None
        
            if search_num_orders.startswith(">"):
                orders_search_mode = "greater"
                num_orders = int(search_num_orders[1:])
                
            elif search_num_orders.startswith("<"):
                orders_search_mode = "lesser"
                num_orders = int(search_num_orders[1:])
            else:
                orders_search_mode = "equal" if search_num_orders else None
                num_orders = int(search_num_orders) if search_num_orders else None

            visited = [int(i) for i in search_visited.split(",")] if "," in search_visited else search_visited or None
            data = queryUsers(ids, usernames, orders_search_mode, num_orders, reviews_search_mode, num_reviews, visited, limit, sort)

            if data and data['status'] == 200:
                st.session_state.users = data['data']
                if st.session_state.users:
                    cols = st.columns(2)
                    for i, user in enumerate(st.session_state.users):
                        with cols[i % 2]:
                            display_user_card(user)
                else:
                    st.write(data)
                    st.info("No users found.")
            else:
                st.write(data)
                st.error("Error fetching users.")
        except:
            st.error("IDs must be integers")

# Update Users
elif choice == "Update Users":
    st.subheader("Update User")
    st.subheader("Find")
    update_search_id = st.text_input("User ID (Multiple e.g. 1,3,4)")
    update_mode = st.selectbox("Update mode", ["Single", "Multiple"])

    st.subheader("Update")
    update_username = st.text_input("New Username")

    if st.button("Update User"):
        try:
            update_ids = [int(i) for i in update_search_id.split(",")] if "," in update_search_id else int(update_search_id)
           

            user_update = User(
                id=None,
                username=update_username or None,
                numReviews=None,
                visitedRestaurants= None,
                numOrders=None
            )

            res = updateUser(update_mode, update_ids, user_update)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating user: {res['message']}")
        except:
            st.error("IDs must be integers")

# Delete Users
elif choice == "Delete Users":
    st.subheader("Delete Users")
    delete_search_id = st.text_input("User ID (Multiple or single)")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete User"):
        try:
            delete_ids = [int(i) for i in delete_search_id.split(",")] if "," in delete_search_id else int(delete_search_id)
            res = deleteUser(delete_ids, delete_mode)
            if res and res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error deleting user: {res['message']}")
        except:
            st.error("IDs must be integers")
