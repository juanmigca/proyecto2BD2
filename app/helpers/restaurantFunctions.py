import streamlit as st
import requests

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
                
                
def queryPlatos(ids=None):
    """
    Queries the menu items from the API.
    """
    url  = f'{st.session_state.host}/menuItems'
    
    if ids is not None:
        url = urlBuilder(url, {"name": ids})
        
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching menu items: {response.status_code}")
        return None
    
    
def createRestaurant(name, longitude, latitude, address, cuisines, platos):
    """
    Creates a new restaurant in the database.
    """
    url  = f'{st.session_state.host}/restaurants'
    data = {
        "name": name,
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        },
        "address": address,
        "cuisines": cuisines,
        "menuItems": platos
    }
    
    response = requests.post(url, body=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating restaurant: {response.status_code}")
        return None