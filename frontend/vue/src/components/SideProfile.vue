<template>
  <dialog ref="dialog">
    <div class="h-8 w-full flex-center gap-4">
      <button
        @click="bar = 0"
        class="size-10 cursor-pointer flex-center rounded-full text-text-main"
        :class="selectWindow === 0 ? 'bg-sidebar border border-text-main' : ''"
      >
        <component :is="profileIcon" class="size-8"/>
      </button>
      <button
        @click="bar = 1"
        class="size-10 cursor-pointer flex-center rounded-full "
        :class="selectWindow === 1 ? 'bg-sidebar border border-text-main' : ''"
      >
        <component :is="contacstIcon" class="size-10 stroke-text-main"/>
      </button>
      <button
        @click="bar = 2"
        class="size-10 cursor-pointer flex-center rounded-full"
        :class="selectWindow === 2 ? 'bg-sidebar border border-text-main' : ''"
      >
        <component :is="addFriend" class="size-7.5 text-text-main"/>
      </button>
    </div>
    <hr>
    <BasicInformations v-if="selectWindow === 0"/>
    <Social v-else-if="selectWindow === 1"/>
    <AddFriends v-else/>
  </dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

import profileIcon              from '@assets/profile.svg';
import contacstIcon             from '@assets/contacts.svg';
import addFriend                from '@assets/addFriend.svg';

import BasicInformations        from './sideProfile/BasicInformations.vue';
import Social                   from './sideProfile/Social.vue';
import AddFriends               from './sideProfile/AddFriends.vue';

const props         = defineProps({ open: Boolean });
const dialog        = ref(null);
const bar           = ref(0);
const selectWindow  = computed(() => bar.value === 0 ? 0 : (bar.value === 1 ? 1 : 2));

watch(() => props.open, (val) => {
  val ? dialog.value.show() : dialog.value.close();
})
</script>

<style scoped>
@import "@/style.css";

dialog {
  @apply sm:m-2 w-full h-full z-70 sm:w-md sm:h-auto sm:rounded-4xl
    shadow-md fixed left-auto p-12 pt-6;
  background-color: var(--color-profile);
}

hr {
  @apply h-px border-sidebar-border my-6;
}
</style>
