# Identity Management Playground

Flask application demonstrating AWS Cognito OIDC authentication for academic testing.

## Features

- ✅ AWS Cognito OIDC login/logout
- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Session management
- ✅ Proper OIDC logout flow

## Setup

### 1. Clone and Navigate
```bash
cd identity-mangement-playground
```

### 2. Create Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies
```bash
myenv/bin/pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your AWS Cognito credentials:
```env
COGNITO_REGION=us-west-2
COGNITO_USER_POOL_ID=your-pool-id
COGNITO_CLIENT_ID=your-client-id
COGNITO_CLIENT_SECRET=your-client-secret
FLASK_SECRET_KEY=your-secret-key-here
```

### 5. Configure AWS Cognito

In your AWS Cognito User Pool App Client settings:

**Allowed callback URLs:**
- `https://d84l1y8p4kdic.cloudfront.net`
- `http://localhost:5000/authorize` (if using local redirect)

**Allowed sign-out URLs:**
- `http://localhost:5000/`

## Running the Application

```bash
# Make sure you're in the virtual environment
source myenv/bin/activate  # or: myenv\Scripts\activate on Windows

# Run Flask
flask --app app run
```

Visit: **http://localhost:5000/**

## File Structure

```
identity-mangement-playground/
├── app.py                 # Main Flask application
├── .env                   # Environment variables (not in git)
├── .env.example           # Template for environment variables
├── .gitignore            # Git ignore rules
├── requirements.txt       # Python dependencies
└── myenv/                # Virtual environment (not in git)
```

## Security Notes

⚠️ **For Academic Testing Only**

This project is configured for local development and testing. The following security improvements are recommended before production use:
- Enable HTTPS
- Add CSRF protection
- Configure session timeouts
- Add security headers
- Use production WSGI server (not Flask dev server)

## How It Works

1. **Login Flow:**
   - User clicks "Login" → Redirects to Cognito
   - User authenticates → Cognito redirects back with authorization code
   - App exchanges code for tokens → Stores user info in session

2. **Logout Flow:**
   - User clicks "Logout" → Clears local session
   - Redirects to Cognito's logout endpoint → Invalidates Cognito session
   - Cognito redirects back to homepage

## Troubleshooting

**"This site can't be reached" error:**
- Ensure your Cognito domain is correct in `.env`
- Check that redirect URLs are whitelisted in AWS Console

**Sessions not persisting across restarts:**
- Make sure `FLASK_SECRET_KEY` is set in `.env` (not using `os.urandom()`)

**"Invalid request" on logout:**
- Verify `http://localhost:5000/` is in Cognito's "Allowed sign-out URLs"
- Ensure you're accessing via `localhost`, not `127.0.0.1`
