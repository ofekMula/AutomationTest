      //defining constants
      const chatForm = document.getElementById('chat-form');
      const chatMessages = document.querySelector('.chat-messages')
      var users_list =["all users"];

      // get client nickname
      const client_nickname = window.location.search.split('=')[1];

      //connecting to server
      const socket = io("http://localhost:8080");
      socket.emit('nickname',client_nickname);

      //events handling:

      if(chatForm){
          chatForm.addEventListener('submit',(e)=>{
            e.preventDefault();
            //get message text
            const msg = e.target.elements.msg.value;
            var selected_user = document.getElementById("users").value;
            //emitting message to the server
            socket.emit('clientChatMessage',msg,selected_user);
            e.target.elements.msg.value = ' ';
            e.target.elements.msg.focus();
          });
      }

      socket.on('message',(sender_nickname,content,time)=> {
          const msg = formatMessage(time,sender_nickname,content)
          sendMsg(msg);
          chatMessages.scrollTop = chatMessages.scrollHeight;
      });

      socket.on('add_user',(array)=> {
          var x = document.getElementById("users");
          for ( var i =0;i<array.length;i++){
            var option_obj = document.getElementById(array[i]);
            if(option_obj ==null){
                var option = document.createElement("option");
                option.id = array[i];
                option.text = array[i];
                x.add(option);
            }
          }
      });

      socket.on('delete_user',(user_nickname)=> {
        var selectobject = document.getElementById("users");
        for (var i=0; i<selectobject.length; i++) {
            if (selectobject.options[i].value == user_nickname){
                selectobject.remove(i);
            }
        }
      });

      //helper functions

      function formatMessage(time,nickname,content){
        return (time + '  ' + nickname +': ' + content);
      }

      function sendMsg(message) {
        const div = document.createElement('div');
        div.classList.add('container');
         div.innerHTML += `<p>${message}</p>`;
         document.querySelector('.chat-messages').appendChild(div);
      }


