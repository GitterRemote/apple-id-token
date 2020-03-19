from . import audience_auth as _audience_auth


verify_identity_token = _audience_auth.auth.verify_identity_token
AuthFailedError = _audience_auth.AuthFailedError
