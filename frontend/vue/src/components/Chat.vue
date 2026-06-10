<template>
  <section class="h-full p-2 sm:p-4 text-text-main flex flex-col">
    <textarea
      class="w-full p-4 resize-none flex-1" 
      id="chat-log" 
      v-model="chatLog"
      disabled
    />
    <div class="flex-center h-8 w-full gap-3 flex-none">
      <input class="border border-text-main rounded-full py-2 px-4 w-full"
        id="chat-message-input"
        v-model="messageInput"
        @keyup.enter="sendMessage"
        placeholder="Type a meowssage..."
      />
      <div class="w-28">
        <Button id="chat-message-submit" @click="sendMessage">Send</Button>
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
      this.chatSocket.onclose = null;
      this.chatSocket.onerror = null;
      this.chatSocket.onmessage = null;
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

</style>
