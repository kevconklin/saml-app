from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from saml import init_saml_auth
import requests, json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your-very-secret-key"

def create_jwt(user_id: str):
    return jwt.encode({"sub": user_id}, SECRET_KEY, algorithm="HS256")

def validate_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/sso/login")
async def login(request: Request):
    auth = init_saml_auth(request, {})
    return RedirectResponse(auth.login())

@app.post("/sso/acs/")
async def acs(request: Request):
    form = await request.form()
    auth = init_saml_auth(request, dict(form))
    auth.process_response()
    
    if auth.get_errors():
        return HTMLResponse(f"Errors: {auth.get_errors()}<br><br>Reason: {auth.get_last_error_reason()}", status_code=400)
    
    user_id = auth.get_nameid()
    token = create_jwt(user_id)
    return RedirectResponse(
        url=f"http://localhost:3000/api/auth/set-cookie?token={token}",
        status_code=302  # or 303
    )


@app.get("/metadata/")
def metadata():
    from onelogin.saml2.settings import OneLogin_Saml2_Settings
    settings = OneLogin_Saml2_Settings(custom_base_path="backend", sp_validation_only=True)
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if errors:
        return HTMLResponse(str(errors), status_code=500)
    return HTMLResponse(metadata, media_type="text/xml")

@app.get("/protected")
def protected(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user = validate_token(token)
    return {"message": "Welcome", "user": user, "token": token}