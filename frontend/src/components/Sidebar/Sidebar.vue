<template>
  <div
    class="sidebar container d-flex flex-column justify-content-between shadow px-2 py-4 my-2"
    style="width: 230px; height: 100vh"
  >
    <!-- <div class="sidebar__header d-flex gap-2 align-items-center">
      <img src="../../assets/coze-logo.jpg" alt="" class="rounded" height="32px" width="32px" />
      <h2>coze</h2>
    </div> -->
    <div class="sidebar__navigate mt-4">
      <a-button
        class="btn d-flex align-items-center justify-content-center gap-2 py-1 mb-3 w-100"
        @click="() => (open = true)"
      >
        <i class="bi bi-plus-lg" style="color: white"></i>
        <h6 class="text-white">Create bot</h6>
      </a-button>
      <CreateBotModal v-model:open="open" @closeModal="() => (open = false)" />

      <div v-for="navItem in navItems" :key="navItem.id">
        <SidebarNavItem
          v-bind="navItem"
          v-model:selectedItem="selectedItem"
          @handleChangeSelectedItem="handleChangeSelectedItem"
        />
      </div>
    </div>
    <div>
      <a-dropdown placement="top">
        <div
          class="sidebar__profile d-flex align-items-center rounded-3 w-100 py-1 mt-3 gap-2"
          style="cursor: pointer"
        >
          <img
            style="width: 30px; height: 30px; border-radius: 50%"
            :src="authStore.avatar"
            alt=""
          />
          <h6 class="fw-normal">{{ authStore.username }}</h6>
        </div>
        <template #overlay>
          <a-menu style="width: 15vh;">
            <a-menu-item>
              <!-- <a href="/account">My account</a> -->
              <div @click="() => router.push('/account')">My account</div>
            </a-menu-item>
            <a-menu-item>
              <!-- <a @click="logout" href="">Logout</a> -->
               <div @click="logout">Logout</div>
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { onMounted } from 'vue'
import SidebarNavItem from './SidebarNavItem.vue'
import CreateBotModal from '../Modal/CreateBotModal.vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useUserStore()
const navItems = [
  {
    id: 0,
    name: 'Home',
    iconClass: 'bi bi-house-door',
    checkInsert: 'none',
    navigate: '/home'
  },
  {
    id: 1,
    name: 'Personal',
    iconClass: 'bi bi-person',
    checkInsert: 'none',
    navigate: '/space/bot'
  }
  // { id: 2, name: 'Bot Store', iconClass: 'bi bi-robot', checkInsert: 'before', navigate: '/home' },
  // { id: 3, name: 'Plugin Store', iconClass: 'bi bi-box', checkInsert: 'none', navigate: '/home' },
  // {
  //   id: 4,
  //   name: 'Workflow Store',
  //   iconClass: 'bi bi-bounding-box',
  //   checkInsert: 'after',
  //   navigate: '/home'
  // },
  // { id: 5, name: 'Coze Premium', iconClass: 'bi bi-gem', checkInsert: 'none', navigate: '/home' },
  // {
  //   id: 6,
  //   name: 'Coze API',
  //   iconClass: 'bi bi-code-slash',
  //   checkInsert: 'none',
  //   navigate: '/home'
  // },
  // {
  //   id: 7,
  //   name: 'Coze Token',
  //   iconClass: 'bi bi-bank',
  //   checkInsert: 'none',
  //   navigate: '/home'
  // }
]
const open = ref(false)
const selectedItem = ref(route.fullPath == '/home' ? 0 : 1)

onMounted(() => {
  authStore.fetchUser()
})
watch(
  () => route.fullPath,
  () => {
    selectedItem.value = route.fullPath == '/home' ? 0 : 1
  }
)

const handleChangeSelectedItem = (newItem) => {
  selectedItem.value = newItem
}
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('tokenExpiration')
  router.push({ path: '/login' })
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
a {
  text-decoration: none;
}
.btn {
  background-color: var(--color-background-button-base);
}
.btn:hover {
  background-color: var(--color-background-button-hover);
}
.sidebar__footer:hover {
  background-color: var(--color-background-hover);
}
</style>
