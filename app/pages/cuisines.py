import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.cuisineFunctions import (
    queryCuisines,
    createCuisine,
    updateCuisine,
    deleteCuisine,
    display_cuisine_card
)
from utils.models import Cuisines

if "cuisine_data" not in st.session_state:
    st.session_state.cuisine_data = Cuisines()

st.title("Cuisines")

menu = ["Create Cuisine", "Find Cuisines", "Update Cuisine", "Delete Cuisines"]
choice = st.selectbox("Select an option", menu)

# Create
if choice == "Create Cuisine":
    with st.form(key='create_cuisine_form'):
        st.subheader("Create Cuisine")
        #cuisine_id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")

        submit_button = st.form_submit_button(label='Submit Cuisine')
        if submit_button:
            st.session_state.cuisine_data = Cuisines(id=None, name=name)
            res = createCuisine(st.session_state.cuisine_data)
            if res and res['status'] == 200:
                st.success("Cuisine created successfully!")
            else:
                st.error("Error creating cuisine")

# Read
elif choice == "Find Cuisines":
    st.subheader("Find Cuisines")
    name = st.text_input("Search by Name")
    ids = st.text_input("ID(s) separated by commas")
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("Find Cuisines"):
        id_list = [i.strip() for i in ids.split(",")] if ids else None
        name_list = name.split(",") if name else None
        data = queryCuisines(id=id_list, name=name_list, limit=limit)
        if data and data['status'] == 200:
            cols = st.columns(3)
            for i, cuisine in enumerate(data['data']):
                with cols[i % 3]:
                    display_cuisine_card(cuisine)
        else:
            st.error("Error fetching cuisines")

# Update
elif choice == "Update Cuisine":
    st.subheader("Update Cuisine")
    cuisine_id = st.text_input("ID of Cuisine to Update")
    name = st.text_input("New Name")

    if st.button("Update Cuisine"):
        try:
            new_data = Cuisines(id=int(cuisine_id), name=name or None)
            res = updateCuisine("Single", cuisine_id, new_data)
            if res and res['status'] == 200:
                st.success("Cuisine updated successfully!")
            else:
                st.error("Error updating cuisine")
        except:
            st.error("Invalid ID")

# Delete
elif choice == "Delete Cuisines":
    st.subheader("Delete Cuisine(s)")
    delete_id = st.text_input("ID(s) to Delete")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete Cuisine"):
        try:
            ids = delete_id.split(",") if delete_mode == "Multiple" else delete_id
            res = deleteCuisine(ids, delete_mode)
            if res and res['status'] == 200:
                st.success("Cuisine(s) deleted successfully!")
            else:
                st.error("Error deleting cuisine(s)")
        except:
            st.error("Invalid ID(s)")
