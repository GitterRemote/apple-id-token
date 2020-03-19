# -*- coding: utf-8 -*-
import base64
import collections
import requests
import rsa


class KeysManager(object):

    _url = "https://appleid.apple.com/auth/keys"

    def __init__(self, raw_keys=None):
        self._keys = self._parse_keys(raw_keys)

    @property
    def keys(self):
        return self._keys

    _Key = collections.namedtuple("_Key", ["public_key", "algorithm"])

    def _parse_key(self, raw_key):
        assert "n" in raw_key and "e" in raw_key
        n = int(base64.urlsafe_b64decode(
            raw_key["n"].encode("ascii") + b"==").hex(), 16)
        e = int(base64.urlsafe_b64decode(
            raw_key["e"].encode("ascii") + b"==").hex(), 16)
        public_key = rsa.PublicKey(n=n, e=e)
        return self._Key(public_key.save_pkcs1(), raw_key.get("alg"))

    def _parse_keys(self, raw_keys):
        if not raw_keys:
            return {}
        return {
            raw_key.get("kid"): self._parse_key(raw_key)
            for raw_key in raw_keys
        }

    def _load_keys_from_apple(self):
        """
        Examples:
            {
                "kty": "RSA",
                "kid": "86D88Kf",
                "use": "sig",
                "alg": "RS256",
                "n": "iGaLqP6y-SJCCBq5Hv6pGDbG_SQ11MNjH7rWHcCFYz4hGwHC4lcSurTlV8u3avoVNM8jXevG1Iu1SY11qInqUvjJur--hghr1b56OPJu6H1iKulSxGjEIyDP6c5BdE1uwprYyr4IO9th8fOwCPygjLFrh44XEGbDIFeImwvBAGOhmMB2AD1n1KviyNsH0bEB7phQtiLk-ILjv1bORSRl8AK677-1T8isGfHKXGZ_ZGtStDe7Lu0Ihp8zoUt59kx2o9uWpROkzF56ypresiIl4WprClRCjz8x6cPZXU2qNWhu71TQvUFwvIvbkE1oYaJMb0jcOTmBRZA2QuYw-zHLwQ",  # nopep8
                "e": "AQAB"
            }
        """
        resp = None
        try:
            resp = requests.get(self._url)
            resp.raise_for_status()
            data = resp.json()
            keys = data.get("keys")
            assert isinstance(keys, list)
        except Exception as e:
            if resp:
                status_code = resp.status_code
                data = resp.text
            else:
                status_code = None
                data = None
            raise Exception("AppleIDServer Error", e, status_code, data)
        else:
            return keys

    def _refresh_keys(self):
        self._keys = self._parse_keys(self._load_keys_from_apple())

    def get_signing_key(self, kid):
        if kid not in self._keys:
            self._refresh_keys()
        return self._keys.get(kid)


_instance = None


def get():
    global _instance
    if not _instance:
        _instance = KeysManager()
    return _instance
