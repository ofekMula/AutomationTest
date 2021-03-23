import datetime


class Message:
    def __init__(self,sender_nickname, content):
        # self._sender_id = sender_id
        self._sender_nickname = sender_nickname
        #self._receiver_id = receiver_id
        self._content = content
        self._time = str(datetime.datetime.now().hour) + ':' +(datetime.datetime.now().minute.real.__str__())

    def get_sender(self):
        return self._sender_nickname

    def get_msg_time(self):
        return self._time

    def get_msg_content(self):
        return self._content

    def make_msg_private(self):
       self._content += ' (private)'

