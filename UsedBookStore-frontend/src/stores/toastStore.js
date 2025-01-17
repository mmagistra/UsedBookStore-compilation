import { ref } from 'vue'
import { defineStore } from 'pinia'

const AUTH_LOCAL_STORAGE_KEY = 'toastStore'
const STORE_NAME = 'toastStore'

export const useToastStore = defineStore(STORE_NAME, {
    state: () => ({
        toasts: ref([])
    }),
    actions: {
        addToast(toast, timeToClose = 0) {
            if (timeToClose > 0) {
                toast.timeToClose = timeToClose
            }
            // toast.id = Math.max(...this.toasts.map(t => t.id), 0) + 1
            toast.id = Date.now()
            localStorage.setItem(AUTH_LOCAL_STORAGE_KEY + toast.id, JSON.stringify(toast))
            this.toasts.push(toast)
        },
        removeToast(id) {
            const newToasts = this.toasts.filter(t => t.id !== id)
            this.toasts = newToasts
            localStorage.removeItem(AUTH_LOCAL_STORAGE_KEY + id)
        },
        uploadToasts() {
            this.toasts = []
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i)
                if (key.startsWith(AUTH_LOCAL_STORAGE_KEY)) {
                    const toast = JSON.parse(localStorage.getItem(key))
                    this.toasts.push(toast)
                }
            }
        },
        getToasts() {
            return this.toasts
        },
    }
})

