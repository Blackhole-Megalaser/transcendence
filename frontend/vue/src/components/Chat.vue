<template>
  <section class="h-full p-2 sm:p-4 text-text-main">
    <div>
      <textarea 
        class="chatbox" 
        id="chat-log" 
        v-model="chatLog" 
        disabled
      />
      <div class="flex-center w-full">
        <input class="inputbox"
          id="chat-message-input"
          v-model="messageInput"
          @keyup.enter="sendMessage"
          placeholder="Type a meowssage..."
        />
        <Button class="sendbox" id="chat-message-submit" @click="sendMessage">Send</Button>
	    </div>
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
</style>
