from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
# Force localhost instead of 127.0.0.1 for consistent URLs with Cognito
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['PREFERRED_URL_SCHEME'] = 'http'
oauth = OAuth(app)

# Get credentials from environment variables
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-west-2')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')

oauth.register(
  name='oidc',
  authority=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}',
  client_id=COGNITO_CLIENT_ID,
  client_secret=COGNITO_CLIENT_SECRET,
  server_metadata_url=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/openid-configuration',
  client_kwargs={'scope': 'email openid phone'}
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return  f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect('https://d84l1y8p4kdic.cloudfront.net')

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    
    # Get the metadata
    metadata = oauth.oidc.load_server_metadata()
    end_session_endpoint = metadata.get('end_session_endpoint')
    
    # Fallback if metadata doesn't provide the explicit logout endpoint
    # (Cognito metadata usually includes it, but it's good to be safe)
    if not end_session_endpoint:
        # Construct it manually based on your domain
        COGNITO_DOMAIN = "https://us-west-28flvcdjq7.auth.us-west-2.amazoncognito.com"
        end_session_endpoint = f"{COGNITO_DOMAIN}/logout"

    client_id = COGNITO_CLIENT_ID
    
    # IMPORTANT: This URL must match EXACTLY what is in your AWS Console "Allowed sign-out URLs"
    # If your console has a trailing slash (http://localhost:5000/), this must also have it.
    logout_uri = url_for('index', _external=True)

    # 1. Use 'logout_uri' instead of 'post_logout_redirect_uri'
    # 2. Use quote_plus to safely encode the URL characters
    cognito_logout_url = (
        f'{end_session_endpoint}?'
        f'client_id={client_id}&'
        f'logout_uri={quote_plus(logout_uri)}'
    )
    
    return redirect(cognito_logout_url)

if __name__ == '__main__':
    app.run(debug=True)
