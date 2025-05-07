import streamlit as st
import requests
import json


def queryFormularios(tipo: str):
    """
    Queries the summary based on the given type.
    """
    url = f'{st.session_state.host}/summary'
    params = {
        "tipo": tipo
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching summary: {response.status_code}")
        return None
    
def display_summary_card(item):
    """
    Displays a summary card for the given item.
    """
    with st.container():
        for key, value in item.items():
            if key == 'id':
                continue
            if key == 'name' or key == 'cuisine' or key == '_id' or key == 'username':
                st.markdown(f"### {value}")

            if key == 'menuItems':
                with st.expander("Menu Items"):
                    for menu_item in value:
                        st.markdown(f"**ID:** {menu_item['id']}, **Name:** {menu_item['name']}, **Times Prepared:** {menu_item['timesPrepared']}")
            else:
                st.markdown(f"**{key}:** {value}")
