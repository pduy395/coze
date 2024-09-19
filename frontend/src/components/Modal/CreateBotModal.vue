<template>
  <div>
    <a-modal :open="open" title="Create bot" centered :closable="false">
      <label for="bot-name" class="fw-medium mb-2 mt-3"
        >Bot name <span style="color: red">*</span></label
      >
      <br />
      <a-input
        v-model:value="botName"
        id="bot-name"
        show-count
        :maxlength="40"
        placeholder="Give the bot a unique name"
      />

      <!-- <div class="fw-medium mt-4 mb-2">User Message Billing <span style="color: red">*</span></div>
      <div>
        When enabled, the user covers the message credit costs; when disabled, the bot creator
        covers the message credit costs.
        <a-switch
          class="switch float-end"
          :checked="switchState"
          @click="handleClickSwitch"
        ></a-switch>
      </div> -->
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
        <a-button class="submit-btn submit-btn--disabled" v-if="!botName.trim()" disabled
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
import { ref, watch, onBeforeUpdate, h } from 'vue'
import { Chatbot } from '@/models/ChatbotModel'
import { createChatbot } from '@/services/ChatbotApi'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { LoadingOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'

const props = defineProps({ open: Boolean })
const emits = defineEmits(['closeModal'])

const router = useRouter()
const botName = ref('')
const switchState = ref(true)
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
  botName.value = ''
  description.value = ''
  showSpin.value = false
})
const handleClickSwitch = () => {
  switchState.value = !switchState.value
}
const handleSubmit = () => {
  showSpin.value = true
  const chatbotData = new Chatbot(botName.value, description.value)
  // console.log(chatbotData);
  createChatbot(chatbotData)
    .then((res) => {
      SuccessMessage(res)
      router.push(`/space/bot/${res.data.id}`)
    })
    .catch((err) => {
      ErrorMessage(err)
      showSpin.value = false
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
