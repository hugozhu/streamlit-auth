import streamlit as st
from typing import Optional, Dict

from streamlit_keycloak import login

url = st.secrets["oauth"]["keycloak"]["url"]
realm = st.secrets["oauth"]["keycloak"]["realm"]
client_id = st.secrets["oauth"]["keycloak"]['client_id']

def get_logged_in_user() -> Optional[Dict]:
    keycloak = login(
        url=url,
        realm=realm,
        client_id=client_id,
    )

    if keycloak.authenticated:
        return keycloak.user_info
    
    return None

def markdown_label(
    text: str, color="#FD504D", sidebar: bool = True
):
    markdown = st.sidebar.markdown if sidebar else st.markdown

    markdown(
        f"""
        <div style="
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: {color};
            color: rgb(255, 255, 255);
            border: 1px solid rgb(255, 75, 75);
            text-decoration: none;
            ">
            {text}
        </div>
    """,
        unsafe_allow_html=True,
    )

def show_login_button():
    markdown_label("Please sign in ...")
