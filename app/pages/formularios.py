import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.formulariosFunctions import queryFormularios, display_summary_card

st.title("Resúmenes")
menu = ["Resumen Ingredientes", "Resumen Cuisines", "Resumen Menu Items", "Resumen Órdenes", "Resumen Restaurantes", "Resumen Reviews", "Resumen Usuarios"]

choice = st.selectbox("Seleccione un resumen por visualizar", menu)


if choice == "Resumen Ingredientes":
    data = queryFormularios(choice)
    st.write(data)
    st.subheader("Resumen Ingredientes")
    if data and data['status']==200:
        st.session_state.summary_data = data['data']
        if st.session_state.summary_data:
            cols = st.columns(3)
            for i, item in enumerate(st.session_state.summary_data):
                with cols[i % 3]:
                    display_summary_card(item)
        else:
            st.write("No se encontró el Resumen de Ingredientes")
    else:
        st.write("Error al obtener el Resumen de Ingredientes")

elif choice == "Resumen Cuisines":
    data = queryFormularios(choice)
    st.subheader("Resumen Cuisines")
    if data and data['status']==200:
        st.session_state.summary_data = data['data']
        if st.session_state.summary_data:
            cols = st.columns(2)
            for i, item in enumerate(st.session_state.summary_data):
                with cols[i % 2]:
                    display_summary_card(item)
        else:
            st.write("No se encontró el Resumen de Cuisines")
    else:
        st.write("Error al obtener el Resumen de Cuisines")

elif choice == "Resumen Menu Items":
    data = queryFormularios(choice)
    st.subheader("Resumen Menu Items")
    if data and data['status']==200:
        st.session_state.summary_data = data['data']
        if st.session_state.summary_data:
            cols = st.columns(3)
            for i, item in enumerate(st.session_state.summary_data):
                with cols[i % 3]:
                    display_summary_card(item)
        else:
            st.write("No se encontró el Resumen de Menu Items")
    else:
        st.write("Error al obtener el Resumen de Menu Items")

elif choice == "Resumen Órdenes":
    choice2 = st.selectbox("Seleccione un resumen por visualizar", ["Resumen General", "Resumen por Status"])
    if choice2 == "Resumen General":
        data = queryFormularios("Resumen Órdenes")
        st.subheader("Resumen General de Órdenes")
        if data and data['status']==200:
            st.session_state.summary_data = data['data']
            if st.session_state.summary_data:
                cols = st.columns(1)
                for i, item in enumerate(st.session_state.summary_data):
                    with cols[i % 1]:
                        display_summary_card(item)
            else:
                st.write("No se encontró el Resumen General de Órdenes")
        else:
            st.write("Error al obtener el Resumen General de Órdenes")
    elif choice2 == "Resumen por Status":
        data = queryFormularios("Resumen Órdenes por Status")
        st.subheader("Resumen por Status de Órdenes")
        if data and data['status']==200:
            st.session_state.summary_data = data['data']
            if st.session_state.summary_data:
                cols = st.columns(3)
                for i, item in enumerate(st.session_state.summary_data):
                    with cols[i % 3]:
                        display_summary_card(item)
            else:
                st.write("No se encontró el Resumen por Status de Órdenes")
        else:
            st.write("Error al obtener el Resumen por Status de Órdenes")
elif choice == "Resumen Restaurantes":
    data = queryFormularios(choice)
    st.subheader("Resumen Restaurantes")
    if data and data['status']==200:
        ids = []
        for item in data['data']:
            ids.append(item['id'])
        choice2 = st.selectbox("Seleccione el restaurante para visualizar su resumen", ids)
        eleccion = [item for item in data['data'] if item['id'] == choice2]
        st.session_state.summary_data = eleccion
        if st.session_state.summary_data:
            cols = st.columns(1)
            for i, item in enumerate(st.session_state.summary_data):
                with cols[i % 1]:
                    display_summary_card(item)
        else:
            st.write("No se encontró el Resumen del Restaurante")
    else:
        st.write("Error al obtener el Resumen de Restaurantes")

elif choice == "Resumen Reviews":
    data = queryFormularios(choice)
    st.subheader("Resumen Reviews")
    if data and data['status']==200:
        st.session_state.summary_data = data['data']
        if st.session_state.summary_data:
            cols = st.columns(1)
            for i, item in enumerate(st.session_state.summary_data):
                with cols[i % 1]:
                    display_summary_card(item)
        else:
            st.write("No se encontró el Resumen de Reviews")
    else:
        st.write("Error al obtener el Resumen de Reviews")

elif choice == "Resumen Usuarios":
    choice2 = st.selectbox("Seleccione un resumen por visualizar", ["Resumen General", "Resumen por usuario individual"])
    if choice2 == "Resumen General":
        data = queryFormularios("Resumen Usuario Promedio")
        st.subheader("Resumen General de Usuarios (Average User)")
        if data and data['status']==200:
            st.session_state.summary_data = data['data']
            if st.session_state.summary_data:
                cols = st.columns(1)
                for i, item in enumerate(st.session_state.summary_data):
                    with cols[i % 1]:
                        display_summary_card(item)
            else:
                st.write("No se encontró el Resumen General de Usuarios")
        else:
            st.write("Error al obtener el Resumen General de Usuarios")
    elif choice2 == "Resumen por usuario individual":
        data = queryFormularios("Resumen Por Usuario")
        st.subheader("Resumen por usuario individual")
        if data and data['status']==200:
            ids = []
            for item in data['data']:
                ids.append(item['id'])
            choice3 = st.selectbox("Seleccione el usuario para visualizar su resumen", ids)
            eleccion = [item for item in data['data'] if item['id'] == choice3]
            st.session_state.summary_data = eleccion
            if st.session_state.summary_data:
                cols = st.columns(1)
                for i, item in enumerate(st.session_state.summary_data):
                    with cols[i % 1]:
                        display_summary_card(item)
            else:
                st.write("No se encontró el Resumen del Usuario")
        else:
            st.write("Error al obtener el Resumen del Usuario")


