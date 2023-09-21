import streamlit as st

st.set_page_config(layout="wide")
st.title("🎈 Hello World! 🎈")
st.balloons()

from streamlit_auth import require_auth, add_auth

auth = add_auth()

st.write(auth)

st.write(st.cache_data)


st.write("Congrats, you are logged in!")
st.write('the email of the user is ' + str(auth["email"]))