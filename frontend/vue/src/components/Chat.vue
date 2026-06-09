<template>
  <section class="h-[calc(100vh-160px)] p-2 sm:p-4 text-text-main flex flex-col">
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

</style>
