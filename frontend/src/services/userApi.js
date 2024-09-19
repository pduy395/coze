import axios from 'axios'
import apiClient from '@/util/http'
import { http_API_URL } from '@/util/http';

export const registerUser = async (data) => {
    const res = await axios.post(`${http_API_URL}/user/register`, data);
    return res;
}

export const loginUser = async (data) => {
        const response = await axios.post(`${http_API_URL}/user/login`, data, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        return response;
}

export const updateUser = async (data) => {
  const res = await apiClient.put('/user/info', data)
  return res
}

export const getDetailUser = async () => {
  const res = await apiClient.get('/user')
  return res
}

export const updateAvatar = async (data) => {
  const res = await apiClient.put('/user/avatar', data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return res
}

export const changePassword = async (data) => {
  const res = await apiClient.put('/user/password', data)
  return res
}

export const deleteUser = async () => {
  const res = await apiClient.delete('/user')
  return res
}
