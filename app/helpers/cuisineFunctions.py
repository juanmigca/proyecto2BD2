import streamlit as st
import requests
from utils.models import Cuisines

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

def queryCuisines(id=None, name=None, limit=10, sort="name"):
    url = f"{st.session_state.host}/cuisines"
    params = {
        "id": id,
        "name": name,
        "limit": limit,
        "sort": sort
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching cuisines: {response.status_code}")
        return None

def createCuisine(cuisine: Cuisines):
    url = f"{st.session_state.host}/cuisines"
    data = cuisine.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating cuisine: {response.status_code}")
        return None

def updateCuisine(mode, id, cuisine: Cuisines):
    
    if mode == "Single":
        url = f"{st.session_state.host}/cuisines"
        params = {"id": id}
    else:
        url = f"{st.session_state.host}/batch/cuisines"
        params = {"ids": id}
    builtUrl = urlBuilder(url, params)
    response = requests.patch(builtUrl, json=cuisine.model_dump(exclude_unset=True))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error updating cuisine(s): {response.status_code}")
        return response.json()

def deleteCuisine(id, mode="Single"):
    params = {"id": id} if mode == "Single" else {"ids": id}
    url = f"{st.session_state.host}/cuisines" if mode == "Single" else f"{st.session_state.host}/batch/cuisines"
    builtUrl = urlBuilder(url, params)
    response = requests.delete(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error deleting cuisine(s): {response.status_code}")
        return None

def display_cuisine_card(cuisine):
    with st.container():
        st.markdown(f"### **Name:** {cuisine.get('name', 'N/A')}")
        st.markdown(f"**ID:** {cuisine.get('id', 'N/A')}")
        st.markdown(f"**Mongo _id:** {cuisine.get('_id', 'N/A')}")
