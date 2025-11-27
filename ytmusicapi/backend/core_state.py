# core_state.py
import time

class HeaderState:
    _instance = None

    def __init__(self):
        self._nonce = None
        self._headers = None
        self._timestamp = None
        self.status = "init"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = HeaderState()
        return cls._instance

    def reset(self):
        """Reinicia el estado a valores iniciales."""
        self._nonce = None
        self._headers = None
        self._timestamp = time.time()
        self.status = "init"

    # -----------------------
    # Getters / Setters reales
    # -----------------------

    def get_headers(self):
        return self._headers

    def set_headers(self, headers: dict):
        self._headers = headers
        self._timestamp = time.time()
        self.status = "ready"

    def headers_ready(self):
        return self._headers is not None
