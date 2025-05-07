import streamlit as st
import requests
import json

def urlBuilder(url, params=None):
    """
    Constructs a full URL by combining a base URL with an endpoint and optional query parameters.

    Args:
        url (str): The endpoint to append to the base URL.
        params (dict, optional): A dictionary of query parameters to include in the URL.

    Returns:
        str: The constructed full URL.
    """
    url = url + '?'
    
    for k,v in params.items():
        if v is not None and v != '':
            if isinstance(v, list):
                for i in v:
                    url += f'{k}={i}&'
            else:
                url += f'{k}={v}&'
    
    return url[:-1]

        

def queryMenuItems(id=None, name=None, limit=10, sort="addedToMenu"):
    """
    Queries the menu items based on the given parameters.
    """
    url = f'{st.session_state.host}/menuItems'
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
        st.error(f"Error fetching menu items: {response.status_code}")
        return None
    

def createMenuItem(menu_item):
    """
    Creates a new menu item in the database.
    """
    url = f'{st.session_state.host}/menuItems'
    data = menu_item.model_dump()
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating menu item: {response.status_code}")
        return None
    
def updateMenuItem(mode, id, update_data):
    """
    Updates one or multiple menu items based on mode
    """
    
    params = {
        "find_id": id,
    }
    if mode == "Single":
        
        url = f'{st.session_state.host}/menuItems'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()

        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error updating menu item: {response.status_code}")

            return response.json()
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/menuItems'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()

        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error updating menu item: {response.status_code}")

            return response.json()
        
def deleteMenuItem(id, mode="Single"):
    """
    Deletes a menu item from the database.
    """
    
    if mode == "Single":
        url = f'{st.session_state.host}/menuItems'
        params = {
            "find_id": id
        }
        builtUrl = urlBuilder(url, params)
        response = requests.delete(builtUrl)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error deleting menu item: {response.status_code}")
            return None
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/menuItems'
        params = {
            "find_id": id
        }
        builtUrl = urlBuilder(url, params)
        response = requests.delete(builtUrl)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error deleting menu item: {response.status_code}")
            return None
        

def queryIngredients():
    """
    Queries the ingredients from the database.
    """
    url = f'{st.session_state.host}/ingredients'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching ingredients: {response.status_code}")
        return None
    

def display_menu_item_card(menu_item):
    with st.container():
        st.markdown(f"### {menu_item['name']}")
        st.markdown(f"**Price:** ${menu_item['price']:.2f}")
        st.markdown(f"**Added to Menu:** {menu_item['addedToMenu']}")
        st.markdown("**Ingredients:**")
        if menu_item['ingredients']:
            for ing in menu_item['ingredients']:
                st.markdown(f"- {ing['name']} ({ing['amount']}{ing['unitMeasure']})")
        else:
            st.markdown("No ingredients listed.")