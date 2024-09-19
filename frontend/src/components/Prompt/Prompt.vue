<template>
  <div class="prompt">
    <header class="prompt_header">
      <div class="prompt_header_title">
        <span>Persona & Prompt</span>
      </div>
      <div @click="showModal" :class="['prompt_header_optimize']">
        <a-tooltip placement="top" color="white" style="background-color: bisque">
          <template #title>
            <span style="color: #111; font-size: 13px">Auto optimize your prompt</span>
          </template>
          <div class="d-flex align-items-center gap-2">
            <HighlightOutlined />
            <span>Optimize</span>
          </div>
        </a-tooltip>
      </div>
      <PromptOptimizeModal
        :open="open"
        :confirm-loading="confirmLoading"
        :optimized-prompt="optimizedPrompt"
        :loading="loading"
        :is-prompt-displayed="isPromptDisplayed"
        :is-socket-complete="isSocketComplete"
        @update:open="(val) => (open = val)"
        @update:optimized-prompt="(val) => (optimizedPrompt = val)"
        @retry="handleRetry"
        @ok="handleOk"
        @close-socket="handleSocketClose"
      />
    </header>

    <div class="prompt_area_wrapper">
      <div class="prompt_area">
        <textarea
          name="prompt"
          id=""
          v-model="data.prompt"
          :placeholder="data.prompt === '' ? placeholderText : ''"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, onBeforeMount, onBeforeUnmount, ref, watch } from 'vue'
import PromptOptimizeModal from '../Modal/PromptOptimizeModal.vue'
import { message } from 'ant-design-vue'
import { UpdateChatbotPrompt } from '@/services/ChatbotApi'
import { useRoute } from 'vue-router'
import { ErrorMessage, SuccessMessage } from '@/models/MessageNotifyModel'
import { useChatBotStore } from '@/stores/chatBotStore'
import { HighlightOutlined } from '@ant-design/icons-vue'
import debounce from 'lodash/debounce'
import { ws_API_URL } from '@/util/http'

const { savedTime, showSaving } = inject('updateSavedTime')

const emit = defineEmits(['update:global-loading'])

const route = useRoute()
const chatBotStore = useChatBotStore()

const token = localStorage.getItem('token')
const wsURL = `${ws_API_URL}/ws/optimize-prompt?token=${token}`
let ws = null
const id = Number(route.params.botId)
const data = ref({
  prompt: chatBotStore.prompt
})
const placeholderText = "Design the bot's persona, features and workflows using natural language."
const open = ref(false)
const confirmLoading = ref(false)
const loading = ref(false)
const optimizedPrompt = ref('')
const isPromptDisplayed = ref(false)
const isSocketComplete = ref(false)
const debouncedUpdatePrompt = debounce(async (newPrompt) => {
  UpdateChatbotPrompt(id, { prompt: newPrompt })
    .then((res) => {
      showSaving.value = true
      setTimeout(() => {
        savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
        showSaving.value = false
      }, 500)
    })
    .catch((err) => ErrorMessage(err))
}, 2000)

onBeforeUnmount(() => {
  if (ws?.readyState == 1) ws?.close()
})
watch(
  () => chatBotStore.prompt,
  (newPrompt) => {
    data.value.prompt = newPrompt
  }
)
watch(
  () => data.value.prompt,
  (newText) => {
    debouncedUpdatePrompt(newText)
  }
)
watch(
  () => open.value,
  () => {
    if (!open.value && ws?.readyState == 1) ws?.close()
  }
)

const showModal = () => {
  if (data.value.prompt) {
    isSocketComplete.value = false
    optimizedPrompt.value = ''
    emit('update:global-loading', true)
    loading.value = true

    ws = new WebSocket(wsURL)

    ws.onopen = () => {
      console.log('WebSocket connected')
      ws.send(JSON.stringify({ prompt: data.value.prompt }))
    }

    ws.onmessage = (event) => {
      if (event.data === 'EOS-8000') {
        isSocketComplete.value = true
      }
      if (event.data !== 'EOS-8000') {
        const response = JSON.parse(event.data)
        optimizedPrompt.value += response.data
      }
      emit('update:global-loading', false)
      loading.value = false
    }

    ws.onerror = (err) => {
      console.log(err)
    }

    open.value = true
  } else {
    message.warning('Please enter text before optimizing.')
  }
}
const handleRetry = () => {
  loading.value = true
  optimizedPrompt.value = ''
  if (isSocketComplete.value) {
    ws.send(JSON.stringify({ prompt: data.value.prompt }))
  }
  isPromptDisplayed.value = false
  isSocketComplete.value = false
}
const handleOk = async () => {
  confirmLoading.value = true
  try {
    data.value.prompt = optimizedPrompt.value
    UpdateChatbotPrompt(id, data.value)
      .then((res) => {
        confirmLoading.value = false
        open.value = false
        SuccessMessage(res)
        showSaving.value = true
        setTimeout(() => {
          savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
          showSaving.value = false
        }, 500)
      })
      .catch((err) => ErrorMessage(err))
  } catch (error) {
    ErrorMessage(error)
  } finally {
    confirmLoading.value = false
    ws.close()
  }
}
const handleSocketClose = () => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.close()
  }
  isSocketComplete.value = false
}
</script>

<style lang="scss" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.prompt {
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: rgb(249 249 249);

  .prompt_header {
    display: flex;
    align-items: center;
    height: 40px;
    justify-content: space-between;
    width: 100%;
    padding: 0 28px;

    .prompt_header_title {
      span {
        font-size: 14px;
        font-weight: 600;
        line-height: 20;
      }
    }

    .prompt_header_optimize {
      cursor: pointer;

      &.active {
        cursor: pointer;
      }

      span {
        font-size: 14px;
        font-weight: 600;
        color: #787171;
      }
    }
  }

  .prompt_area_wrapper {
    height: calc(100vh - 210px);
    overflow: auto;

    .prompt_area {
      height: 100%;
      width: 100%;
      padding: 28px;

      textarea {
        width: 100%;
        height: 100%;
        color: rgba(28, 29, 35, 0.8);
        background-color: rgb(249 249 249);
        font-size: 14px;
        line-height: 22px;
        border: 0 solid transparent;
        outline: none;
        resize: none;
        padding: 0;
      }
    }
  }
}
</style>
