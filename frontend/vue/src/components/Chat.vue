<template>
  <section class="h-full bg-bg-main p-2 sm:p-4 text-text-main">
    <div>
    <textarea class="chatbox" id="chat-log" v-model="chatLog" readonly></textarea>
   <center>
	  <input class="inputbox"
        id="chat-message-input"
        v-model="messageInput"
        @keyup.enter="sendMessage"
        placeholder="Type a meowssage..."
       />
      <Button class="sendbox" id="chat-message-submit" @click="sendMessage">Send</Button>
	</center>
  </div>
  </section>
</template>

<script setup>

import Button from '@components/Button.vue';

</script>

<script>

export default {
  props: {
    initialRoomName: {
      type: String,
      default: 'room'
    }
  },
  data() {
    return {
      roomName: this.initialRoomName,
      chatSocket: null,
      chatLog: '',
      messageInput: ''
    };
  },

  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.chatSocket) {
      this.chatSocket.close();
    }
  },
  methods: {
    connectWebSocket() {
	  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	  const host = window.location.host;
	
      const wsUrl = `${protocol}//${host}/ws/chat/${this.roomName}/`;
      this.chatSocket = new WebSocket(wsUrl);

	  console.log('Chat socket connected to ' + this.roomName);
      this.chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        this.chatLog += data.message + '\n';
      };

      this.chatSocket.onclose = (e) => {
        console.log('Chat socket closed');
      };
    },
    sendMessage() {
      if (this.messageInput.trim()) {
        this.chatSocket.send(JSON.stringify({
          message: this.messageInput
        }));
		this.scrollText();
        this.messageInput = '';
      }
    },
	scrollText() {
	    var textarea = document.getElementById('chat-log');
	    textarea.value += document.getElementById('chat-message-submit').value + "\n";            
	    textarea.scrollTop = textarea.scrollHeight;
	}
  }
};
</script>

<style scoped>
@import "@/style.css";

textarea {
	display: block;
	cursor: text;
	height: auto;
	min-width: 30em;
    max-width: 100%;
    min-height: 10em;
	overflow: auto;
}

.chatbox {
	height:100%;
	width:100%;
	border: 4mm ridge rgb(211 220 50 / 0.6);
	margin-top:5%;
	padding:0.4%;
}

.inputbox {
	border: solid white;
	margin-top:1%;
	margin-bottom:1%;
	padding:0.4%;
}

.sendbox {
	width:15%;
	margin-left:5%;
}

.fscreen {
  @apply h-[calc(100dvh-5rem)] w-dvw
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  @apply bg-bg-main pt-20
}

</style>
