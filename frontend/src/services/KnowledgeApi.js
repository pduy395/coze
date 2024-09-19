import apiClient from '@/util/http'

export function createKnowledge(knowledgeData) {
  return apiClient.post('/knowledge', knowledgeData)
}

export function getAllKnowledge() {
  return apiClient.get('/knowledge/all')
}

export function getKnowledgeById(knowledgeId) {
  return apiClient.get(`/knowledge/${knowledgeId}`)
}

export function getAllSegmentOfKnowledge(knowledgeId, offset, limit, search) {
  return apiClient.get(`/knowledge/${knowledgeId}/embed?offset=${offset}&limit=${limit}&search=${search}`)
}

export function deleteKnowledge(knowledgeId) {
  return apiClient.delete(`/knowledge/${knowledgeId}`)
}

export function updateKnowledgeEnable(knowledgeId, state) {
  return apiClient.put(`/knowledge/${knowledgeId}/enable?request=${state}`, {})
}

export function updateKnowledgeInfo(knowledgeId, knowledgeData) {
  return apiClient.put(`/knowledge/${knowledgeId}/modify`, knowledgeData)
}

export function deleteSegment(knowledgeId) {
  return apiClient.delete(`/knowledge/${knowledgeId}/segment`)
}

export function getKnowledgeProcessing(knowledgeId) {
  return apiClient.get(`/knowledge/${knowledgeId}/progress`)
}

export function resegmentKnowledge(knowledgeId, auto, data) {
  return apiClient.post(`/knowledge/${knowledgeId}/resegment?auto=${auto}`, data)
}