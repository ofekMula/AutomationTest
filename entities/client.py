class Client:
    '''
    Client object : holds information of client who connected to server:
    - session id
    - nickname
    '''

    def __init__(self, session_id, nickname):
        self._session_id = session_id
        self._nickname = nickname

    def get_client_sid(self):
        return self._session_id

    def get_client_nickname(self):
        return self._nickname

    def set_nickname(self, nickname):
        self._nickname = nickname


