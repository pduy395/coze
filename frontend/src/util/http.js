import axios from 'axios'
import router from '@/router' // Đường dẫn đến tệp router của bạn

const IP = '192.168.1.7'
const PORT = '8000'
export const http_API_URL = `http://${IP}:${PORT}`
export const ws_API_URL = `ws://${IP}:8500`
  
const apiClient = axios.create({
  baseURL: http_API_URL
})

// Interceptor để thêm token vào tất cả các yêu cầu
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    const tokenExpiration = localStorage.getItem('tokenExpiration')

    if (token && tokenExpiration) {
      if (new Date().getTime() > parseInt(tokenExpiration, 10)) {
        // Token hết hạn
        localStorage.removeItem('token')
        localStorage.removeItem('tokenExpiration')
        router.push({ name: 'Login' })
        return Promise.reject(new Error('Token expired'))
      }
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor để xử lý lỗi khi token hết hạn
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    if (error.response && error.response.status === 401) {
      // Token hết hạn hoặc không hợp lệ
      localStorage.removeItem('token')
      localStorage.removeItem('tokenExpiration')
      router.push({ name: 'Login' })
    }
    if (error?.response?.status === 422) {
      // router.push({ name: 'NotFound' })
      
    }
    return Promise.reject(error)
  }
)

export default apiClient
