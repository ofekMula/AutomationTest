      const chatForm = document.getElementById('chat-form');
      const chatMessages = document.querySelector('.chat-messages')
      const socket = io("http://localhost:8080");

      socket.on('message',message=> {
          console.log(message);
          sendMsg(message);
//          document.getElementById('chat-messages').scrollTop = 0;
          document.querySelector('.chat-messages').scrollTop = 0;


      });

      function sendMsg(message) {
        const div = document.createElement('div');
        div.classList.add('container');
          div.innerHTML += `<p>${message}</p>`;
          document.querySelector('.chat-messages').appendChild(div);


      }

      // send message to chat
      if(chatForm){
          chatForm.addEventListener('submit',(e)=>{
            e.preventDefault();
            //get message text
            const msg = e.target.elements.msg.value;
            //emitting message to the server
            socket.emit('clientChatMessage',msg);
            e.target.elements.msg.value = ' ';
            e.target.elements.msg.focus();
          });
      }
