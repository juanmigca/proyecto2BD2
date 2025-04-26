import streamlit as st
import requests

def urlBuilder(url, params=None):
    """
    Constructs a full URL by combining a base URL with an endpoint and optional query parameters.

    Args:
        base_url (str): The base URL.
        endpoint (str): The endpoint to append to the base URL.
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
        


def queryRestaurants(id=None, name=None, cuisines=None):
    params = {
        "id": id,
        "name": name,
        "cuisine": cuisines
    }


    url  = f'{st.session_state.host}/restaurants'
    builtUrl = urlBuilder(url, params)
    response = requests.get(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching restaurants: {response.status_code}")
        return None
    



st.title("Restaurants")

st.write("This is the restaurants page.")

menu = ["Create Restaurant", "Find Restaurants", "Update Restaurant", "Delete Restaurant"]

choice = st.selectbox("Select an option", menu)

### Logica CRUD



# Create a restaurant
if choice == "Create Restaurant":
    st.subheader("Create Restaurant")
    restaurant_name = st.text_input("Restaurant Name")
    restaurant_location = st.text_input("Restaurant Location")
    restaurant_cuisine = st.text_input("Cuisine Type")
    restaurant_rating = st.number_input("Rating", min_value=1, max_value=5, value=3)
    
    if st.button("Create Restaurant"):
        # Here you would typically call a function to create the restaurant in the database
        st.success(f"Restaurant '{restaurant_name}' created successfully!")


elif choice == "Find Restaurants":
    st.subheader("Find Restaurants")
    search_id = st.text_input("Search by Restaurant ID")
    search_name = st.text_input("Search by Restaurant Name")
    search_cuisine = st.text_input("Search by Cuisine Type")
    
    if st.button("Find Restaurants"):
        print(search_id, search_name, search_cuisine)
        data = None
        data = queryRestaurants(id=search_id, name=search_name, cuisines=search_cuisine)
        print(data)
        if data is not None and data['status'] == 200:
            restaurants = data['data']
            if restaurants:
                st.write(restaurants)
            else:
                st.write("No restaurants found.")
        else:
            st.error("Error fetching restaurants.")
        # Here you would typically call a function to find restaurants in the database
        st.success(f"Found restaurants matching '{search_name}' and '{search_cuisine}'!")

elif choice == "Update Restaurant":
    st.subheader("Update Restaurant")
    restaurant_id = st.text_input("Restaurant ID")
    new_name = st.text_input("New Restaurant Name")
    new_location = st.text_input("New Restaurant Location")
    new_cuisine = st.text_input("New Cuisine Type")
    new_rating = st.number_input("New Rating", min_value=1, max_value=5, value=3)
    
    if st.button("Update Restaurant"):
        # Here you would typically call a function to update the restaurant in the database
        st.success(f"Restaurant '{restaurant_id}' updated successfully!")

elif choice == "Delete Restaurant":
    st.subheader("Delete Restaurant")
    restaurant_id = st.text_input("Restaurant ID")
    
    if st.button("Delete Restaurant"):
        # Here you would typically call a function to delete the restaurant from the database
        st.success(f"Restaurant '{restaurant_id}' deleted successfully!")

