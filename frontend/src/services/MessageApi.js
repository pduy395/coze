import apiClient from '@/util/http'

export function getMessage(chatbot_id, offset, limit) {
  return apiClient.get(`/message/chatbot/${chatbot_id}?offset=${offset}&limit=${limit}`)
}

export function postMessage(chatbot_id, messageData) {
  return apiClient.post(`/message/chatbot/${chatbot_id}`, messageData)
}

export function deleteMessage(message_id) {
  return apiClient.delete(`/message/${message_id}`)
}

export function deleteChatHistory(chatbot_id) {
  return apiClient.delete(`/message/history/${chatbot_id}`)
}

export function generateMessage(chatbot_id, question) {
  return apiClient.post(`/message/chatbot/${chatbot_id}/generate`, { question: question })
}
