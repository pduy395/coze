<template>
  <div>
    <a-modal :open="open" title="Edit bot" centered :closable="false">
      <label for="bot-name" class="fw-medium mb-2 mt-3"
        >Bot name <span style="color: red">*</span></label
      >
      <br />
      <a-input
        v-model:value="name"
        id="bot-name"
        show-count
        :maxlength="40"
        placeholder="Give the bot a unique name"
      />

      <div class="fw-medium mt-4 mb-2">Bot function description</div>
      <a-textarea
        class="mb-5"
        v-model:value="description"
        placeholder="It introduces the bot functions and is displayed to the bot users"
        :auto-size="{ minRows: 3 }"
        show-count
        :maxlength="800"
      />

      <template #footer>
        <a-button class="cancel-btn" @click="$emit('closeModal')" :disabled="showSpin"
          >Cancel</a-button
        >
        <a-button class="submit-btn submit-btn--disabled" v-if="name == ''" disabled
          >Confirm</a-button
        >
        <a-button class="submit-btn" v-else @click="handleSubmit" :disabled="showSpin"
          ><a-spin :indicator="indicator" v-show="showSpin" />Confirm</a-button
        >
      </template>
    </a-modal>
  </div>
</template>
<script setup>
import { h, ref, onBeforeUpdate } from 'vue'
import { updateChatbot } from '@/services/ChatbotApi'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { LoadingOutlined } from '@ant-design/icons-vue'
import { useChatBotStore } from '@/stores/chatBotStore'

const props = defineProps({ open: Boolean, botId: String, botName: String, botDescription: String })
const emits = defineEmits(['closeModal'])
const onChange = defineModel('onChange')

const chatBotStore = useChatBotStore()
const name = ref('')
const description = ref('')
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '24px',
    color: 'white',
    marginRight: '10px'
  },
  spin: true
})
const showSpin = ref(false)

onBeforeUpdate(() => {
  name.value = props.botName
  description.value = props.botDescription
  showSpin.value = false
})

const handleSubmit = () => {
  showSpin.value = true

  const newChatbotData = {
    name: name.value,
    description: description.value,
    llm_name: chatBotStore.llm_name,
    prompt: chatBotStore.prompt,
    updated_time: chatBotStore.updated_time,
    favourite: chatBotStore.favourite
  }

  updateChatbot(props.botId, newChatbotData)
    .then((res) => {
      // onChange.value = !onChange.value
      SuccessMessage(res)
      chatBotStore.changeStateValue(name.value, description.value)
      emits('closeModal')
    })
    .catch((err) => {
      showSpin.value = false
      ErrorMessage(err)
    })
}
</script>

<style scoped>
.submit-btn {
  background-color: var(--color-background-button-base);
  color: white;
}
.submit-btn:hover {
  background-color: var(--color-background-button-hover);
  color: white;
}
.submit-btn--disabled {
  opacity: 0.5;
}
</style>
