import { ref } from 'vue'
import { defineStore } from 'pinia'

const AUTH_LOCAL_STORAGE_KEY = 'auth'
const STORE_NAME = 'authStore'

export const useAuthStore = defineStore(STORE_NAME, {
  state: () => ({
    token: ref(''),
    isAuth: ref(false),
    username: ref('')

  }),
  actions: {
    async login(username, password) {
      const response = await fetch('http://127.0.0.1:8000/api-token-auth/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username,
          password
        })
      }).catch((error) => {
        if (error.message === 'Failed to fetch') {
          return false
        }
        return false
      })

      if (response.ok) {
        const data = await response.json()
        this.setToken(data.token)
        this.setUsername(username)
        return true
      } else {
        return false
      }
    },
    async register(first_name, last_name, username, password) {
      const errorMessages = 'Пароль слишком слабый.'
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          first_name,
          last_name,
          username,
          password
        })
      }).catch ((error) => {
        if (error.response.status === 400) {
          const errorData = error.response.data;
          if (errorData.details) {
            if (typeof errorData.details === 'object') {
              errorMessages = errorData.details[0].msg
            } else {
              errorMessages = errorData.details
            }
          }
        }
      })
      if (response.ok) {
        return {isCreated: true}
      } else {
        const data = await response.json()
        const errorMessages = {'username': '', 'password': '', 'first_name': '', 'last_name': ''}
        Object.keys(data.details).forEach((key) => {
          if (data.details[key]) {
            errorMessages[key] = data.details[key].join('\n');
          }
        })
        return {
          isCreated: false,
          errors: errorMessages,
        }
      }
    },
    logout() {
      this.token = ''
      this.isAuth = false
      this.username = ''
      localStorage.removeItem(AUTH_LOCAL_STORAGE_KEY + 'Token')
      localStorage.removeItem(AUTH_LOCAL_STORAGE_KEY + 'Username')
    },
    setToken(token) {
      this.token = token
      localStorage.setItem(AUTH_LOCAL_STORAGE_KEY + 'Token', JSON.stringify(token))
      this.isAuth = true
    },
    getToken() {
      const token = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY + 'Token')
      if (token) {
        this.token = JSON.parse(token)
        this.isAuth = true
      }
      return this.token
    },
    setUsername(username) {
      this.username = username
      localStorage.setItem(AUTH_LOCAL_STORAGE_KEY + 'Username', JSON.stringify(username))
    },
    getUsername() {
      const username = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY + 'Username')
      if (username) {
        this.username = JSON.parse(username)
      }
      return this.username
    },
    getIsAuth() {
      const token = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY + 'Token')
      if (token) {
        this.token = JSON.parse(token)
        this.isAuth = true
      }
      return this.isAuth
    }
  }
})
