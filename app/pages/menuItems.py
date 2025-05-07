import streamlit as st
#from helpers.menuItemsFunctions import 
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from helpers.menuItemsFunctions import queryMenuItems, createMenuItem, updateMenuItem, deleteMenuItem, queryIngredients, display_menu_item_card
from utils.models import MenuItem

st.title("Menu Items")


menu = ["Create Menu Item", "Find Menu Items", "Update Menu Items", "Delete Menu Items"]

choice = st.selectbox("Select an option", menu)

### Logica CRUD





# Create a MenuItem
if choice == "Create Menu Item":
    with st.form(key='create_MenuItem_form'):
        ingredients = queryIngredients()
        #st.write(ingredients)

        st.subheader("Create MenuItem")
        #MenuItem id can only be an int
        menuItem_id = st.number_input("MenuItem ID", min_value=1, step=1)
        MenuItem_name = st.text_input("MenuItem Name")
        MenuItem_price = st.number_input("Price", format="%.2f")
        create_ingredients = st.multiselect("Ingredients", [i['name'] for i in ingredients['data']])

    
        submit_button = st.form_submit_button(label='Create MenuItem')
        
        
        
        if submit_button:
            # Here you would typically call a function to create the MenuItem in the database
            ingredientsCreate = [i for i in ingredients['data'] if i['name'] in create_ingredients]
            #remove _id from platosCreate
            for i in ingredientsCreate:
                del i['_id']
    
        
       
           
            
            data = MenuItem(
                id=int(menuItem_id),
                name=MenuItem_name,
                price=MenuItem_price,
                ingredients=ingredientsCreate,
                )
            
            st.write(data)
            res = createMenuItem(data)  
            #res = {'status': 200, 'message': 'MenuItem created successfully!'}
            if res['status'] == 200:
                
                st.success(f"MenuItem '{MenuItem_name}' created successfully!")
            else:
                st.error(f"Error creating MenuItem: {res['message']}")  
elif choice == "Find Menu Items":
    st.subheader("Find Menu Items")
    search_id = st.text_input("Search by Menu Item ID")
    search_name = st.text_input("Search by Menu Item Name")
    search_order = st.selectbox("Order by", ["addedToMenu", "name"])
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("Find Menu Items"):
        try:
            if search_id:
                search_ids = [int(i) for i in search_id.split(",")] if "," in search_id else int(search_id)
            else:
                search_ids = None

            search_names = search_name.split(",") if "," in search_name else search_name

            data = queryMenuItems(id=search_ids, name=search_names, sort=search_order, limit=limit)

            if data and data['status'] == 200:
                st.session_state.menu_items = data['data']
                if st.session_state.menu_items:
                    cols = st.columns(3)
                    for i, item in enumerate(st.session_state.menu_items):
                        with cols[i % 3]:
                            display_menu_item_card(item)
                else:
                    st.info("No menu items found.")
            else:
                st.error("Error fetching menu items.")
        except:
            st.error("IDs must be integers")


elif choice == "Update Menu Items":
    st.subheader("Update Menu Item")
    st.subheader("Find")
    update_search_id = st.text_input("Menu Item ID (Multiple e.g. 1,3,4)")
    update_mode = st.selectbox("Update mode", ["Single", "Multiple"])

    st.subheader("Update")
    update_new_name = st.text_input("New Menu Item Name")
    update_new_price = st.number_input("New Price", format="%.2f")
    ingredients = queryIngredients()
    update_new_ingredients = st.multiselect("New Ingredients", [i['name'] for i in ingredients['data']])

    if st.button("Update Menu Item"):
        try:
            if update_search_id:
                update_ids = [int(i) for i in update_search_id.split(",")] if "," in update_search_id else int(update_search_id)
            else:
                update_ids = None


            new_ingredients = [i for i in ingredients['data'] if i['name'] in update_new_ingredients]
            for i in new_ingredients:
                del i['_id']

            update_item = MenuItem(
                id=None,
                name=update_new_name or None,
                price=update_new_price if update_new_price else None,
                ingredients=new_ingredients or None,
                addedToMenu=None
            )

            res = updateMenuItem(update_mode, update_ids, update_item)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating menu item: {res['message']}")
        except:
            st.error("IDs must be integers")

elif choice == "Delete Menu Items":
    st.subheader("Delete Menu Items")
    delete_search_id = st.text_input("Menu Item ID (Multiple or single)")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete Menu Item"):
        try:
            if delete_search_id:
                delete_ids = [int(i) for i in delete_search_id.split(",")] if "," in delete_search_id else int(delete_search_id)
            else:
                delete_ids = None

            res = deleteMenuItem(delete_ids, delete_mode)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error deleting menu item: {res['message']}")
        except:
            st.error("IDs must be integers")