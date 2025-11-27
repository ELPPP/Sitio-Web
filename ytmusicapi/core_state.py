# core_state.py
class HeaderState:
    _instance = None

    def __init__(self):
        self._nonce = None
        self.New_nonce = None
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
        self.headers = None
        self._timestamp = time.time()
        self.status = "init"