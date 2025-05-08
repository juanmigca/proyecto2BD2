import streamlit as st
import requests
from utils.models import Ingredient

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

def queryIngredients(name=None, amount=None, unitMeasure=None, limit=10, sort="name"):
    url = f"{st.session_state.host}/ingredients"
    params = {
        "name": name,
        "amount": amount,
        "unitMeasure": unitMeasure,
        "limit": limit,
        "sort": sort
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching ingredients: {response.status_code}")
        return None

def createIngredient(ingredient: Ingredient):
    url = f"{st.session_state.host}/ingredients"
    data = ingredient.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating ingredient: {response.status_code}")
        return None

def updateIngredient(mode, name, ingredient: Ingredient):
    params = {"find_name": name}
    if mode == "Single":
        url = f"{st.session_state.host}/ingredients"
    else:
        url = f"{st.session_state.host}/batch/ingredients"
    builtUrl = urlBuilder(url, params)
    response = requests.patch(builtUrl, json=ingredient.model_dump(exclude_unset=True))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error updating ingredient(s): {response.status_code}")
        return response.json()

def deleteIngredient(name, mode="Single"):
    params = {"find_name": name}
    if mode == "Single":
        url = f"{st.session_state.host}/ingredients"
    else:
        url = f"{st.session_state.host}/batch/ingredients"
    builtUrl = urlBuilder(url, params)
    response = requests.delete(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error deleting ingredient(s): {response.status_code}")
        return None

def display_ingredient_card(ingredient):
    with st.container():
       
        st.markdown(f"### **Name:** {ingredient.get('name', 'N/A')}")
        st.markdown(f"**Amount:** {ingredient.get('amount', 'N/A')}")
        st.markdown(f"**Unit:** {ingredient.get('unitMeasure', 'N/A')}")
        st.markdown(f"**Mongo _id:** {ingredient.get('_id', 'N/A')}")
