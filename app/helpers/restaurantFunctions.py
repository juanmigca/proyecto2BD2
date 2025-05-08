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
        


def queryRestaurants(id=None, name=None, cuisines=None, limit=10, sort="rating"):
    params = {
        "id": id,
        "name": name,
        "cuisine": cuisines,
        "limit": limit,
        "sort": sort
    }


    url  = f'{st.session_state.host}/restaurants'
    builtUrl = urlBuilder(url, params)
    response = requests.get(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching restaurants: {response.status_code}")
        return None
    
def queryCuisines():

    url  = f'{st.session_state.host}/cuisines'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching cuisines: {response.status_code}")
        return None
    

def display_restaurant_card(restaurant):
    with st.container():
        st.markdown(f"### {restaurant['name']}")
        st.markdown(f"**ID:** {restaurant['id']}")
        st.markdown(f"**Cuisines:** {', '.join(restaurant['cuisines'])}")
        st.markdown(f"**Rating:** {round(float(restaurant['rating']),2)}/10")

        # Expander for additional details
        with st.expander("Details"):
            st.markdown(f"**Location:** Longitud: {restaurant['location']['coordinates'][0]}, Latitud: {restaurant['location']['coordinates'][1]}")
            st.markdown(f"**Address:** {restaurant['address']}")
            st.markdown(f"**Number of Reviews:** {restaurant['numReviews']}")
            
  
        with st.expander("Menu Items"):
            if restaurant['menuItems']:
                for item in restaurant['menuItems']:
                    st.markdown(f"- {item['name']} - ${item['price']}")
                    st.markdown(f"**Added to Menu:** {item['addedToMenu']}")
                    st.markdown(f"**Ingredients:** {', '.join([i['name'] + ' ' + str(i['amount']) + str(i['unitMeasure']) for i in item['ingredients']])}")
        
    
            else:
                st.write("No menu items available.")
                
                
def queryPlatos():
    """
    Queries the menu items from the API.
    """
    url  = f'{st.session_state.host}/menuItems'
   
        
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching menu items: {response.status_code}")
        return None
    
    
def createRestaurant(restaurant):
    """
    Creates a new restaurant in the database.
    """
    url  = f'{st.session_state.host}/restaurants'
    data = restaurant.model_dump()
    

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating restaurant: {response.status_code}")

        return response.json()
    
def updateRestaurant(mode, id, name, cuisine, update_data):
    """
    Updates one or multiple restaurants based on mode
    """

    params = {
        "find_id": id,
        "find_name": name,
        "find_cuisine": cuisine
    }
    if mode == "Single":
    
        url = f'{st.session_state.host}/restaurants'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()

        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error updating restaurant: {response.status_code}")

            return response.json()

    
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/restaurants'
        builtUrl = urlBuilder(url, params)
        data = update_data.model_dump()

        response = requests.patch(builtUrl, json=data)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error updating restaurants: {response.status_code}")

            return response.json()
    

def deleteRestaurant(mode, id, name, cuisine):
    params = {
        "find_id": id,
        "find_name": name,
        "find_cuisine": cuisine
    }
    if mode == "Single":
    
        url = f'{st.session_state.host}/restaurants'
        builtUrl = urlBuilder(url, params)
        

        response = requests.delete(builtUrl)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error deleting restaurant: {response.status_code}")

            return response.json()

    
    elif mode == "Multiple":
        url = f'{st.session_state.host}/batch/restaurants'
        builtUrl = urlBuilder(url, params)
       

        response = requests.delete(builtUrl)
        if response.status_code == 200:

            return response.json()
        else:
            st.error(f"Error deleting restaurants: {response.status_code}")

            return response.json()