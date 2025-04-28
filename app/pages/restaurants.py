import streamlit as st
import requests

if "restaurants" not in st.session_state:
    st.session_state.restaurants = []
if "selected_restaurant_id" not in st.session_state:
    st.session_state.selected_restaurant_id = None


def urlBuilder(url, params=None):
    """
    Constructs a full URL by combining a base URL with an endpoint and optional query parameters.

    Args:
        base_url (str): The base URL.
        endpoint (str): The endpoint to append to the base URL.
        params (dict, optional): A dictionary of query parameters to include in the URL.

    Returns:
        str: The constructed full URL.
    """
    url = url + '?'
    
    for k,v in params.items():
        if v is not None and v != '':
            if isinstance(v, list):
                for i in v:
                    url += f'{k}={i}&'
            else:
                url += f'{k}={v}&'
    
    return url[:-1]
        


def queryRestaurants(id=None, name=None, cuisines=None, limit=10):
    params = {
        "id": id,
        "name": name,
        "cuisine": cuisines,
        "limit": limit
    }


    url  = f'{st.session_state.host}/restaurants'
    builtUrl = urlBuilder(url, params)
    response = requests.get(builtUrl)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching restaurants: {response.status_code}")
        return None
    
def queryCuisines():



    url  = f'{st.session_state.host}/cuisines'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching cuisines: {response.status_code}")
        return None
    

def display_restaurant_card(restaurant):
    with st.container():
        st.markdown(f"### {restaurant['name']}")
        st.markdown(f"**Cuisines:** {', '.join(restaurant['cuisines'])}")
        st.markdown(f"**Rating:** {round(float(restaurant['rating']),2)}/10")

        # Expander for additional details
        with st.expander("Details"):
            st.markdown(f"**Location:** Longitud: {restaurant['location']['coordinates'][0]}, Latitud: {restaurant['location']['coordinates'][1]}")
            st.markdown(f"**Address:** {restaurant['address']}")
            st.markdown(f"**Number of Reviews:** {restaurant['numReviews']}")
            
  
        with st.expander("Menu Items"):
            if restaurant['menuItems']:
                for item in restaurant['menuItems']:
                    st.markdown(f"- {item['name']} - ${item['price']}")
                    st.markdown(f"**Added to Menu:** {item['addedToMenu']}")
                    st.markdown(f"**Ingredients:** {', '.join([i['name'] + ' ' + str(i['amount']) + str(i['unitMeasure']) for i in item['ingredients']])}")
        
    
            else:
                st.write("No menu items available.")

        
        
        

            


    


st.title("Restaurants")

st.write("This is the restaurants page.")

menu = ["Create Restaurant", "Find Restaurants", "Update Restaurant", "Delete Restaurant"]

choice = st.selectbox("Select an option", menu)

### Logica CRUD



# Create a restaurant
if choice == "Create Restaurant":
    with st.form(key='create_restaurant_form'):
        cuisines = queryCuisines()

        st.subheader("Create Restaurant")
        restaurant_name = st.text_input("Restaurant Name")
        restaurant_location = st.text_input("Restaurant Location")

        restaurant_rating = st.number_input("Rating", min_value=1, max_value=5, value=3)
        create_cuisines = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
            
            
        submit_button = st.form_submit_button(label='Create Restaurant')
        
        if submit_button:
            # Here you would typically call a function to create the restaurant in the database
            st.success(f"Restaurant '{restaurant_name}' created successfully!")


elif choice == "Find Restaurants":
    st.subheader("Find Restaurants")
    cuisines = queryCuisines()
    search_id = st.text_input("Search by Restaurant ID")
    search_name = st.text_input("Search by Restaurant Name")
    search_cuisine = st.multiselect("Cuisines", [i['name'] for i in cuisines['data']])
    limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
    
    if st.button("Find Restaurants"):
        print(search_id, search_name, search_cuisine)
        data = None
        data = queryRestaurants(id=search_id, name=search_name, cuisines=search_cuisine, limit=limit)
        print(data)
        if data is not None and data['status'] == 200:
            st.session_state.restaurants = data['data']
         
            if st.session_state.restaurants:
                numRestaurants = len(st.session_state.restaurants)
                
                cols = st.columns(3)
                for i, restaurant in enumerate(st.session_state.restaurants):
                    with cols[i % 3]:
                        display_restaurant_card(restaurant)
            else:
                st.write("No restaurants found.")
           
                    
        
        else:
            st.error("Error fetching restaurants.")
        # Here you would typically call a function to find restaurants in the database
      

elif choice == "Update Restaurant":
    st.subheader("Update Restaurant")
    restaurant_id = st.text_input("Restaurant ID")
    new_name = st.text_input("New Restaurant Name")
    new_location = st.text_input("New Restaurant Location")
    new_cuisine = st.text_input("New Cuisine Type")
    new_rating = st.number_input("New Rating", min_value=1, max_value=5, value=3)
    
    if st.button("Update Restaurant"):
        # Here you would typically call a function to update the restaurant in the database
        st.success(f"Restaurant '{restaurant_id}' updated successfully!")

elif choice == "Delete Restaurant":
    st.subheader("Delete Restaurant")
    restaurant_id = st.text_input("Restaurant ID")
    
    if st.button("Delete Restaurant"):
        # Here you would typically call a function to delete the restaurant from the database
        st.success(f"Restaurant '{restaurant_id}' deleted successfully!")

