import streamlit as st
from helpers.restaurantFunctions import queryRestaurants, queryCuisines, display_restaurant_card, queryPlatos, createRestaurant, updateRestaurant, deleteRestaurant
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
        #st.write(cuisines)
        #st.write(platos)
        st.subheader("Create Restaurant")
        #restaurant id can only be an int
        #resutaurant_id = st.number_input("Restaurant ID", min_value=1, step=1)
        restaurant_name = st.text_input("Restaurant Name")
        restaurant_longitude = st.number_input("Restaurant Longitude", format="%.6f", max_value=180.0, min_value=-180.0)
        restaurant_latitude = st.number_input("Restaurant Latitude", format="%.6f", min_value=-90.0, max_value=90.0)
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
              
            #print(platosCreate)
       
            url  = f'{st.session_state.host}/restaurants'
            
            data = Restaurant(
                id=None,
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
            
            #st.write(data)
            res = createRestaurant(data)
            #res = {'status': 200, 'message': 'Restaurant created successfully!'}
            if res['status'] == 200:
                
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
    cuisines = queryCuisines()
    platos = queryPlatos()
    st.subheader("Update Restaurant")
    st.subheader("Find")
    update_search_id = st.text_input("Restaurant ID (Multiple e.g. 1,3,4)")
    update_search_name = st.text_input("Restaurant Name (Multiple e.g. McDonalds,Wendys or single e.g. McDonalds)")
    update_search_cuisine = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
    update_mode = st.selectbox("Update mode", ["Single", "Multiple"])


    st.subheader("Update")
    update_new_name = st.text_input("New Restaurant Name")
    update_new_address = st.text_input("New Restaurant Address")
    update_new_cuisines = st.multiselect("New Cuisines", [i['name'] for i in cuisines['data']])
    update_new_platos = st.multiselect("New Menu Items", [i['name'] for i in platos['data']])


    if st.button("Update Restaurant"):
        try: 
            if update_search_id != "":
                update_ids = update_search_id.split(",")
                update_ids = [int(i) for i in update_ids]
                if len(update_ids) == 1:
                    update_ids = update_ids[0]
            else:
                update_ids = update_search_id
            update_names = update_search_name.split(",")
            if len(update_names) == 1:
                update_names = update_names[0]

            if update_names == "":
                update_names = None
            
            if update_new_address == "":
                update_new_address = None
            
            #remove _id from platosCreate
            if update_new_platos != []:
                platos_update = [i for i in platos['data'] if i['name'] in update_new_platos]
                for i in platos_update:
                    del i['_id']
                    if isinstance(i['addedToMenu'], datetime):
                        i['addedToMenu'] = i['addedToMenu'].strftime("%Y-%m-%d %H:%M:%S")
                    
                    else:
                        i['addedToMenu'] = str(i['addedToMenu'])
            else: 
                platos_update = None

            if update_new_cuisines == []:
                update_new_cuisines = None

            update_restaurant = Restaurant(
                id=None,
                name=update_new_name,
                address=update_new_address,
                cuisines=update_new_cuisines,
                location = None,
                menuItems = platos_update,
                rating = None,
                numReviews= None
            )
            res = updateRestaurant(update_mode, update_ids, update_names, update_search_cuisine, update_restaurant)
            st.write(res)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating restaurant: {res['message']}")
        except:
            st.error(f"IDs can only be integers {update_new_platos}")

      

elif choice == "Delete Restaurant":
    st.subheader("Delete Restaurant")
    cuisines = queryCuisines()
    delete_search_id = st.text_input("Restaurant ID (Multiple e.g. 1,3,4 or single e.g. 1)")
    delete_search_name = st.text_input("Restaurant Name (Multiple e.g. McDonalds,Wendys or single e.g. McDonalds)")
    delete_search_cuisines = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
    delete_mode = st.selectbox("Update mode", ["Single", "Multiple"])

    
    if st.button("Delete Restaurant"):
        
        try: 
            if delete_search_id != "":
                delete_ids = delete_search_id.split(",")
                delete_ids = [int(i) for i in delete_ids]
                if len(delete_ids) == 1:
                    delete_ids = delete_ids[0]
            else:
                delete_ids = delete_search_id
            delete_names = delete_search_name.split(",")
            if len(delete_names) == 1:
                delete_names = delete_names[0]
            
            res = deleteRestaurant(delete_mode, delete_ids, delete_search_name, delete_search_cuisines)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating restaurant: {res['message']}")
        except:
            st.error(f"IDs can only be integers {delete_search_id}")

        
