from onelogin.saml2.auth import OneLogin_Saml2_Auth
from fastapi import Request

def prepare_request(request: Request, form_data: dict):
    return {
        "https": "off",  # or "on" if you're using HTTPS
        "http_host": "localhost",
        "server_port": "8000",
        "script_name": request.url.path,
        "get_data": dict(request.query_params),
        "post_data": form_data
    }

def init_saml_auth(request: Request, form_data: dict):
    req_data = prepare_request(request, form_data)
    return OneLogin_Saml2_Auth(req_data, custom_base_path="backend")
