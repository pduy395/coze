import { defineStore } from 'pinia'
import { getChatbotById, updateChatbotLlmName } from '@/services/ChatbotApi'
import { ErrorMessage, SuccessMessage } from '@/models/MessageNotifyModel'

export const useChatBotStore = defineStore('chatbot', {
  state: () => ({
    prompt: '',
    name: '',
    llm_name: '',
    description: '',
    updated_time: '',
    favourite: false
  }),
  actions: {
    async fetchChatBot(chatbotId) {
      getChatbotById(chatbotId)
        .then((res) => {
          // console.log(res.data);
          const { prompt, name, llm_name, description, updated_time, favourite } = res.data
          this.prompt = prompt
          this.name = name
          this.llm_name = llm_name
          this.description = description
          this.updated_time = updated_time
          this.favourite = favourite
        })
        .catch((e) => {
          ErrorMessage(e)
        })
    },
    updateChatbot(botId, data) {
      updateChatbotLlmName(botId, data)
        .then((res) => {
          SuccessMessage(res)
        })
        .catch((e) => {
          ErrorMessage(e)
        })
    },
    changeStateValue(newName, newDescription) {
      this.name = newName
      this.description = newDescription
    }
  }
})
