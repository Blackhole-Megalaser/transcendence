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
        this.handleSocketMessage(e);
      };

      this.chatSocket.onclose = (e) => {
        console.log('Chat socket closed');
      };
    },
    handleSocketMessage(e) {
      const data = JSON.parse(e.data);

      if (data.type === 'history' && Array.isArray(data.messages)) {
        this.chatLog = data.messages
          .map((message) => this.formatMessage(message))
          .filter(Boolean)
          .join('\n');

        if (this.chatLog) {
          this.chatLog += '\n';
        }

        this.$nextTick(this.scrollText);
        return;
      }

      if (data.type === 'message') {
        this.appendMessage(data.message);
        return;
      }

      if (data.message) {
        this.appendMessage(data.message);
      }
    },
    sendMessage() {
      const message = this.messageInput.trim();

      if (!message || !this.chatSocket || this.chatSocket.readyState !== WebSocket.OPEN) {
        return;
      }

      this.chatSocket.send(JSON.stringify({
        message
      }));
      this.messageInput = '';
    },
    appendMessage(message) {
      const formattedMessage = this.formatMessage(message);

      if (!formattedMessage) {
        return;
      }

      this.chatLog += formattedMessage + '\n';
      this.$nextTick(this.scrollText);
    },
	  formatMessage(message) {
        if (typeof message === 'string') {
          return message;
        }

        if (!message) {
          return '';
        }

        const author = message.author || 'anonymous';
        const text = message.text || message.message || '';

        return text ? `${author}: ${text}` : '';
	  },
	  scrollText() {
	      const textarea = document.getElementById('chat-log');

          if (!textarea) {
            return;
          }

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
