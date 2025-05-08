import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.ingredientFunctions import queryIngredients, createIngredient, updateIngredient, deleteIngredient, display_ingredient_card
from utils.models import Ingredient

if "ingredient_data" not in st.session_state:
    st.session_state.ingredient_data = Ingredient()

st.title("Ingredients")

menu = ["Create Ingredient", "Find Ingredients", "Update Ingredients", "Delete Ingredients"]
choice = st.selectbox("Select an option", menu)

# Create
if choice == "Create Ingredient":
    with st.form(key='create_ingredient_form'):
        st.subheader("Create Ingredient")
        name = st.text_input("Name")
        amount = st.number_input("Amount", min_value=0.0)
        unit = st.text_input("Unit of Measure")

        submit_button = st.form_submit_button(label='Submit Ingredient')
        if submit_button:
            st.session_state.ingredient_data = Ingredient(name=name, amount=amount, unitMeasure=unit)
            res = createIngredient(st.session_state.ingredient_data)
            if res and res['status'] == 200:
                st.success("Ingredient created successfully!")
            else:
                st.error("Error creating ingredient")

# Read
elif choice == "Find Ingredients":
    st.subheader("Find Ingredients")
    name = st.text_input("Search by Name")
    amount = st.text_input("Amount")
    unit = st.text_input("Unit of Measure")
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("Find Ingredients"):
        try:
            names = name.split(",") if name else None
            amounts = amount.split(",") if amount else None
            amount_parsed = [float(a) for a in amounts] if amounts else None
            units = unit.split(",") if unit else None
            data = queryIngredients(name=names, amount=amount_parsed, unitMeasure=units, limit=limit)
            if data and data['status'] == 200:
                cols = st.columns(3)
                for i, ingredient in enumerate(data['data']):
                    with cols[i % 3]:
                        display_ingredient_card(ingredient)
                    
            else:
                st.error("Error fetching ingredients")
        except:
            st.error("Amount must be a number or comma-separated list")

# Update
elif choice == "Update Ingredients":
    st.subheader("Update Ingredient")
    ingredient_id = st.text_input("Name of Ingredient to Update")
    name = st.text_input("New Name")
    amount = st.number_input("New Amount", min_value=0.0, format="%.2f")
    unit = st.text_input("New Unit of Measure")

    if st.button("Update Ingredient"):
        try:
            new_data = Ingredient(name=name or None, amount=amount or None, unitMeasure=unit or None)
            res = updateIngredient("Single", ingredient_id, new_data)
            if res and res['status'] == 200:
                st.success("Ingredient updated successfully!")
            else:
                st.error("Error updating ingredient")
        except:
            st.error("Invalid ID")

# Delete
elif choice == "Delete Ingredients":
    st.subheader("Delete Ingredient(s)")
    delete_id = st.text_input("Name of Ingredient(s) to Delete")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete Ingredient"):
        try:
            ids = delete_id.split(",") if delete_mode == "Multiple" else delete_id
            res = deleteIngredient(ids, delete_mode)
            if res and res['status'] == 200:
                st.success("Ingredient(s) deleted successfully!")
            else:
                st.error("Error deleting ingredient(s)")
        except:
            st.error("Invalid ID(s)")
