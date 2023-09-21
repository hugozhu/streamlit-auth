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


st.sidebar.markdown(f"""
        <a id="keycloak-btn" href="javascript:void(0);"></a>
    """, unsafe_allow_html=True)

from streamlit.components.v1 import html

html(f"""
    <script>
        function redirectToKeycloak() {{
            window.top.document.getElementById('keycloak-link').click();
        }}
        window.parent.document.getElementById('keycloak-btn').addEventListener("transitionend", function(event) {{
        	alert("hello")
            redirectToKeycloak();
            event.preventDefault();
        }}, false);
     
        redirectToKeycloak();
        event.preventDefault();     

        // Create iframe element
        const redirect_link = document.createElement('a');
        redirect_link.href = '{st.secrets["oauth"]["keycloak"]['logout_url']}';
        redirect_link.target = '_top';
        redirect_link.innerText = 'Invisible Link';
        redirect_link.style = 'display:none;';
        redirect_link.id = 'keycloak-link';
        window.top.document.body.appendChild(redirect_link);
    </script>
""") 
