import { defineStore } from "pinia";
import { getKnowledgeByChatBot } from "@/services/ChatbotApi";
import { ErrorMessage } from "@/models/MessageNotifyModel";

export const useKnowledgeStore = defineStore('knowledge',{
    state: () => ({
        knowledgeOfchatbot: []
    }),
    actions: {
        fetchKnowledgeofChatbot(idBot){
            getKnowledgeByChatBot(idBot)
            .then(response => {
                this.knowledgeOfchatbot = response.data;
            })
            .catch(error => {
                ErrorMessage(error)
            })
        }
    }
})