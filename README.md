# streamlit-auth
Streamlit module for creating oauth protected Stramlit apps.

[![Releases](https://img.shields.io/pypi/v/streamlit-auth)](https://pypi.org/project/streamlit-auth/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hugozhu.streamlit.app)


## Packaging
```sh
python3 -m pip install build
python3 -m build
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository pypi dist/*
```

## Local Installation
```
pip install dist/*.tar.gz
```

# streamlit-auth

<strong>A python package for creating oauth protected Stramlit apps! </strong>

## Documentation

Once you configure the authentication and subscription on `st.secrets`, you can use the the library methods to conditionally render the content of the page:

```python
import streamlit as st
from streamlit_auth import add_auth

add_auth()

st.write("Congrats, you are logged in!")
st.write('the email of the user is ' + str(st.session_state.login_user["email"]))

```toml
[oauth]
provider = "keycloak"

[oauth.google]
client_id = "....apps.googleusercontent.com"
client_secret = "GOCSPX-..."
redirect_url_test = 'http://localhost:8501/'
redirect_url = "http://localhost:8501/"

[oauth.keycloak]
url = 'https://keycloak.your-domain.com/auth'
realm = 'myrealm'
client_id = 'myclient'
logout_url = "https://keycloak.your-domain.com/auth/realms/myrealm/protocol/openid-connect/logout"
```