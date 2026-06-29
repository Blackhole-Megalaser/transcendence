<script setup>
    import { ref, onMounted, onUnmounted } from 'vue';

    const roomCode = ref('VWXYZ');
    const roomName = ref('Amigos');
    const username = ref('Anas');


</script>

<template>
    <div class="flex justify-center h-full w-full">
        <div class="flex flex-col
            bg-navbar border-solid border-8 border-navbar
            gap-4 w-2xl h-9/10">
            <div class="flex justify-center
                gap-4 w-full">
                <h1 class="text-navbar-menu font-bold">GAME RULES</h1>
            </div>
            <div class="flex flex-col
                bg-white
                gap-4 w-full h-full">
                <div>
                    <div>Create Room:</div>
                    <div class="flex">
                        <input/>
                        <button class="bg-navbar-menu rounded-sm">CREATE ROOM</button>
                    </div>
                </div>
                <div>
                    <div>Join Room:</div>
                    <div class="flex">
                        <input/>
                        <button class="bg-navbar-menu rounded-sm">JOIN ROOM</button>
                    </div>
                </div>
                <div class="flex flex-row">
                    <div>Leave Room:</div>
                    <div>
                        <button class="bg-red-600 rounded-sm">LEAVE ROOM</button>
                    </div>
                </div>
                <div class="flex flex-row">
                    <div>Game Start:</div>
                    <div>
                        <a href="/skribbl">
                            <button class="bg-green-600 rounded-sm">Start Game</button>
                        </a>
                    </div>
                </div>
                <div class="text-center">__________ROOM INFO__________</div>
                <div>Room Code: {{ roomCode }}</div>
                <div>Room Name: {{ roomName }}</div>
                <div>Users in lobby:</div>
                <div class="flex flex-row">
                    <div>
                        <div>Avatar1: </div>
                        <div>Username1: {{ username }}</div>
                    </div>
                    <!-- <div>
                        <div>Avatar2</div>
                        <div>Username2</div>
                    </div> -->
                </div>
            </div>
        </div>
        
    </div>
</template>