import streamlit as st
import requests
from utils.models import Review

def urlBuilder(url, params=None):
    url = url + '?'
    for k, v in params.items():
        if v is not None and v != '':
            if isinstance(v, list):
                for i in v:
                    url += f'{k}={i}&'
            else:
                url += f'{k}={v}&'
    return url[:-1]

def queryReviews(id=None, user_id=None, restaurant_id=None, rating=None, limit=10):
    url = f"{st.session_state.host}/reviews"
    params = {
        "id": id,
        "user_id": user_id,
        "restaurant_id": restaurant_id,
        "rating": rating,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching reviews: {response.status_code}")
        return None

def createReview(review: Review):
    url = f"{st.session_state.host}/reviews"
    data = review.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating review: {response.status_code}")
        return None

def updateReview(mode, id, update_data: Review):
    params = {
        "find_id": id
    }
    if mode == "Single":
        url = f"{st.session_state.host}/reviews"
    else:
        url = f"{st.session_state.host}/batch/reviews"
    builtUrl = urlBuilder(url, params)
    response = requests.patch(builtUrl, json=update_data.model_dump(exclude_unset=True))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error updating review(s): {response.status_code}")
        return response.json()

def deleteReview(id, mode="Single"):
    params = {
        "find_id": id
    }
    if mode == "Single":
        url = f"{st.session_state.host}/reviews"
    else:
        url = f"{st.session_state.host}/batch/reviews"
    builtUrl = urlBuilder(url, params)
    response = requests.delete(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error deleting review(s): {response.status_code}")
        return None

def display_review_card(review):
    with st.container():
        st.markdown(f"### Review ID: {review['id']}")
        st.markdown(f"**User ID:** {review.get('userId', 'N/A')}")
        st.markdown(f"**Restaurant ID:** {review.get('restaurantId', 'N/A')}")
        st.markdown(f"**Order ID:** {review.get('orderId', 'N/A')}")
        st.markdown(f"**Stars:** {'⭐' * int(review.get('stars', 0))}")
        st.markdown(f"**Comment:** {review.get('comment', 'No comment')}")
        st.markdown(f"**Timestamp:** {review.get('timestamp', 'N/A')}")