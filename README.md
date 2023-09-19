# streamlit-auth
Streamlit module for creating oauth protected Stramlit apps.

[![Releases](https://img.shields.io/pypi/v/st-paywall)](https://pypi.org/project/streamlit-auth/)

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
from st_paywall import add_auth

add_auth(required=True)

#after authentication, the email and subscription status is stored in session state
st.write(st.session_state.email)
st.write(st.session_state.user_subscribed)
```

If the `required` parameter is `True`, the app will stop with `st.stop()` if the user is not logged in and subscribed. Otherwise, you the developer will have control over exactly how you want to paywall the apps!

I hope you use this to create tons of value, and capture some of it with the magic of Streamlit.

This package expects that you have a `.streamlit/secrets.toml` file which you will have to create. Inside it, you will need to add your Stripe (or Buy Me A Coffee) and Google API information that runs the authentication and subscription parts of the package. If you already have all of your information for your payment and authentication providers, here is how the package expects your secrets file to look.

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