export { default as Button }      	from '@components/Button.vue'
export { default as NavBar }      	from '@components/NavBar.vue'
export { default as SideBar }     	from '@components/SideBar.vue'
export { default as SideProfile } 	from '@components/SideProfile.vue'

export { setupFontAwesome } from './fontawesome'
export { setupPinia }       from './pinia'
export { useUi }            from './ui'
export { getCookie }        from './cookieGetter'
export { useSkribbleStore }	from './skribble'
export { 
  fetchUserInfos,
  fetchFriendlist,
  fetchFriends 
} from './fetchUserInfos'
