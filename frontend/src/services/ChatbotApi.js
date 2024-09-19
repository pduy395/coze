import apiClient from '@/util/http'

export function createChatbot(chatbotData) {
  return apiClient.post('/chatbot', chatbotData)
}

export function getAllChatbot() {
  return apiClient.get('/chatbot/all')
}

export function getChatbotById(chatbotId) {
  return apiClient.get(`/chatbot/${chatbotId}`)
}

export function deleteChatbot(chatbotId) {
  return apiClient.delete(`/chatbot/${chatbotId}`)
}

export function duplicateChatbot(chatbotId) {
  return apiClient.post(`/chatbot/${chatbotId}/duplicate`, {})
}

export function updateChatbot(chatbotId, chatbotData) {
  return apiClient.patch(`/chatbot/${chatbotId}`, chatbotData)
}

export function optimizePrompt(data) {
  return apiClient.post('/chatbot/optimize-prompt', data)
}

export function UpdateChatbotPrompt(id, data){
  return apiClient.patch(`/chatbot/${id}/prompt`, data)
}

export function addKnowledge(chatbotId, knowledgeId){
  return apiClient.post(`/chatbot/${chatbotId}/knowledge/${knowledgeId}`)
}

export function removeKnowledge(chatbotId, knowledgeId){
  return apiClient.delete(`/chatbot/${chatbotId}/knowledge/${knowledgeId}`)
}

export function getKnowledgeByChatBot(chatbotId){
  return apiClient.get(`/chatbot/${chatbotId}/knowledge`)
}

export function updateChatbotLlmName(chatbotId, data){
  return apiClient.patch(`chatbot/${chatbotId}/llm_label`, data)
}