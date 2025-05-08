import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.reviewFunctions import queryReviews, createReview, updateReview, deleteReview
from helpers.userFunctions import queryUsers
from helpers.restaurantFunctions import queryRestaurants
from helpers.orderFunctions import queryOrders
from utils.models import Review

if "review_data" not in st.session_state:
    st.session_state.review_data = Review()

st.title("Reviews")

menu = ["Create Review", "Find Reviews", "Update Reviews", "Delete Reviews"]
choice = st.selectbox("Select an option", menu)

# Create Review
if choice == "Create Review":
    with st.form(key='create_review_form'):
        st.subheader("Create Review")

     

        #review_id = st.number_input("Review ID", min_value=1, step=1)
        user_id = st.text_input("User ID")
        restaurant_id = st.text_input("Restaurant ID")
        order_id = st.text_input("Order ID (Optional)")
        stars = st.slider("Stars", min_value=1, max_value=10, step=1)
        comment = st.text_area("Comment")

        submit_button = st.form_submit_button(label='Submit Review')

        if submit_button:
            try:
                if not user_id or not restaurant_id:
                    st.error("User ID and Restaurant ID are required")

                user_id = int(user_id)
                restaurant_id = int(restaurant_id)
                order_id = int(order_id) if order_id else None
                user_doc = queryUsers(user_id=user_id, limit=1)[0]
                if not user_doc:
                    st.error("User not found")
                else:
                    st.session_state.review_data.userId = user_id
                restaurant_doc = queryRestaurants(restaurant_id=restaurant_id, limit=1)[0]
                if not restaurant_doc:
                    st.error("Restaurant not found")
                if order_id is not None:
                    order_doc = queryOrders(id=order_id, limit=1)[0]
                    if order_doc.get('userId') != user_id or order_doc.get('restaurantId') != restaurant_id:
                        st.error("Order does not belong to the user or restaurant")
                if not user_doc or not restaurant_doc:
                    st.error("User or Restaurant not found")
                else:
                    st.session_state.review_data = Review(
                        id=None,
                        userId=int(user_id),
                        restaurantId=int(restaurant_id),
                        orderId=int(order_id),
                        stars=stars,
                        comment=comment
                    )
                
    
                    res = createReview(st.session_state.review_data)
                    if res and res['status'] == 200:
                        st.success("Review created successfully!")
                    else:
                        st.error("Error creating review")
            except:
                st.error("IDs must be integers")
# Find Reviews
elif choice == "Find Reviews":
    st.subheader("Find Reviews")
    search_id = st.text_input("Search by Review ID")
    search_user_id = st.text_input("Search by User ID")
    search_restaurant_id = st.text_input("Search by Restaurant ID")
    search_rating = st.selectbox("Search by Rating", ["", 1, 2, 3, 4, 5])
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("Find Reviews"):
        try:
            ids = [int(i) for i in search_id.split(",")] if "," in search_id else int(search_id) if search_id else None
            user_ids = [int(i) for i in search_user_id.split(",")] if "," in search_user_id else int(search_user_id) if search_user_id else None
            rest_ids = [int(i) for i in search_restaurant_id.split(",")] if "," in search_restaurant_id else int(search_restaurant_id) if search_restaurant_id else None
            rating = int(search_rating) if search_rating else None

            data = queryReviews(ids, user_ids, rest_ids, rating, limit)
            if data and data['status'] == 200:
                st.session_state.reviews = data['data']
                if st.session_state.reviews:
                    for r in st.session_state.reviews:
                        st.write(f"ID: {r['id']}, User: {r['userId']}, Restaurant: {r['restaurantId']}, Stars: {r['stars']}, Comment: {r['comment']}")
                else:
                    st.info("No reviews found.")
            else:
                st.error("Error fetching reviews")
        except:
            st.error("IDs must be integers")

# Update Reviews
elif choice == "Update Reviews":
    st.subheader("Update Review")
    review_id = st.number_input("Review ID to Update", min_value=1, step=1)

    new_stars = st.slider("New Stars", min_value=1, max_value=5, step=1)
    new_comment = st.text_area("New Comment")

    if st.button("Update Review"):
        try:
            review = Review(id=None, stars=new_stars, comment=new_comment)
            res = updateReview("single", review_id, review)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating review: {res['message']}")
        except:
            st.error("IDs must be integers")

# Delete Reviews
elif choice == "Delete Reviews":
    st.subheader("Delete Reviews")
    delete_id = st.text_input("Review ID (Multiple or single)")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete Review"):
        try:
            delete_ids = [int(i) for i in delete_id.split(",")] if "," in delete_id else int(delete_id)
            res = deleteReview(delete_ids, delete_mode)
            if res and res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error deleting review: {res['message']}")
        except:
            st.error("IDs must be integers")
