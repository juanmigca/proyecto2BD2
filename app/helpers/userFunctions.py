import streamlit as st
import requests

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

def queryUsers(id=None, username=None, orderMode=None, numOrders=None, reviewsMode=None, numReviews=None, visitedRestaurants=None, limit=10, sort="username"):
    url = f'{st.session_state.host}/users'
    params = {
        "id": id,
        "username": username,
        "orderMode": orderMode,
        "numOrders": numOrders,
        "reviewsMode": reviewsMode,
        "numReviews": numReviews,
        "visitedRestaurants": visitedRestaurants,
        "limit": limit,
        "sort": sort

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching users: {response.status_code}")
        return None

def createUser(user):
    url = f'{st.session_state.host}/users'
    data = user.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating user: {response.status_code}")
        return None

def updateUser(mode, id, update_data):
    params = {
        "find_id": id,
    }
    if mode == "Single":
        url = f'{st.session_state.host}/users'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()
        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error updating user: {response.status_code}")
            return response.json()
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/users'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()
        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error updating users: {response.status_code}")
            return response.json()

def deleteUser(id, mode="Single"):
    params = {
        "find_id": id
    }
    if mode == "Single":
        url = f'{st.session_state.host}/users'
        builtUrl = urlBuilder(url, params)
        response = requests.delete(builtUrl)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error deleting user: {response.status_code}")
            return None
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/users'
        builtUrl = urlBuilder(url, params)
        response = requests.delete(builtUrl)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error deleting users: {response.status_code}")
            return None

def display_user_card(user):
    with st.container():
        st.markdown(f"### {user['username']}")
        st.markdown(f"**User ID:** {user['id']}")
        st.markdown(f"**Number of Reviews:** {user.get('numReviews', 'N/A')}")
        
        st.markdown("**Visited Restaurants:**")
        visited = user.get("visitedRestaurants", [])
        
        if visited:
            url = f"{st.session_state.host}/restaurants"
            params = {
                "id": visited
            }
            response = requests.get(url, params=params)
            for restaurant in response.json()["data"]:
                st.markdown(f"- {restaurant["id"]}: {restaurant["name"]}")
        else:
            st.markdown("No restaurants visited.")


