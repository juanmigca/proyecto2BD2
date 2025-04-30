import streamlit as st


st.session_state.host = 'http://127.0.0.1:8000'


st.set_page_config(page_title='Restaurant reviewer', page_icon='🍗', layout='wide', initial_sidebar_state='auto')


pages_nav = [
    st.Page("pages/home.py", title='Home'),
    st.Page("pages/restaurants.py", title='Restaurants'),
    st.Page("pages/menuItems.py", title='Menu Items'),
    st.Page("pages/users.py", title='Users'),
    st.Page("pages/orders.py", title='Orders'),
    st.Page("pages/reviews.py", title='Reviews'),
    ]


pg = st.navigation(pages_nav)
pg.run()

