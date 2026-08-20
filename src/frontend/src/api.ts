import axios from 'axios'

// URL locale pour le développement
const API_BASE = 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const login = async (username: string, password: string) => {
  const response = await api.post('/auth/login', null, {
    params: { username, password },
  })
  const { access_token } = response.data
  localStorage.setItem('token', access_token)
  return access_token
}

export const logout = () => {
  localStorage.removeItem('token')
}