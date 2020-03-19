# -*- coding: utf-8 -*-
import jwt
from . import keys_manager as _keys_manager


class AuthFailedError(Exception):

    def __init__(self, *args, jwt_err=None, **kwargs):
        self.jwt_err = jwt_err
        super(AuthFailedError, self).__init__(*args, **kwargs)


class AudienceAuth(object):

    def __init__(self, audience=None, verify_aud=True, issuer=None,
                 verify_iss=True, jwt_options=None, keys_manager=None):
        self.audience = audience
        self.issuer = issuer or "https://appleid.apple.com"
        jwt_options = jwt_options or {}
        jwt_options.setdefault("verify_aud", verify_aud)
        jwt_options.setdefault("verify_iss", verify_iss)
        self.jwt_options = jwt_options
        self._keys_manager = keys_manager or _keys_manager.get()

    def verify_identity_token(self, encoded_identity_token, **kwargs):
        header = jwt.get_unverified_header(encoded_identity_token)
        key = self._keys_manager.get_signing_key(header.get("kid"))
        if not key:
            raise AuthFailedError(
                "kid does not match any public key",
                self._keys_management.keys
            )
        algorithm = header.get("alg", key.algorithm)

        params = dict(
            key=key.public_key,
            algorithms=[algorithm],
            audience=self.audience,
            issuer=self.issuer,
            options=self.jwt_options,
        )

        params.update(kwargs)

        try:
            decoded = jwt.decode(encoded_identity_token, **params)
        except jwt.InvalidSignatureError as e:
            raise AuthFailedError(algorithm, key, jwt_err=e)
        except jwt.InvalidAlgorithmError as e:
            raise AuthFailedError(algorithm, key, jwt_err=e)
        except jwt.PyJWTError as e:
            raise AuthFailedError(jwt_err=e)

        return decoded


auth = AudienceAuth()
