import streamlit as st
from helpers.restaurantFunctions import queryRestaurants, queryCuisines, display_restaurant_card, queryPlatos, createRestaurant
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.models import Restaurant

if "restaurants" not in st.session_state:
    st.session_state.restaurants = []
if "selected_restaurant_id" not in st.session_state:
    st.session_state.selected_restaurant_id = None
if "cuisines" not in st.session_state:
    st.session_state.cuisines = []
    







st.title("Restaurants")

st.write("This is the restaurants page.")

menu = ["Create Restaurant", "Find Restaurants", "Update Restaurant", "Delete Restaurant"]

choice = st.selectbox("Select an option", menu)

### Logica CRUD



# Create a restaurant
if choice == "Create Restaurant":
    with st.form(key='create_restaurant_form'):
        cuisines = queryCuisines()
        platos = queryPlatos()

        st.subheader("Create Restaurant")
        #restaurant id can only be an int
        resutaurant_id = st.number_input("Restaurant ID", min_value=1, step=1)
        restaurant_name = st.text_input("Restaurant Name")
        restaurant_longitude = st.number_input("Restaurant Longitude", format="%.6f")
        restaurant_latitude = st.number_input("Restaurant Latitude", format="%.6f")
        restaurant_address = st.text_input("Restaurant Address")
        create_cuisines = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
        create_platos = st.multiselect("Menu Items", [i['name'] for i in platos['data']])
    
        submit_button = st.form_submit_button(label='Create Restaurant')
        
        
        
        if submit_button:
            # Here you would typically call a function to create the restaurant in the database
            platosCreate = [i for i in platos['data'] if i['name'] in create_platos]
            #remove _id from platosCreate
            for i in platosCreate:
                del i['_id']
                if isinstance(i['addedToMenu'], datetime):
                    i['addedToMenu'] = i['addedToMenu'].strftime("%Y-%m-%d %H:%M:%S")
                
                else:
                    i['addedToMenu'] = str(i['addedToMenu'])
              
            print(platosCreate)
       
            url  = f'{st.session_state.host}/restaurants'
            
            data = Restaurant(
                id=int(resutaurant_id),
                name=restaurant_name,
                address=restaurant_address,
                cuisines=create_cuisines,
                location={
                    'type': 'Point',
                    'coordinates': [restaurant_longitude, restaurant_latitude]
                },
                menuItems=platosCreate,
                rating=0,
                numReviews=0)
            
            st.write(data)
            res = createRestaurant(data)
            #res = {'status': 200, 'message': 'Restaurant created successfully!'}
            if res['status'] == 200:
                st.session_state.restaurants.append(res)
                st.success(f"Restaurant '{restaurant_name}' created successfully!")
            else:
                st.error(f"Error creating restaurant: {res['message']}")
          


elif choice == "Find Restaurants":
    st.subheader("Find Restaurants")
    cuisines = queryCuisines()
    search_id = st.text_input("Search by Restaurant ID")
    search_name = st.text_input("Search by Restaurant Name")
    search_cuisine = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
    search_order = st.selectbox("Order by", ["rating", "name"])
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
    
    if st.button("Find Restaurants"):   
        
        data = None
        data = queryRestaurants(id=search_id, name=search_name, cuisines=search_cuisine, limit=limit, sort=search_order)
    
        if data is not None and data['status'] == 200:
            st.session_state.restaurants = data['data']
         
            if st.session_state.restaurants:
                numRestaurants = len(st.session_state.restaurants)
                
                cols = st.columns(3)
                for i, restaurant in enumerate(st.session_state.restaurants):
                    with cols[i % 3]:
                        display_restaurant_card(restaurant)
            else:
                st.write("No restaurants found.")
        else:
            st.error("Error fetching restaurants.")
        
      

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

