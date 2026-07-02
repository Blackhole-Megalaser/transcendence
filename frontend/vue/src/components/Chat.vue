<template>
  <section class="h-full text-text-main flex flex-col">
    <ul
      v-if="compact"
      class="w-full flex-1 overflow-auto px-2 py-2 space-y-1 text-sm"
      id="chat-log"
    >
      <li
        class="w-full min-w-0 rounded-md px-2 py-1 leading-snug"
        :class="message.system ? systemMessageClass(message) : 'bg-transparent'"
        :key="index"
        v-for="( message, index ) in chatLog"
      >
        <span class="font-black" :class="message.system ? '' : 'text-title'">{{ message.author }}</span>
        <span class="opacity-50 text-xs ml-1">{{ message.formatedDate }}</span>
        <span class="mx-1 opacity-50">:</span>
        <span class="break-words">{{ message.text }}</span>
      </li>
    </ul>
    <ul
      v-else
      class="w-full flex-1 overflow-auto px-4 pt-2 md:pt-4 pb-2"
      id="chat-log"
    >
      <li
        class="w-full flex gap-4"
        :class="message.showAuthorInfos ? 'pt-2' : ''"
        :key="index"
        v-for="( message, index ) in chatLog"
      >
        <div 
          class="group relative min-w-12 rounded-full overflow-hidden cursor-pointer"
          :class="message.showAuthorInfos ? 'h-12' : ''" 
          >
          <div 
            class="absolute inset-0 size-12 bg-cover bg-center"
            :style="{ backgroundImage: `url(${message.profile_pic ?? defaultcat})` }"
            v-if="message.showAuthorInfos"
          />
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
    <div class="flex-center h-auto w-full gap-2 flex-none border-t border-text-main" :class="compact ? 'px-2 py-1.5' : 'px-4 py-2 gap-3'">
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
import { nextTick } from 'vue';
</script>

<script>
export default {
  props: {
    initialRoomName: {
      type: String,
      default: 'room'
    },
    initialHistoryFetch: {
      type: Boolean,
      default: true
    },
    initialModuleName: {
      type: String,
      default: 'chat'
    },
    compact: {
      type: Boolean,
      default: false
    },
    messageInterceptor: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      roomName: this.initialRoomName,
      moduleName: this.initialModuleName,
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
      receiveHistory: this.initialHistoryFetch,
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
	
      const wsUrl       = `${protocol}//${host}/ws/${this.moduleName}/${this.roomName}/`;
      this.chatSocket   = new WebSocket(wsUrl);
      this.isConnecting = true;

      this.chatSocket.onopen = (e) => {
        this.isConnecting = false;
        this.isConnected = true;
        console.log('Chat socket connected to', this.roomName);
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

      if (data.type === 'history' && Array.isArray(data.messages) && this.receiveHistory) {
        this.chatLog = [];
		this.chatLog.push(...data.messages
          .map((message) => this.formatMessage(message))
          .filter(Boolean));

        this.$nextTick(this.scrollText);
        this.receiveHistory = false;
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
    async sendMessage() {
      const message = this.messageInput.trim();

      if (!message || !this.chatSocket || this.chatSocket.readyState !== WebSocket.OPEN) {
         return;
      }

      let shouldSend = true;
      if (this.messageInterceptor) {
        shouldSend = await this.messageInterceptor(message) !== false;
      } else {
        this.$emit('input_message', message);
      }

      if (shouldSend) {
        this.chatSocket.send(JSON.stringify({
          message
        }));
      }
      this.messageInput = '';
      this.$nextTick(this.focusOnInput);
    },
    appendMessage(message) {
      const formattedMessage = this.formatMessage(message);

      if (!formattedMessage) {
        return;
      }

      this.chatLog.push(formattedMessage);
      this.$nextTick(this.scrollText);
    },
    systemMessageClass(message) {
      if (message.tone === 'success') return 'bg-green-100 text-green-700 font-bold';
      if (message.tone === 'error') return 'bg-red-100 text-red-700 font-bold';
      return 'bg-title/10 text-text-main font-bold';
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
      const system          = Boolean(message.system || message.type === 'system');
      const tone            = message.tone || (system ? 'info' : null);
      this.lastMessageInfos = { Author: author, Timestamp: timestamp };
      return { author, formatedDate, text, showAuthorInfos, profile_pic, isConnected, system, tone};
	  },
	  scrollText() {
	    const div = document.getElementById('chat-log');
	    div.scrollTop = div.scrollHeight;
	  },
    focusOnInput() {
      const input = document.getElementById('chat-message-input');
      input.focus();
    }
  },
};
</script>
