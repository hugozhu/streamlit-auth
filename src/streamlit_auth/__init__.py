import streamlit as st
from typing import Optional, Dict

from .google_auth import get_logged_in_user as get_google_user, show_login_button as show_google_login_button

from .keycloak_auth import get_logged_in_user as get_keycloak_user, show_login_button as show_keycloak_login_button

def get_oauth_provider() -> str:
    try:
        return st.secrets["oauth"]['provider']
    except KeyError:
        return "keycloak"
    
oauth_provider = get_oauth_provider()

def add_auth(required=True):        
    user_info = get_logged_in_user()    
    if oauth_provider == 'keycloak':
        if not user_info:
            show_keycloak_login_button()
            st.stop()
        else:
            st.sidebar.write(user_info['email'])
            
        if st.sidebar.button("Logout", type="primary"):    
            del st.session_state.login_user
            st.session_state.pop('email', None)            
            import webbrowser
            webbrowser.open_new_tab(st.secrets["oauth"]["keycloak"]['logout_url'])
            st.experimental_rerun()

    if oauth_provider == 'google':
        if not user_info:
            show_google_login_button()   
            st.stop()
        else:
            st.sidebar.write(user_info['email'])

        if st.sidebar.button("Logout", type="primary"):
            st.session_state.pop('login_user', None)
            st.session_state.pop('email', None)
            st.experimental_rerun()

def get_logged_in_user() -> Optional[Dict]:
    if "login_user" in st.session_state:
        return st.session_state.login_user
    
    if oauth_provider == 'keycloak':
        user_info = get_keycloak_user()
        if user_info:
            st.session_state.login_user = user_info
            return user_info        

    if oauth_provider == 'google':
        user_info = get_google_user()
        if user_info:
            st.session_state.login_user = user_info
            return user_info
    
    return None