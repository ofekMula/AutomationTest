import eventlet
import socketio
from entities.client import Client
from entities.message import Message

DEFAULT_NICKNAME = 'new_client'
SERVER_URL = 'localhost'
PORT_NUM = 8080
SERVER_NAME = 'Admin'
DEFAULT_SELECTED_USER = 'default'
# tracking on all the connected clients to the server
connected_clients = dict()

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    connected_clients[sid] = Client(sid, DEFAULT_NICKNAME)
    print(sid, 'connected')


@sio.on('nickname')
def update_nickname(sid,nickname):
    connected_clients[sid].set_nickname(nickname)
    welcome_msg = Message(SERVER_NAME,nickname+ ' joined chat')
    sio.emit('message', (welcome_msg.get_sender(),welcome_msg.get_msg_content(),welcome_msg.get_msg_time()))
    sio.emit('add_user', list(client.get_client_nickname() for client in connected_clients.values()))
    print(nickname)


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


def find_client_by_nickname(nickname):
    for client in connected_clients.values():
        if client.get_client_nickname() == nickname:
            return client
    return None
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((SERVER_URL, PORT_NUM)), app)

#
# from aiohttp import web
# import socketio
#
# ## creates a new Async Socket IO Server
# sio = socketio.AsyncServer(cors_allowed_origins='*')
# ## Creates a new Aiohttp Web Application
# app = web.Application()
# # Binds our Socket.IO server to our Web App
# ## instance
# sio.attach(app)
#
# ## we can define aiohttp endpoints just as we normally
# ## would with no change
# async def index(request):
#     with open('index.html') as f:
#         return web.Response(text=f.read(), content_type='text/html')
#
# ## If we wanted to create a new websocket endpoint,
# ## use this decorator, passing in the name of the
# ## event we wish to listen out for
# @sio.on('message')
# async def print_message(sid, message):
#     ## When we receive a new event of type
#     ## 'message' through a socket.io connection
#     ## we print the socket ID and the message
#     print("Socket ID: " , sid)
#     print(message)
#
# ## We bind our aiohttp endpoint to our app
# ## router
# app.router.add_get('/', index)
#
# ## We kick off our server
# if __name__ == '__main__':
#     web.run_app(app)