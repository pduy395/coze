<template>
  <div class="preview-chat px-3 py-4">
    <div
      class="chat-history"
      @scroll.passive="
        (e) => {
          scrollTop = e.target.scrollTop
          scrollHeight = e.target.scrollHeight
        }
      "
    >
      <div v-if="chatHistory.length || showResponding">
        <div v-for="message in chatHistory" :key="message.id">
          <Message
            :question="message.question"
            :answer="message.answer"
            :tokens="message.input_tokens + message.output_tokens"
            :latency="message.latency"
            :question-time="message.time"
            :username="userStore.username"
            :bot-name="chatBotStore.name"
            :message-id="message.id"
            v-model:messageDeleteId="messageDeleteId"
          />
        </div>
      </div>
      <div v-else>
        <div class="d-flex align-items-center flex-column">
          <DefaultBotIcon width="50px" height="50px" border-radius="10px" />
          <h6>{{ chatBotStore.name }}</h6>
        </div>
      </div>
      <div v-show="showResponding">
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
              <h6 class="username">{{ userStore.username }}</h6>
              <p class="question d-inline-flex text-white rounded-4" style="font-size: 14px">
                {{ respondingQuestion }}
              </p>
            </div>
          </div>
          <div class="chatbot d-flex gap-2">
            <DefaultBotIcon width="30px" height="30px" border-radius="100%" />
            <div>
              <h6 class="bot-name">{{ chatBotStore.name }}</h6>
              <h6 v-if="isStopResponding > 0">
                There are too many users now. Please wait a moment.
              </h6>
              <div v-if="isResponding" class="d-flex flex-column align-items-start gap-3">
                <a-spin :indicator="indicator" />
                <div
                  class="d-flex ps-1 pe-2 align-items-center border"
                  style="cursor: pointer; border-radius: 12px"
                  @click="handleStopResponding"
                >
                  <i class="stop-responding-icon bi bi-stop-circle fs-6"></i>
                  <h6 class="stop-responding-text m-0">Stop responding</h6>
                </div>
              </div>
              <div v-else>
                <p
                  class="answer typing d-inline-flex flex-column rounded-4 mb-1"
                  style="font-size: 14px; white-space: pre-line"
                  v-html="markedAnswer"
                ></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-for="brLine in brLinesNumber" :key="brLine.id">
        <br />
      </div>
    </div>

    <div class="pe-4 position-relative">
      <div class="d-flex gap-3 px-2 align-items-center justify-content-between">
        <a-tooltip class="ms-2 mb-1" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">Delete chat history</h6>
          </template>
          <a-button class="p-0" style="border: none" @click="handleDeleteChatHistory">
            <i class="bi bi-trash z-1"></i>
          </a-button>
        </a-tooltip>
        <a-textarea
          class="question-input"
          placeholder="Send a message"
          style="font-size: 14px"
          v-model:value="question"
          :auto-size="{ minRows: 1 }"
          @keydown.enter.exact.prevent="
            () => {
              showResponding ? handleStopResponding() : handleSendQuestion()
            }
          "
        ></a-textarea>
        <a-tooltip class="ms-2 mb-1 me-3" color="gray" placement="top">
          <template #title>
            <h6 class="text-white fw-normal m-0">
              {{ showResponding ? 'Stop responding' : 'Send' }}
            </h6>
          </template>
          <a-button
            class="p-0"
            style="border: none"
            @click="
              () => {
                showResponding ? handleStopResponding() : handleSendQuestion()
              }
            "
          >
            <SendOutlined
              class="mb-5 fs-6"
              v-if="!showResponding"
              :style="{ color: question.length ? '#4e40e5' : 'black' }"
            />
            <i class="bi bi-square-fill" v-else></i>
          </a-button>
        </a-tooltip>
      </div>
      <div class="note text-center mt-2 px-3">
        The content is generated by AI and is used for reference only, as it may be untrue and
        inaccurate.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, h, watch, nextTick, inject } from 'vue'
