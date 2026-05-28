<template>
  <br>
  <center>
    <h2 >Work in progress</h2>
    <br>
    <div>
    <textarea id="chat-log" v-model="chatLog" readonly></textarea>
	<br>
    <input
      id="chat-message-input"
      v-model="messageInput"
      @keyup.enter="sendMessage"
      placeholder="Type a message..."
    />
	<br>
    <Button id="chat-message-submit" @click="sendMessage">Send</Button>
  </div>
  </center>
</template>

<script setup>

import Button from '@components/Button.vue';

</script>

<script>

export default {
  data() {
    return {
      roomName: 'room',
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

      this.chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        this.chatLog += data.message + '\n';
      };

      this.chatSocket.onclose = (e) => {
        console.error('Chat socket closed unexpectedly');
      };
    },
    sendMessage() {
      if (this.messageInput.trim()) {
        this.chatSocket.send(JSON.stringify({
          message: this.messageInput
        }));
        this.messageInput = '';
      }
    }
  }
};
</script>

<style scoped>
@import "@/style.css";

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
