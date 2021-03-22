import eventlet
import socketio
from entities.client import Client

DEFAULT_NICKNAME = 'new_client'
SERVER_URL = "localhost"
PORT_NUM = 8080

# tracking on all the connected clients to the server
connected_clients = dict()

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    connected_clients[sid] = Client(sid, DEFAULT_NICKNAME)
    print(sid ,'connected')
    sio.emit('message', 'A user has joined to the chat')




@sio.on('clientChatMessage')
def chat_message(sid, msg):
    print(sid,'sent message:',msg)
    sio.emit('message',msg)




@sio.event
def message(sid, data):
    print('Socket ID: ', sid, 'message: ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


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