import eventlet
import socketio
from entities.client import Client
from entities.message import Message

# CONSTANTS
DEFAULT_NICKNAME = 'new_client'
SERVER_URL = 'localhost'
PORT_NUM = 8080
SERVER_NAME = 'Admin'
DEFAULT_SELECTED_USER = 'default'

# allow server to track all connected clients
connected_clients = dict()

# init socketio and avoid  cors
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    connected_clients[sid] = Client(sid, DEFAULT_NICKNAME)
    print(sid, 'connected')

# for updating nickname of connected client - used after connection
@sio.on('nickname')
def update_nickname(sid,nickname):
    connected_clients[sid].set_nickname(nickname)
    welcome_msg = Message(SERVER_NAME,nickname+ ' joined chat')
    sio.emit('message', (welcome_msg.get_sender(),welcome_msg.get_msg_content(),welcome_msg.get_msg_time()))
    sio.emit('add_user', list(client.get_client_nickname() for client in connected_clients.values()))



@sio.on('clientChatMessage')
def chat_message(sid, msg,selected_user):
    print(sid,'sent message:',msg)
    user = connected_clients[sid]
    msg_chat = Message(user.get_client_nickname(),msg)
    if selected_user == DEFAULT_SELECTED_USER:
        sio.emit('message',(msg_chat.get_sender(),msg_chat.get_msg_content(),msg_chat.get_msg_time()))
    else:
        reciever_client = find_client_by_nickname(selected_user)
        if reciever_client is not None:
            msg_chat.make_msg_private()
            sio.emit('message', (msg_chat.get_sender(), msg_chat.get_msg_content(), msg_chat.get_msg_time()),
                     room=reciever_client.get_client_sid())
            #for displaying the message to the sender
            sio.emit('message', (msg_chat.get_sender(), msg_chat.get_msg_content(), msg_chat.get_msg_time()),
                     room=sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    nickname = connected_clients[sid].get_client_nickname()
    leave_msg = Message(SERVER_NAME,nickname+ ' left chat')
    connected_clients.pop(sid)
    sio.emit('message', (leave_msg.get_sender(),leave_msg.get_msg_content(),leave_msg.get_msg_time()))
    sio.emit('delete_user', nickname)

#helper function
def find_client_by_nickname(nickname):
    for client in connected_clients.values():
        if client.get_client_nickname() == nickname:
            return client
    return None

if __name__ == '__main__':
    # run the server
    eventlet.wsgi.server(eventlet.listen((SERVER_URL, PORT_NUM)), app)

