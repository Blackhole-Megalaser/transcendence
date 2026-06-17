<template>
  <section class="h-full text-text-main flex flex-col">
    <ul class="w-full px-4 pt-4 pb-2 flex-1 overflow-auto" id="chat-log">
      <li
        class="w-full flex gap-4"
        :class="message.showAuthorInfos ? 'pt-2' : ''"
        :key="index"
        v-for="( message, index ) in chatLog"
      >
        <div class="min-w-12">
          <img 
            :src="message.profile_pic ? message.profile_pic : defaultcat"
            alt="Pfp"
            class="size-12 rounded-full overload-hidden"
            v-if="message.showAuthorInfos"
            >
        </div>
        <div>
          <h3 
            class="text-lg font-semibold"
            v-if="message.showAuthorInfos"
          >{{ message.author }}
          <span class="inline-block font-normal text-xs opacity-60">
            {{ message.formatedDate }}
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
        <Button id="chat-message-submit" @click="sendMessage"
          :disabled="!isConnected"
        >Send</Button>
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
      lastMessageInfos: '',
      isConnecting: false,
      isConnected: false,
      baseDelay: 300,     // divided by 10 to stay with int
      currentDelay: 3000,
      jitter: 0.05,
      jitterValue: 0,
      connectionAttempt: -1,
      intervalId: 0,
    };
  },
  mounted() {
    // connect on start and monitor the ws state
    this.connectWebSocket();
    this.intervalId = setInterval(this.refreshDelay, this.currentDelay);
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
    if (this.chatSocket) {
      this.chatSocket.close();
    }
  },
  methods: {
    refreshDelay() {
      // console.log(this.currentDelay);
      if (!this.isConnected && !this.isConnecting) {
        this.connectWebSocket();
        clearInterval(this.intervalId);

        // Add ± jitter % of current value to prevent mass reconnecting
        this.currentDelay = this.baseDelay * (10 + (this.connectionAttempt));
        this.jitterValue  = Math.floor(this.currentDelay * (Math.random() * 2 - 1) * this.jitter);

        // console.log("curDelay =", this.currentDelay);
        // console.log("jitValue =", this.jitterValue);
        this.currentDelay = this.currentDelay + this.jitterValue;

        // console.log("Total Delay ="this.currentDelay);
        this.intervalId = setInterval(this.refreshDelay, this.currentDelay);
      }
      else if (this.isConnected) {
        // delay is auto reset on next attempt
        this.connectionAttempt  = -1;
      }
    },
    connectWebSocket() {
      if (this.chatSocket?.readyState == WebSocket.OPEN) {
        this.isConnecting       = false;
        this.isConnected        = true;
        this.connectionAttempt  = -1;
        return
      }

    this.isConnected = false;
    this.connectionAttempt++;
    console.log("Attempting to connect to chat...");

	  const protocol      = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	  const host          = window.location.host;
	
      const wsUrl       = `${protocol}//${host}/ws/chat/${this.roomName}/`;
      this.chatSocket   = new WebSocket(wsUrl);
      this.isConnecting = true;

      this.chatSocket.onopen = (e) => {
        this.isConnecting = false;
        this.isConnected = true;
        console.log('Chat socket connected to ' + this.roomName);
      }

      this.chatSocket.onerror = (e) => {
        this.isConnecting = false;
        this.isConnected = false;
        console.log("Failed to reach server: Retrying in", this.currentDelay, "ms");
      }

      this.chatSocket.onmessage = (e) => {
        this.handleSocketMessage(e);
      };

      this.chatSocket.onclose = (e) => {
        this.isConnecting = false;
        this.isConnected = false;
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
      const text            = message.text || message.message || '';
      const author          = message.author || 'anonymous';
      const profile_pic     = message.picture;
      const date            = new Date(message.created_at);
      const formatedDate    = date.toLocaleDateString('fr-FR', { hour: '2-digit', minute: '2-digit'}).split(" ")[1];
      const isSameAuthor    = author === this.lastMessageInfos.Author;
      const timestamp       = date.getTime();
      const isWithinMinutes = (timestamp - this.lastMessageInfos.Timestamp) < 5 * 60 * 1000;
      const showAuthorInfos = !isSameAuthor || !isWithinMinutes;
      const isConnected     = this.isConnected;
      this.lastMessageInfos = { Author: author, Timestamp: timestamp };
      return { author, formatedDate, text, showAuthorInfos, profile_pic, isConnected};
	  },
	  scrollText() {
	      const div = document.getElementById('chat-log');
	      div.scrollTop = div.scrollHeight;
	  }
  },
};
</script>
