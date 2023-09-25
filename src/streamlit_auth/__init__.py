import streamlit as st
from typing import Optional, Dict
import extra_streamlit_components as stx
import uuid
from .google_auth import get_logged_in_user as get_google_user, show_login_button as show_google_login_button

from .keycloak_auth import get_logged_in_user as get_keycloak_user, show_login_button as show_keycloak_login_button

from streamlit.logger import get_logger

logger = get_logger(__name__)

st.cache_data.login_users = {}

def new_session_id():
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

def get_sssion_id():
    uuid = cookie_manager.get("uuid")
    if uuid is None:
        uuid = st.session_state.get("uuid")
    return uuid

def get_login():
    uuid = get_sssion_id()
    # logger.info("--uuid -%s---%s", uuid, cookie_manager)    
    if uuid is not None:
        return st.cache_data.login_users.get(uuid)

    return None

def require_auth(message="Please sign in"):
    if login := get_login():
        return login

    if message:
        st.warning(message, icon="⚠️")

    st.stop()

def add_auth(required=True, show_login_button=True, show_sidebar=True):
    user_info = get_logged_in_user()   
    if show_login_button:
        if not user_info:
            if oauth_provider == 'keycloak':
                show_keycloak_login_button()
            if oauth_provider == 'google':    
                show_google_login_button()       
            st.stop()        

    if show_sidebar:
        st.sidebar.write(user_info['email'])
        if oauth_provider == 'keycloak':
            if st.sidebar.button("Logout", type="primary"):
                uuid = cookie_manager.get("uuid")
                if uuid is not None:
                    uuid = ""
                else:
                    cookie_manager.delete("uuid")
                    st.session_state.pop('uuid', None)
                    st.cache_data.login_users.pop(uuid, None)            
                st.sidebar.markdown(f"""
                        <a id="keycloak-btn" href="javascript:void(0);"></a>
                    """, unsafe_allow_html=True)
                from streamlit.components.v1 import html
                html(f"""
                    <script>
                        function redirectToKeycloak() {{
                            window.top.document.getElementById('keycloak-link').click();
                        }}
                        window.parent.document.getElementById('keycloak-btn').addEventListener("click", function(event) {{
                            redirectToKeycloak();
                            event.preventDefault();
                        }}, false);
                     
                        // Create iframe element
                        const redirect_link = document.createElement('a');
                        redirect_link.href = '{st.secrets["oauth"]["keycloak"]['logout_url']}';
                        redirect_link.target = '_top';
                        redirect_link.innerText = 'Invisible Link';
                        redirect_link.style = 'display:none;';
                        redirect_link.id = 'keycloak-link';
                        window.top.document.body.appendChild(redirect_link);
                        redirectToKeycloak();
                    </script>
                """) 

        if oauth_provider == 'google':
            if st.sidebar.button("Logout", type="primary"):
                uuid = get_sssion_id()
                if uuid is None:
                    uuid = ""                
                cookie_manager.delete("uuid")
                st.session_state.pop('uuid', None)
                st.cache_data.login_users.pop(uuid, None)
                st.experimental_rerun()

    return user_info

def get_logged_in_user() -> Optional[Dict]:
    login = get_login()
    #logger.info("--get_login -%s---", login)

    if login is not None:
        return login
    
    if oauth_provider == 'keycloak':
        user_info = get_keycloak_user()
        # logger.info("--keycloak -%s---", user_info)
        
    if oauth_provider == 'google':
        try:
            user_info = get_google_user()
            logger.info("--google -%s---", user_info)
        except:
            logger.info("parse google callback url error")
            user_info = None

    if user_info:
        uuid = new_session_id()
        cookie_manager.set("uuid", uuid)
        st.session_state["uuid"] = uuid
        # logger.info("--uuid -%s-: %s--%s", uuid, user_info, cookie_manager.get('uuid'))        
        st.cache_data.login_users[uuid] = user_info
        return user_info
    
    return None