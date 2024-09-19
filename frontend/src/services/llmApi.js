import apiClient from "@/util/http";

export const getAllLlm = async (id) => {
    const response = await apiClient.get(`/llm/chatbot/${id}`);
    return response;
}

export const getLlmById = async (id) => {
    const response = await apiClient.get(`llm/${id}`);
    return response;
}

export const updateConfigLLM = async(id, data) => {
  const response = await apiClient.patch(`/llm/${id}`, data)
  return response
}