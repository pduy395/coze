<template>
  <div>
    <!-- <div v-if="checkInsert == 'before'">
      <hr class="my-3" />
      <h6 class="px-2 fw-light mb-2">Explore</h6>
    </div> -->
    <router-link :to="navigate" style="text-decoration: none">
      <div class="mb-2" @click="() => emits('handleChangeSelectedItem', id)">
        <div
          v-if="id != selectedItem"
          class="nav-item d-flex align-items-center rounded-3 p-2 gap-2"
        >
          <i :class="iconClass"></i>
          <h6>{{ name }}</h6>
        </div>
        <div
          v-else
          class="nav-item nav-item-selected d-flex align-items-center rounded-3 p-2 gap-2"
        >
          <i :class="iconClass"></i>
          <h6>{{ name }}</h6>
        </div>
      </div>
    </router-link>
    <!-- <div v-if="checkInsert == 'after'">
      <hr class="my-3" />
      <h6 class="px-2 py-2 fw-light d-inline">Teams</h6>
      <i class="bi bi-plus-lg float-end rounded-3"></i>
      <div style="height: 80px"></div>
      <div class="d-flex justify-content-between px-2">
        <div v-for="icon in iconList" :key="icon.id">
          <a-tooltip :arrow="icon.onlyContainText" color="white">
            <template #title>
              <div v-if="icon.onlyContainText">
                {{ icon.title }}
              </div>
              <div v-else-if="icon.title === 'Discord-Telegram'">
                <div class="d-flex gap-2">
                  <i class="bi bi-discord"></i>
                  <h6>Discord</h6>
                </div>
                <div class="d-flex gap-2">
                  <i class="bi bi-telegram"></i>
                  <h6>Telegram</h6>
                </div>
              </div>
              <div v-else>
                <div class="d-flex gap-2">
                  <i class="bi bi-youtube"></i>
                  <h6>Youtube</h6>
                </div>
                <div class="d-flex gap-2">
                  <i class="bi bi-twitter-x"></i>
                  <h6>X</h6>
                </div>
              </div>
            </template>
            <i :class="icon.class"></i>
          </a-tooltip>
        </div>
      </div>
      <hr class="my-4" />
    </div> -->
  </div>
</template>

<script setup>
const props = defineProps({
  id: Number,
  name: String,
  iconClass: String,
  checkInsert: String,
  navigate: String
})
const emits = defineEmits(['handleChangeSelectedItem'])
const selectedItem = defineModel('selectedItem')

const iconList = [
  { class: 'bi bi-journal-text p-2 rounded-3', title: 'Documents', onlyContainText: true },
  { class: 'bi bi-alexa p-2 rounded-3', title: 'Discord-Telegram', onlyContainText: false },
  { class: 'bi bi-chat-text p-2 rounded-3', title: 'Youtube-X', onlyContainText: false },
  { class: 'bi bi-envelope p-2 rounded-3', title: 'Feedback', onlyContainText: true }
]
</script>

<style scoped>
* {
  margin: 0;
  color: black;
  padding: 0;
}
.nav-item,
i {
  cursor: pointer;
}
.nav-item:hover,
i:hover {
  background-color: #eee;
}
.nav-item-selected {
  background-color: #eee;
}
h6 {
  font-weight: normal;
}
</style>
