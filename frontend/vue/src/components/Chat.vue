<template>
  <section class="h-full text-text-main flex flex-col">
    <ul class="w-full px-4 pt-4 flex-1 overflow-auto" id="chat-log">
      <li
        class="w-full flex gap-4"
        :class="!message.isSameAuthor ? 'pt-2' : ''"
        :key="index"
        v-for="( message, index ) in chatLog"
      >
        <div class="w-12"><!-- INCOMING PROFILE PICTURE -->
          <img 
            :src="defaultcat" 
            alt="Pfp"
            class="size-12 rounded-full overload-hidden"
            v-if="!message.isSameAuthor"
          >
        </div>
        <div>
          <h3 
            class="text-lg font-semibold" 
            v-if="!message.isSameAuthor"
          >{{ message.author }}
            <span class="text-sm opacity-60">
              {{ message.date }}
            </span>
          </h3>
          <p>{{ message.text }}</p>
        </div>
      </li>
    </ul>
    <div class="flex-center h-auto w-full p-4 gap-3 flex-none border-t border-text-main">
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
import Button     from '@components/Button.vue';
import defaultcat from '@assets/default_cat.png';
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
      chatLog: [],
      messageInput: '',
      lastMessageAuthor: ''
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
        this.chatLog.push(...data.messages
          .map((message) => this.formatMessage(message))
          .filter(Boolean));

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

      this.chatLog.push(formattedMessage);
      this.$nextTick(this.scrollText);
    },
	  formatMessage(message) {
      const author  = message.author || 'anonymous';
      const isSameAuthor = author === this.lastMessageAuthor
      this.lastMessageAuthor = author
      const text    = message.text || message.message || '';
      const date    = message.created_at;
      return { author, date, text, isSameAuthor };
	  },
	  scrollText() {
	      const div = document.getElementById('chat-log');
	      div.scrollTop = div.scrollHeight;
	  }
  }
};
</script>
