import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.orderFunctions import queryOrders, createOrder, updateOrder, deleteOrder, display_order_card
from helpers.restaurantFunctions import queryRestaurants
from utils.models import User, Order

st.session_state.order_data = Order()
st.session_state.temp_items = []

st.title("Orders")

menu = ["Create Order", "Find Orders", "Update Orders", "Delete Orders"]
choice = st.selectbox("Select an option", menu)

# Create Order
if choice == "Create Order":
    with st.form(key='create_order_form'):

        restaurants = queryRestaurants(limit=1000)
        st.subheader("Create Order")
        order_id = st.number_input("Order ID", min_value=1, step=1)
        user_id = st.number_input("User ID", min_value=1, step=1)
        restaurant_id = st.selectbox("Restaurant ID", [restaurant['id'] for restaurant in restaurants['data']])
        restaurant_selected = next((restaurant for restaurant in restaurants['data'] if restaurant['id'] == restaurant_id), None)
        

        
            

        submit_button = st.form_submit_button(label='Seleccionar Restaurante')
        if submit_button:
            st.session_state.order_data = Order(
                id=int(order_id),
                userId=int(user_id),
                restaurantId=int(restaurant_id),
                items=[]
            
            )
        
    st.subheader("Order Items")
    with st.form(key='order_items_form'):
        if restaurant_selected:
            st.write(f"Selected Restaurant: {restaurant_selected['name']}")
            st.session_state.temp_items = []
            menu_items = restaurant_selected.get('menuItems', [])
            for item in menu_items:
                item_id = item['id']
                item_name = item['name']
                item_price = item['price']
                quantity = st.number_input(f"Quantity of {item_name} (ID: {item_id})", min_value=0, step=1, key=f"quantity_{item_id}")
                if quantity > 0:
                    st.session_state.temp_items.append({
                        'id': item_id,
                        'name': item_name,
                        'price': item_price,
                        'ingredients': item.get('ingredients', []),
                        'addedToMenu': item.get('addedToMenu', None),
                        'quantity': quantity
                    })
                    
            

            submit_button = st.form_submit_button(label='Create Order')
            if submit_button:
                # keep only latest for each item
                st.session_state.order_data.items = []
                for item in st.session_state.temp_items:
                    if item not in st.session_state.order_data.items:
                        st.session_state.order_data.items.append(item)
                st.session_state.order_data.subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.order_data.items)
                st.session_state.order_data.tax = 0.12 * st.session_state.order_data.subtotal
    
    st.subheader("Order Summary")
    with st.form(key='order_summary_form'):
        if st.session_state.order_data.items:
            st.write("Items:")
            for item in st.session_state.order_data.items:
                st.write(f"{item['name']} (ID: {item['id']}) - Quantity: {item['quantity']} - Price: ${item['price']:.2f}")
            st.write(f"Subtotal: ${st.session_state.order_data.subtotal:.2f}")
            st.write(f"Tax: ${st.session_state.order_data.tax:.2f}")
        
            tip = st.number_input("Tip", min_value=0.0, step=0.01, format="%.2f")

        submit_button = st.form_submit_button(label='Submit Order')
        if submit_button:
            st.session_state.order_data.tip = tip
            st.session_state.order_data.total = st.session_state.order_data.subtotal + st.session_state.order_data.tax + tip
            res = createOrder(st.session_state.order_data)
            #st.write(st.session_state.order_data)
            if res and res['status'] == 200:
                st.success("Order created successfully! Total: ${:.2f}".format(st.session_state.order_data.subtotal + st.session_state.order_data.tax + tip))
            else:
                #st.write(res)
                st.error("Error creating order.")
  

                
              

# Find Orders
elif choice == "Find Orders":
    st.subheader("Find Orders")
    search_id = st.text_input("Search by Order ID")
    search_user_id = st.text_input("Search by User ID")
    search_restaurant_id = st.text_input("Search by Restaurant ID")
    search_status = st.selectbox("Search by Status", ["", "pending", "completed", "cancelled"])
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("Find Orders"):
        try:
            ids = [int(i) for i in search_id.split(",")] if "," in search_id else int(search_id) if search_id else None
            user_ids = [int(i) for i in search_user_id.split(",")] if "," in search_user_id else int(search_user_id) if search_user_id else None
            rest_ids = [int(i) for i in search_restaurant_id.split(",")] if "," in search_restaurant_id else int(search_restaurant_id) if search_restaurant_id else None
            status = search_status or None
            

            data = queryOrders(ids, user_ids, rest_ids, status, limit)

            if data and data['status'] == 200:
                st.session_state.orders = data['data']
                if st.session_state.orders:
                    cols = st.columns(2)
                    for i, order in enumerate(st.session_state.orders):
                        with cols[i % 2]:
                            display_order_card(order)
                else:
                    st.info("No orders found.")
            else:
                st.error("Error fetching orders.")
        except:
            st.error("IDs must be integers")

# Update Orders
elif choice == "Update Orders":
    st.subheader("Update Order")
    st.subheader("Find")
    update_search_id = st.text_input("Order ID (Multiple e.g. 1,3,4)")
    update_mode = st.selectbox("Update mode", ["Single", "Multiple"])

    st.subheader("Update")
    new_status = st.selectbox("New Status", ["", "En Camino", "Entregado", "Cancelado"])
    new_fecha = st.date_input("New Arrived At", value=None)
    new_hora = st.time_input("New Arrived At Time", value=None)

    if st.button("Update Order"):
        try:
            update_ids = [int(i) for i in update_search_id.split(",")] if "," in update_search_id else int(update_search_id)
            fecha_hora = datetime.combine(new_fecha, new_hora) if new_fecha and new_hora else None
            order_update = Order(
                id=None,
                status=new_status if new_status else None,
                arrivedAt=fecha_hora.strftime("%Y-%m-%d %H:%M:%S") if fecha_hora else None
            )
            res = updateOrder(update_mode, update_ids, order_update)
            if res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error updating order: {res['message']}")
        except:
            st.error("IDs must be integers")

# Delete Orders
elif choice == "Delete Orders":
    st.subheader("Delete Orders")
    delete_search_id = st.text_input("Order ID (Multiple or single)")
    delete_mode = st.selectbox("Delete mode", ["Single", "Multiple"])

    if st.button("Delete Order"):
        try:
            delete_ids = [int(i) for i in delete_search_id.split(",")] if "," in delete_search_id else int(delete_search_id)
            res = deleteOrder(delete_ids, delete_mode)
            if res and res['status'] == 200:
                st.success(f"Success! {res['message']}!")
            else:
                st.error(f"Error deleting order: {res['message']}")
        except:
            st.error("IDs must be integers")
            
