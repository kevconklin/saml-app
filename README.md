## Next steps: 

Add a settings.json with Azure Entra ID configs/cert info.

Example: 

```json
{
  "strict": true,
  "debug": true,
  "sp": {
    "entityId": "http://localhost:8000/metadata/",
    "assertionConsumerService": {
      "url": "http://localhost:8000/sso/acs/",
      "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    },
    "singleLogoutService": {
      "url": "http://localhost:8000/sso/sls/",
      "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    },
    "x509cert": "MIID...",
    "privateKey": "-----BEGIN PRIVATE KEY-----..."
  },
  "idp": {
    "entityId": "https://idp.example.com/metadata",
    "singleSignOnService": {
      "url": "https://idp.example.com/sso",
      "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    },
    "singleLogoutService": {
      "url": "https://idp.example.com/slo",
      "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    },
    "x509cert": "MIID..."
  }
}
```

## Create necessary certs

```mkdir -p backend/certs
cd backend/certs

openssl req -newkey rsa:2048 -nodes -keyout sp.key -x509 -days 365 -out sp.crt
```

These can go here in the settings.json: 
```json
"sp": {
  ...
  "x509cert": "<paste contents of sp.crt, one line, no headers>",
  "privateKey": "<paste contents of sp.key, one line, no headers>"
}
```

May need this command to get it into one line: 

```
awk 'NF {sub(/\\n/, \"\"); printf \"%s\\\\n\", $0;}' sp.crt
```


## Manage Azure AD

Set up Azure Entra ID subscription. 

### Configure SAML-Based Sign-On
In your app’s Overview screen, go to Single sign-on → Select SAML. In the Basic SAML Configuration section:

Click *Edit*

Set the following:
- Identifier (Entity ID) -->	http://localhost:8000/metadata/
- Reply URL (ACS)	--> http://localhost:8000/sso/acs/
- Sign on URL	--> Leave blank
- Relay State	--> Leave blank

Click Save

### Download IdP Metadata and Cert
Scroll down to the SAML Signing Certificate section

Download:
- Federation Metadata XML
- Certificate (Base64)

### Update Your settings.json
Extract these values from the metadata XML or Azure UI:

```json
"idp": {
  "entityId": "https://sts.windows.net/<tenant-id>/",
  "singleSignOnService": {
    "url": "https://login.microsoftonline.com/<tenant-id>/saml2",
    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
  },
  "singleLogoutService": {
    "url": "https://login.microsoftonline.com/<tenant-id>/logout",
    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
  },
  "x509cert": "<paste Azure cert here without BEGIN/END lines>"
}
```
To format the cert correctly:

```bash
awk 'NF {sub(/\\n/, ""); printf "%s\\n", $0;}' azure_cert.crt
```
Paste that value into settings.json.
