<template>
  <br>
  <center>
    <h2 >Work in progress</h2>
    <br>
    <div>
    <textarea id="chat-log" v-model="chatLog" readonly></textarea>
    <input
      id="chat-message-input"
      v-model="messageInput"
      @keyup.enter="sendMessage"
      placeholder="Type a message..."
    />
    <Button id="chat-message-submit" @click="sendMessage">Send</Button>
  </div>
  </center>
</template>

<!-- <script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';

import Button from '@components/Button.vue';
// // import { runChat } from './chat.js';

const log     = ref(null)
const input   = ref(null)
const submit  = ref(null)
// // runChat();

const observer = new IntersectionObserver((entries, observer) => {
  console.log(entries)
});

const roomName = 'chat';

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    log.value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

input.focus();
input.onkeyup = function(e) {
    if (e.key === 'Enter') {
        submit.click();
    }
};

submit.onclick = function(e) {
    // const messageInputDom = document.querySelector('#chat-message-input');
    const messageInputDom = input;
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};

onMounted(() => {
  window.addEventListener("keydown", handleKeyPress);
  const input = document.querySelector("#chat-message-input");
  const submit = document.querySelector('#chat-message-submit');
  const log = document.querySelector('#chat-log');
  observer.observe(input);
  observer.observe(submit);
  observer.observe(log);
})
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyPress);
  observer.disconnect();
})

</script> -->

<style scoped>
@import '../../style.css';

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


<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';

import Button from '@components/Button.vue';

export default {
  data() {
    return {
      roomName: 'chat',
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
      const wsUrl = `ws://${window.location.host}/ws/chat/${this.roomName}/`;
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
