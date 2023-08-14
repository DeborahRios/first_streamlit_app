import  streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites 🥣 🥗 🐔 🥑🍞')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocate Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)
# streamlit.dataframe(my_fruit_list)

def get_fruityvice_data (this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # streamlit.text(fruityvice_response.json())

    # take JSON response and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# new section to display Fruityvice API 
streamlit.header("Fruityvice Fruit Advice!")
try:
  #  Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit from to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # Output it the screen as a table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.header("The Fruit Load List Contains:")
# snowflake-related function 
def get_fruit_load_list():
    # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        # my_data_row = my_cur.fetchone()
        return my_cur.fetchall()
    


# add button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()

    streamlit.dataframe(my_data_row)

streamlit.stop()
fruit_choice = streamlit.text_input('What fruit would you like to Add?')
streamlit.write('Thanks for adding: ', fruit_choice)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
