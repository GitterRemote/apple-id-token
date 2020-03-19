# apple-id-token
Verify Apple ID token (JWT) from server in Python

## Usage
```python
import apple_id_token

decoded = apple_id_token.verify_identity_token(identity_token, verify_aud=False)

decoded = apple_id_token.verify_identity_token(identity_token, audience="xxx")
```

