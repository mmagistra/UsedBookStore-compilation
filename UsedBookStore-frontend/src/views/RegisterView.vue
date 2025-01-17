<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header text-center">
            <h3>Регистрация</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="first_name" class="form-label">Имя</label>
                <input type="text" class="form-control" id="first_name" v-model="first_name" required
                :class="{ 'is-invalid': errors.first_name && invalidData }">
                <div class="text-danger" v-if="errors.first_name && invalidData">
                  {{ errors.first_name }}
                </div>
              </div>
              <div class="mb-3">
                <label for="last_name" class="form-label">Фамилия</label>
                <input type="text" class="form-control" id="last_name" v-model="last_name" required
                :class="{ 'is-invalid': errors.last_name && invalidData }">
                <div class="text-danger" v-if="errors.last_name && invalidData">
                  {{ errors.last_name }}
                </div>
              </div>
              <div class="mb-3">
                <label for="username" class="form-label">Логин</label>
                <input type="text" class="form-control" id="username" v-model="username" required
                :class="{ 'is-invalid': errors.username && invalidData }">
                <div class="text-danger" v-if="errors.username && invalidData">
                  {{ errors.username }}
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="password" v-model="password" required
                :class="{ 'is-invalid': errors.password && invalidData }">
                <div class="text-danger" v-if="errors.password && invalidData">
                  {{ errors.password }}
                </div>
              </div>
              <div class="mb-3">
                <label for="password_confirmation" class="form-label">Подтверждение пароля</label>
                <input type="password" class="form-control" id="password_confirmation" v-model="password_confirmation" required
                :class="{ 'is-invalid': errors.password_confirmation && invalidData }">
                <div class="text-danger" v-if="errors.password_confirmation && invalidData">
                  {{ errors.password_confirmation }}
                </div>
              </div>
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
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
import { useAuthStore } from '../stores/authStore.js'
import { useToastStore } from '../stores/toastStore.js'

const authStore = useAuthStore()
const toastStore = useToastStore()
const first_name = ref('')
const last_name = ref('')
const username = ref('')
const password = ref('')
const password_confirmation = ref('')
const invalidData = ref(false)
const errors = ref({
  first_name: '',
  last_name: '',
  username: '',
  password: '',
  password_confirmation: '',
})

const handleRegister = async () => {
  if (password.value !== password_confirmation.value) {
    invalidData.value = true
    errors.value = {'password_confirmation': 'Пароли не совпадают'}
    return
  }

  const registerCallback = await authStore.register(first_name.value, last_name.value, username.value, password.value)
  if (registerCallback.isCreated) {
    toastStore.addToast({
      'title': 'Успешная регистрация',
      'subtitle': '',
      'text': 'Вы успешно зарегистрировались',
      'color': 'success',
      'icon': 'check',
    }, 5000)
    window.location.href = '/login'
  } else {
    invalidData.value = true
    errors.value = registerCallback.errors
  }
}
</script>

<style lang="scss" scoped>
</style>

