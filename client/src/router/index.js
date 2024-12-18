import AuthorsView from '@/views/AuthorsView.vue'
import CharactersView from '@/views/CharactersView.vue'
import EpisodesView from '@/views/EpisodesView.vue'
import MediaView from '@/views/MediaView.vue'
import OffArtView from '@/views/OffArtView.vue'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({ 
  history: createWebHistory(import.meta.env.BASE_URL), 
  routes: [ 
    { 
      path: "/", 
      name: "CharactersView", 
      component: CharactersView, 
    }, 
    { 
      path: "/media", 
      name: "MediaView", 
      component: MediaView, 
    }, 
    { 
      path: "/episodes", 
      name: "EpisodesView", 
      component: EpisodesView, 
    }, 
    { 
      path: "/authors", 
      name: "AuthorsView", 
      component: AuthorsView, 
    }, 
    { 
      path: "/offart", 
      name: "OffArtView", 
      component: OffArtView, 
    },
    { 
      path: "/users", 
      name: "LoginView", 
      component: LoginView, 
    },
  ] 
})
export default router
