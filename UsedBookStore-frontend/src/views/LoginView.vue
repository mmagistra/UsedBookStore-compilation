<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header text-center">
                        <h3>Авторизация</h3>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="handleLogin" id="loginForm">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" class="form-control" id="username" v-model="username" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Пароль</label>
                                <input type="password" class="form-control" id="password" v-model="password" required>
                            </div>
                            <div class="mb-3" v-if="invalidData">
                                <p class="text-danger">Неправильный логин или пароль</p>
                            </div>
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">Войти</button>
                                <router-link to="/register" class="btn btn-secondary">Зарегистрироваться</router-link>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

import {useAuthStore} from '../stores/authStore.js'
import {useToastStore} from '../stores/toastStore.js'

const username = ref('')
const password = ref('')
const invalidData = ref(false)

const authStore = useAuthStore()
const toastStore = useToastStore()

const handleLogin = async () => {
    const isDataCorrect = await authStore.login(username.value, password.value)

    if (isDataCorrect) {
        toastStore.addToast({
            'title': `Добро пожаловать, ${username.value}`,
            'subtitle': '',
            'text': 'Вы успешно вошли в аккаунт',
            'color': 'success',
            'icon': 'check',
        }, 5000)
        invalidData.value = false
        window.location.href = '/'
    }
    else {
        invalidData.value = true
        password.value = ''
    }
}
</script>

<style lang="scss" scoped>

</style>

