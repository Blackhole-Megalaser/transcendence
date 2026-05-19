<template>
	<div id="app">
		<h2>Work in progress</h2>
		<Button
			v-on:click="sendMessage('hello')"
			>
			> Send <
		</button>
	</div>
</template>

<script>

import Button from '../../components/Button.vue';

export default {
	name: 'App',
    data: function() {
      return {
		connection: null
	  }
    },
	methods: {
		sendMessage: function(message) {
			console.log("UwU")
			console.log(this.connection);
			this.connection.send(message);
		}
	},
	created: function() {
		console.log("Init connection to WebSocket")
		this.connection = new WebSocket("wss://echo.websocket.org")

		this.connection.onopen = function(event) {
			console.log(event)
			console.log("Success")
		}

		this.connection.onmessage = function(event) {
			console.log(event);
		}

	},
	components: {
		Button: Button,
	}
}

</script>

<style>
@import '../../style.css';


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