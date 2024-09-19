<template>
  <div class="message px-4 py-2 rounded-2">
    <div class="user d-flex gap-2">
      <img
        class="user-avt"
        :src="userStore.avatar"
        alt=""
        width="30px"
        height="30px"
        style="border-radius: 100%"
      />
      <div>
        <div class="d-flex justify-content-between gap-5" style="height: 26px">
          <h6 class="username">{{ username }}</h6>
          <p class="questionTime">{{ new Date(questionTime).toLocaleString() }}</p>
        </div>
        <p class="question d-inline-flex text-white rounded-4" style="font-size: 14px">
          {{ question }}
        </p>
      </div>
    </div>
    <div class="chatbot d-flex gap-2">
      <DefaultBotIcon width="30px" height="30px" border-radius="100%" />
      <div>
        <h6 class="bot-name">{{ botName }}</h6>
        <p
          class="answer d-inline-flex flex-column rounded-4 mb-1"
          :id="messageId"
          v-html="markedAnswer"
          style="font-size: 14px"
        ></p>
      </div>
    </div>
    <div class="d-flex justify-content-between align-items-center" style="padding-left: 35px">
      <div class="time d-flex gap-0 align-items-center">
        <i class="bi bi-check2 fs-5"></i>
        <h6 class="fw-light m-0">{{ (latency / 1000).toFixed(1) }}s | {{ tokens }} Tokens</h6>
      </div>
      <div class="options">
        <a-tooltip class="copy ms-2" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">Copy</h6>
          </template>
          <i class="bi bi-copy" @click="handleCopyAnswer"></i>
        </a-tooltip>
        <!-- <a-tooltip class="debug ms-2" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">Debug</h6>
          </template>
          <i class="bi bi-gear"></i>
        </a-tooltip> -->
        <!-- <a-tooltip class="quote ms-2" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">Quote</h6>
          </template>
          <i class="bi bi-quote"></i>
        </a-tooltip> -->
        <a-tooltip class="delete ms-2" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">Delete</h6>
          </template>
          <i class="bi bi-trash" @click="handleDeleteMessage"></i>
        </a-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { deleteMessage } from '@/services/MessageApi'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { message } from 'ant-design-vue'
import { marked } from 'marked'
import DefaultBotIcon from '../icons/DefaultBotIcon.vue'
import copy from 'clipboard-copy'
import RemoveMarkdown from 'remove-markdown'
import { useUserStore } from '@/stores/authStore'

const props = defineProps({
  question: String,
  answer: String,
  username: String,
  botName: String,
  latency: Number,
  questionTime: String,
  tokens: Number,
  messageId: Number
})
const messageDeleteId = defineModel('messageDeleteId')
const markedAnswer = marked(props.answer)
const userStore = useUserStore()

const handleDeleteMessage = () => {
  // console.log(props)
  deleteMessage(props.messageId)
    .then((res) => {
      messageDeleteId.value = props.messageId
      SuccessMessage(res)
    })
    .catch((err) => ErrorMessage(err))
}
const handleCopyAnswer = () => {
  copy(RemoveMarkdown(props.answer))
  message.success('Copy successfully')
}
</script>

<style lang="scss" scoped>
.message {
  border: 1px solid white;
}
.message:hover {
  border: 1px solid #e7e7e9;
}
.message:hover .options,
.message:hover .questionTime {
  display: flex;
}
.question {
  background-color: var(--color-background-button-base);
  padding: 12px 8px 12px 8px;
  font-weight: 500;
}
p {
  white-space: pre-line;
  max-width: 100%;
}
.questionTime {
  display: none;
}
.answer {
  background-color: #f7f7fa;
  border: 1px solid #e7e7e9;
  padding: 8px;
  font-weight: 500;
}
.options {
  display: none;
}
i {
  cursor: pointer;
  border-radius: 5px;
  padding: 4px;
}
i:hover {
  background-color: var(--color-background-hover);
}
</style>
