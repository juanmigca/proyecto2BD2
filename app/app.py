import streamlit as st



st.session_state.host = 'http://127.0.0.1:8000'


st.set_page_config(page_title='Restaurant reviewer', page_icon='🍗', layout='wide', initial_sidebar_state='auto')

pages = [
    st.Page("pages/restaurants_page.py", title='Restaurants'),
    st.Page("pages/menuItems_page.py", title='Menu Items'),
    st.Page("pages/users_page.py", title='Users'),
    st.Page("pages/orders_page.py", title='Orders'),
    st.Page("pages/reviews_page.py", title='Reviews'),
    ]

pg = st.navigation(pages)
pg.run()

