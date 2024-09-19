import apiClient from '@/util/http'

export function UploadFile(data, knowledge_id) {
  return apiClient.post(`/file?knowledge_id=${knowledge_id}`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function getDataUrl(data) {
  return apiClient.put(`/file/data_url`, data)
}

export function getDataFromLocal(){
  return apiClient.get('/file/data_url')
}

export function uploadFileOnline(data, knowledge_id) {
  return apiClient.post(`/file/data_url?knowledge_id=${knowledge_id}`, data)
}

export function EmbedFileFirst(knowledge_id, auto, data){
  return apiClient.put(`/file/${knowledge_id}/embed-first?auto=${auto}`, data)
}

export function EmbedNext(data){
  return apiClient.put(`/file/embed-next`, data)
}

export function deleteDocument(file_id) {
  return apiClient.delete(`/file?file_id=${file_id}`)
}

export function renameDocument(file_id, new_name) {
  return apiClient.put(`/file/${file_id}/name`, { name: new_name })
}

export function editSegment(file_id, index, doc) {
  return apiClient.put(`/file/replace-doc?file_id=${file_id}&index=${index}`, { content: doc })
}

export function insertSegment(file_id, behind_segment_index, content) {
  return apiClient.put(`/file/insert-doc?file_id=${file_id}&index=${behind_segment_index}`, {
    content: content
  })
}

export function getSegmentOfDocument(file_id, offset, limit, search) {
  return apiClient.get(`/file/${file_id}/embed?offset=${offset}&limit=${limit}&search=${search}`)
}
