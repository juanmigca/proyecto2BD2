import streamlit as st
import requests
from utils.models import Order


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


def queryOrders(id=None, user_id=None, restaurant_id=None, status=None,  limit=10):
    url = f'{st.session_state.host}/orders'
    params = {
        "id": id,
        "user_id": user_id,
        "restaurant_id": restaurant_id,
        "status": status,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching orders: {response.status_code}")
        return None


def createOrder(order: Order):
    url = f'{st.session_state.host}/orders'
    data = order.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error creating order: {response.status_code}")
        return None


def updateOrder(mode, id, update_data: Order):
    params = {
        "find_id": id
    }
    if mode == "Single":
        url = f'{st.session_state.host}/orders'
    else:
        url = f'{st.session_state.host}/batch/orders'
    builtUrl = urlBuilder(url, params)
    response = requests.patch(builtUrl, json=update_data.model_dump())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error updating order(s): {response.status_code}")
        return response.json()


def deleteOrder(id, mode="Single"):
    params = {
        "find_id": id
    }
    if mode == "Single":
        url = f'{st.session_state.host}/orders'
    else:
        url = f'{st.session_state.host}/batch/orders'
    builtUrl = urlBuilder(url, params)
    response = requests.delete(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error deleting order(s): {response.status_code}")
        return None


def display_order_card(order):
    with st.container():
        st.markdown(f"### Order ID: {order['id']}")
        st.markdown(f"**User ID:** {order.get('userId', 'N/A')}")
        st.markdown(f"**Restaurant ID:** {order.get('restaurantId', 'N/A')}")
        st.markdown(f"**Status:** {order.get('status', 'N/A')}")
        st.markdown(f"**Ordered At:** {order.get('orderedAt', 'N/A')}")
        st.markdown(f"**Arrived At:** {order.get('arrivedAt', 'N/A')}")
        with st.expander("Order Details", expanded=False):
            st.markdown(f"**Subtotal:** ${order.get('subtotal', 'N/A')}")
            st.markdown(f"**Tax:** ${order.get('tax', 'N/A')}")
            st.markdown(f"**Tip:** ${order.get('tip', 'N/A')}")
            st.markdown(f"**Total:** ${order.get('total', 'N/A')}")
            st.markdown("**Items:**")
            for item in order.get('items', []):
                st.markdown(f"- {item['name']} (x{item['quantity']}) - ${item['price']}")
              

