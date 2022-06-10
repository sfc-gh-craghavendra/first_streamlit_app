import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt").set_index("Fruit")

# Let's put a pick list so that the user can pick the fruit they want to include in the smoothie
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Watermelon','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

# define a function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display Fruityvice Advice!
streamlit.header('FruityVice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))

except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
# Snowflake related functions

def get_fruitload_list():
    with my_cnx.cursor() as my_cur:
        return my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.dataframe(get_fruitload_list)


streamlit.stop()

fruit_choice = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit');")