import { onBeforeMount, onMounted, onBeforeUpdate, onBeforeUnmount } from 'vue'
import { SuccessMessage, ErrorMessage, WarningMessage } from '@/models/MessageNotifyModel'
import { postMessage, deleteChatHistory, getMessage } from '@/services/MessageApi'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/authStore'
import { LoadingOutlined, SendOutlined } from '@ant-design/icons-vue'
import { useChatBotStore } from '@/stores/chatBotStore'
import Message from '../Message/Message.vue'
import DefaultBotIcon from '../icons/DefaultBotIcon.vue'
import { marked } from 'marked'
import { message } from 'ant-design-vue'
import { ws_API_URL } from '@/util/http'

const { savedTime, showSaving } = inject('updateSavedTime')
const { renderLoading } = inject('renderLoading')

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const chatBotStore = useChatBotStore()
const chatbotId = route.params.botId
const chatHistory = ref([])
const question = ref('')
const answer = ref('')
const markedAnswer = ref('')
const respondingQuestion = ref('')
const brLinesNumber = ref(2)
const showResponding = ref(false)
const isResponding = ref(false)
const isStopResponding = ref(0)
const inputTokens = ref(0)
const outputTokens = ref(0)
const sendQuestionTime = ref('')
const stopRespondingTime = ref('')
const scrollTop = ref(0)
const scrollHeight = ref(0)
const continueFetchChatHistory = ref(true)
const messageDeleteId = ref(-1)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '24px'
  },
  spin: true
})
const token = localStorage.getItem('token')
const wsURL = `${ws_API_URL}/ws/generate/${chatbotId}?token=${token}`
const ws = new WebSocket(wsURL)
const isPendingGetChatHistory = ref(false)

ws.onopen = () => {
  console.log('WebSocket connected')
  ws.send('ping pong')
}
ws.onclose = (event) => {
  console.log('WebSocket closed')
  console.log(event)
  if (event.reason) {
    handleStopResponding()
    isStopResponding.value = 0

    const reason = event.reason
    message.error(reason)
    if (reason == 'Could not validate credentials') {
      router.push({ name: 'Login' })
    } else {
      if (reason == 'Object not found') router.push({ name: 'NotFound' })
      else message.error('Something is wrong! Please reload the page and try again.')
    }
  }
}
ws.onerror = (err) => {
  // console.log(ws.readyState);
  console.log(err)
}
onBeforeMount(async () => {
  getChatHistory().then(() => {
    setTimeout(() => {
      renderLoading.value = false
    }, 300)
  })
})
onMounted(() => {
  setTimeout(() => {
    scrollDownToTheBottom()
  }, 305)
  const textarea = document.getElementsByClassName('question-input')[0]
  textarea.addEventListener('input', () => {
    textarea.style.height = textarea.scrollHeight + 1.6 + 'px'
  })
})
onBeforeUnmount(() => {
  if (ws.readyState == 1) ws.close()
})
watch(
  () => messageDeleteId.value,
  () => {
    const temp = chatHistory.value.filter((message) => message.id != messageDeleteId.value)
    chatHistory.value = temp
  }
)
watch(
  () => scrollTop.value,
  () => {
    if (scrollTop.value * 20 <= scrollHeight.value) getChatHistory()
  }
)

