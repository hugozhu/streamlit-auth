import streamlit as st
from streamlit_auth import add_auth

st.set_page_config(layout="wide")
st.title("🎈 Hello World! 🎈")
st.balloons()

add_auth()

st.write("Congrats, you are logged in!")
st.write('the email of the user is ' + str(st.session_state.login_user["email"]))