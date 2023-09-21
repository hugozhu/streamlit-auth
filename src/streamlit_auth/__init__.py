import streamlit as st
from typing import Optional, Dict
import extra_streamlit_components as stx
import uuid
from .google_auth import get_logged_in_user as get_google_user, show_login_button as show_google_login_button

from .keycloak_auth import get_logged_in_user as get_keycloak_user, show_login_button as show_keycloak_login_button

st.cache_data.login_users = {}

def gen_session_id():
    return uuid.uuid4().hex

@st.cache_data
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

def get_oauth_provider() -> str:
    try:
        return st.secrets["oauth"]['provider']
    except KeyError:
        return "keycloak"
    
oauth_provider = get_oauth_provider()

def get_login():
    if "login_user" in st.session_state:
        if "email" in st.session_state.login_user:
            return st.session_state.login_user

    if uuid := cookie_manager.get('uuid'):
        return st.cache_data.login_users.get(uuid)

    return None

def require_auth(message="Please sign in"):
    if login := get_login():
        return login

    if message:
        st.warning(message, icon="⚠️")
    st.stop()

def add_auth(required=True, show_sidebar=True):
    user_info = get_logged_in_user()    
    if oauth_provider == 'keycloak':
        if not user_info:
            show_keycloak_login_button()
            st.stop()

        if show_sidebar:
            st.sidebar.write(user_info['email'])            
            if st.sidebar.button("Logout", type="primary"):    
                del st.session_state.login_user
                st.session_state.pop('email', None)
                uuid = cookie_manager.get("uuid")
                cookie_manager.delete(uuid)
                del st.cache_data.login_users[uuid]
                import webbrowser
                webbrowser.open(st.secrets["oauth"]["keycloak"]['logout_url'])
                st.experimental_rerun()            

    if oauth_provider == 'google':
        if not user_info:
            show_google_login_button()   
            st.stop()
        
        if show_sidebar:
            st.sidebar.write(user_info['email'])
            if st.sidebar.button("Logout", type="primary"):            
                st.session_state.pop('login_user', None)
                st.session_state.pop('email', None)
                uuid = cookie_manager.get("uuid")
                cookie_manager.delete(uuid)                
                del st.cache_data.login_users[uuid]
                st.experimental_rerun()

    return user_info

def get_logged_in_user() -> Optional[Dict]:
    login = get_login()
    if login != None:
        return login
    
    if oauth_provider == 'keycloak':
        user_info = get_keycloak_user()
        if user_info:
            uuid = gen_session_id()
            cookie_manager.set("uuid", uuid)
            st.session_state.login_user = user_info
            st.cache_data.login_users[uuid] = user_info
            return user_info        

    if oauth_provider == 'google':
        user_info = get_google_user()
        if user_info:
            cookie_manager.set("uuid", gen_session_id())
            st.session_state.login_user = user_info
            st.cache_data.login_users[uuid] = user_info
            return user_info
    
    return None