const getChatHistory = async () => {
  if (isPendingGetChatHistory.value) return
  isPendingGetChatHistory.value = true

  if (!continueFetchChatHistory.value) return

  getMessage(chatbotId, chatHistory.value.length, 10)
    .then(async (res) => {
      // console.log(res.data)
      continueFetchChatHistory.value = res.data.length != 0
      const temp = [...chatHistory.value]
      temp.unshift(...res.data.reverse())
      chatHistory.value = temp

      await nextTick()
      if (chatHistory.value.length != res.data.length) {
        const elm = document.getElementsByClassName('chat-history')[0]
        elm.scrollTop = elm.scrollHeight - scrollHeight.value
      }
    })
    .catch((err) => {
      ErrorMessage(err)
    })
    .finally(() => (isPendingGetChatHistory.value = false))
}
const scrollDownToTheBottom = () => {
  setTimeout(() => {
    const elm = document.getElementsByClassName('chat-history')[0]
    elm.scrollTop = elm.scrollHeight
  }, 0)
}
const handleDeleteChatHistory = () => {
  if (showResponding.value) {
    WarningMessage('Please wait for reply or stop responding')
    return
  }
  if (chatHistory.value.length == 0) {
    WarningMessage('History chat is empty')
    return
  }

  deleteChatHistory(chatbotId)
    .then((res) => {
      showSaving.value = true
      SuccessMessage(res)
      chatHistory.value = []
      setTimeout(() => {
        savedTime.value = new Date(Date.now()).toLocaleTimeString()
        showSaving.value = false
      }, 500)
    })
    .catch((err) => ErrorMessage(err))
}
const handleSendQuestion = () => {
  if (!question.value.trim()) return
  if (ws.readyState == 0) {
    WarningMessage('Please wait for the connection to complete')
    return
  }
  if (showResponding.value) {
    WarningMessage('Please wait for reply or stop responding')
    return
  }
  if (question.value == '') {
    WarningMessage('Please enter a question')
    return
  }

  inputTokens.value = 0
  outputTokens.value = 0
  sendQuestionTime.value = new Date().toISOString()
  stopRespondingTime.value = new Date().toISOString()
  answer.value = ''
  respondingQuestion.value = question.value
  question.value = ''

  showResponding.value = true
  isResponding.value = true
  scrollDownToTheBottom()
  generateMessageByWebSocket()
}
const generateMessageByWebSocket = () => {
  ws.send(respondingQuestion.value)

  ws.onmessage = (message) => {
    const messageData = JSON.parse(message.data)
    if (isStopResponding.value > 0) {
      if (messageData.data == undefined) isStopResponding.value--
      return
    }

    isResponding.value = false
    inputTokens.value = messageData.input_tokens
    outputTokens.value = messageData.output_tokens

    if (messageData.data == undefined) {
      postMessage(chatbotId, messageData)
        .then((res) => {
          // console.log(res.data)
          chatHistory.value = [...chatHistory.value, { ...messageData, id: res.data.id }]
          showResponding.value = false
        })
        .catch((err) => {
          handleStopResponding()
          ErrorMessage(err)
        })
    } else displayAnswer(messageData.data)
  }
}
const handleStopResponding = () => {
  isStopResponding.value++
  if (answer.value == '') {
    showResponding.value = false
    isResponding.value = false
    question.value = respondingQuestion.value
    return
  }

  stopRespondingTime.value = new Date().toISOString()
  const messageData = {
    answer: answer.value,
    question: respondingQuestion.value,
    input_tokens: inputTokens.value,
    output_tokens: outputTokens.value,
    time: sendQuestionTime.value,
    latency: Date.parse(stopRespondingTime.value) - Date.parse(sendQuestionTime.value)
  }

  postMessage(chatbotId, messageData)
    .then((res) => {
      // console.log(res.data)
      chatHistory.value = [...chatHistory.value, { ...messageData, id: res.data.id }]
    })
    .catch((err) => {
      ErrorMessage(err)
    })
    .finally(() => {
      showResponding.value = false
      isResponding.value = false
    })
}
const displayAnswer = (respond) => {
  answer.value = answer.value + respond
  markedAnswer.value = marked(answer.value)
  scrollDownToTheBottom()
}
</script>

<style lang="scss" scoped>
i {
  cursor: pointer;
  border-radius: 5px;
  padding: 4px;
}
i:hover {
  background-color: var(--color-background-hover);
}
.chat-history {
  height: calc(100vh - 240px);
  overflow: auto;
}
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
  white-space: pre-line;
  max-width: 100%;
}
.answer {
  background-color: #f7f7fa;
  border: 1px solid #e7e7e9;
  padding: 8px;
  font-weight: 500;
}
.stop-responding-icon,
.stop-responding-text {
  color: var(--color-background-button-base);
}
.question-input {
  position: absolute;
  bottom: 0;
  right: 30px;
  width: calc(100% - 80px);
  overflow-y: auto;
  max-height: 126px;
  padding: 8px 36px 8px 16px;
  border-radius: 30px;
}
.note {
  position: absolute;
  bottom: -40px;
  width: 100%;
}
</style>
