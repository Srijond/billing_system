import axios from 'axios'
import store from './store'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
})

// Add token to requests
api.interceptors.request.use(config => {
  const token = store.state.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      store.commit('LOGOUT')
      window.location = '/login'
    }
    return Promise.reject(error)
  }
)

export default api