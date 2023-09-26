import streamlit as st

import os
import sys
# 将当前目录的 src 文件夹添加到 sys.path 中
src_dir = os.path.join(os.getcwd(), 'src')
sys.path.insert(0, src_dir)

st.set_page_config(layout="wide")
st.title("🎈 Hello World! 🎈")
st.balloons()

from streamlit_auth import require_auth, add_auth

auth = add_auth(True, True, False)

st.write(auth)

st.write("Congrats, you are logged in!")
st.write('the email of the user is ' + str(auth["email"]))