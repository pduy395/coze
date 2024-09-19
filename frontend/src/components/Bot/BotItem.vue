<template>
  <div class="bot-item rounded-2 p-3 shadow" @click="handleNavigate">
    <div class="d-flex justify-content-between">
      <div class="">
        <h6
          style="max-width: 290px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap"
        >
          {{ botName }}
        </h6>
        <p
          class="fw-light"
          style="max-width: 290px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap"
        >
          {{ description }}
        </p>
      </div>
      <DefaultBotIcon width="60px" height="60px" border-radius="10px" />
    </div>
    <h6 class="fw-light mt-4 text-black-50" style="font-size: 12px">
      {{ llmName }} ~ Edited {{ new Date(updatedTime).toLocaleString() }}
    </h6>
    <div class="d-flex justify-content-between align-items-center">
      <div class="profile d-flex align-items-center mt-3 gap-1 fs-1">
        <img style="width: 20px; height: 20px; border-radius: 50%" :src="userStore.avatar" alt="" />
        <h6 class="fw-light text-black-50">{{ userStore.username }}</h6>
      </div>
      <div class="d-flex gap-2">
        <a-popover>
          <template #content>
            <h6 v-if="favorite" class="fw-normal">Remove from favorites list</h6>
            <h6 v-else class="fw-normal">Add to favorites list</h6>
          </template>
          <i
            v-if="favorite"
            class="bi bi-star-fill px-1 mt-2 rounded-2 text-warning"
            @click="(e) => handleUpdateFavorite(e)"
          ></i>
          <i
            v-else
            class="bi bi-star-fill px-1 mt-2 rounded-2 text-white"
            @click="(e) => handleUpdateFavorite(e)"
          ></i>
        </a-popover>
        <a-tooltip color="white" placement="bottomRight" :arrow="false">
          <template #title>
            <div class="options text-black">
              <!-- <h6>Analysis</h6> -->
              <h6 @click="handleDuplicateChatbot">Duplicate</h6>
              <!-- <h6>Migrate</h6> -->
              <h6 class="text-danger" @click="handleDeleteChatbot">Delete</h6>
            </div>
          </template>
          <i
            class="bi bi-three-dots-vertical px-1 mt-2 rounded-2"
            @click="
              (e) => {
                e.stopPropagation()
              }
            "
          ></i>
        </a-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteChatbot, duplicateChatbot, updateChatbot } from '@/services/ChatbotApi'
import { Chatbot } from '@/models/ChatbotModel'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { useUserStore } from '@/stores/authStore'
import DefaultBotIcon from '../icons/DefaultBotIcon.vue'

const props = defineProps({
  botId: Number,
  botName: String,
  description: String,
  favorite: Boolean,
  llmName: String,
  updatedTime: String,
  prompt: String
})

const userStore = useUserStore()
const onDuplicate = defineModel('onDuplicate')
const onDelete = defineModel('onDelete')
const onChangeFavorites = defineModel('onChangeFavorites')
const route = useRoute()
const router = useRouter()
const path = route.fullPath

const handleNavigate = () => {
  router.push(`${path}/${props.botId}`)
}
const handleDeleteChatbot = () => {
  deleteChatbot(props.botId)
    .then((res) => {
      onDelete.value = props.botId
      SuccessMessage(res)
    })
    .catch((err) => {
      ErrorMessage(err)
    })
}
const handleDuplicateChatbot = () => {
  duplicateChatbot(props.botId)
    .then((res) => {
      onDuplicate.value = res.data.copy_chatbot
      SuccessMessage(res)
    })
    .catch((err) => {
      ErrorMessage(err)
    })
}
const handleUpdateFavorite = (e) => {
  e.stopPropagation()

  const chatbotData = new Chatbot(
    props.botName,
    props.description,
    props.prompt,
    props.llmName,
    props.updatedTime,
    !props.favorite
  )
  updateChatbot(props.botId, chatbotData)
    .then((res) => {
      onChangeFavorites.value = { botId: props.botId, state: !onChangeFavorites.value.state }
      SuccessMessage(res)
    })
    .catch((err) => {
      ErrorMessage(err)
    })
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
.bot-item {
  cursor: pointer;
}
i.bi-heartbreak-fill {
  font-size: xx-large;
  color: var(--color-background-button-base);
}
.profile > h6 {
  font-size: 14px;
}
.avatar {
  background-color: var(--color-background-button-base);
}
i.bi-three-dots-vertical,
i.bi-star-fill {
  font-size: medium;
  background-color: rgb(128, 128, 128, 0.15);
}
.options > h6 {
  font-weight: normal;
  padding: 8px 4px;
  cursor: pointer;
  border-radius: 5px;
}
.options > h6:hover {
  background-color: var(--color-background-hover);
}
</style>
