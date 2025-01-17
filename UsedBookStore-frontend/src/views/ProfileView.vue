<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header text-center">
            <h3>Профиль</h3>
          </div>
          <div class="card-body">
            <h4 class="card-text text-center mb-3">Добро пожаловать, {{ username }}!</h4>

            <hr>
            <h5 class="card-title text-center mb-3">Зарезервированные книги</h5>
            <div class="list-group">
              <a v-for="book in reservedBooks" :key="book.id" class="list-group-item list-group-item-action">
                <!-- <div class="d-flex w-100 justify-content-between">
                  <p class="me-3">
                    {{ book.book.title }} - <i>{{ book.book.publisher }}</i>
                  </p>
                  <div>
                    <strong class="me-3">{{ book.sale_price }} ₽</strong>
                    <button class="btn btn-outline-danger">
                      Отменить
                    </button>
                  </div>
                </div> -->
                <div class="d-flex w-100 justify-content-between">
                  <div class="w-85 me-3">
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-1">{{ book.book.title }} <small class="text-muted">- {{ book.book.publisher
                          }}</small></h5>
                      <small>До {{ book.reserve_expiration_datetime }}</small>
                    </div>
                    <div class="d-flex w-100 justify-content-between">
                      <strong class="mb-1">{{ book.sale_price }} ₽</strong>
                      <small class="badge rounded-pill"
                        :style="{ 'background-color': conditionColor(book.condition.degree_of_wear) }">
                        {{book.condition.description }} качество
                      </small>
                    </div>
                  </div>
                  <CartMinusIcon width="38" height="38" class="btn btn-outline-danger" @click="cancelReserveInstance(book.pk)"/>
                </div>
              </a>
            </div>

            <div class="d-grid gap-2 mt-3">
              <button @click="handleLogout" class="btn btn-danger">Выйти</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

import { useAuthStore } from '../stores/authStore.js'
import { useToastStore } from '../stores/toastStore.js'
import CartMinusIcon from '@/components/icons/CartMinusIcon.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()
const username = ref('Пользователь')
const reservedBooks = ref([])

const handleLogout = () => {
  authStore.logout()

  toastStore.addToast({
    'title': 'Успешно',
    'subtitle': '',
    'text': 'Вы успешно вышли из аккаунта',
    'color': 'success',
    'icon': 'check',
  }, 5000)

  window.location.href = '/'
}

const cancelReserveInstance = (pk) => {
  if (authStore.getIsAuth()) {
    fetch('http://127.0.0.1:8000/api/reserved_instances/cancel_reserve/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authStore.getToken()}`
      },
      body: JSON.stringify({
        book_instance_pk: pk,
      })
    }).then(
      (response) => {
        if (response.ok) {
          updateReservedBooks().catch(
            (error) => {
              throw new Error('Failed to update reserved books')
            }
          )
          toastStore.addToast({
            'title': 'Успешно',
            'subtitle': '',
            'text': 'Резерв успешно отменен',
            'color': 'success',
            'icon': 'check',
          }, 5000)
          return
        }
        throw new Error('Failed to cancel reserve book')
      }
    ).catch(
      (error) => {
        console.log(error)
        toastStore.addToast({
          'title': 'Ошибка',
          'subtitle': '',
          'text': 'Ошибка при отмене резерва книги. Попробуйте еще раз',
          'color': 'warning',
          'icon': 'check',
        }, 5000)
      }
    )
  } else {
    toastStore.addToast({
      'title': 'Ошибка',
      'subtitle': '',
      'text': 'Вы должны быть авторизованы, чтобы отменить резерв книги',
      'color': 'warning',
      'icon': 'check',
    }, 5000)
  }
}

const conditionColor = (degree_of_wear) => {
  let color = '#fff'
  switch (degree_of_wear) {
    case 1:
      color = '#2E7D32'
      break
    case 2:
      color = '#81C784'
      break
    case 3:
      color = '#c7b726'
      break
    case 4:
      color = '#FF9800'
      break
    case 5:
      color = '#F44336'
      break
    default:
      color = '#fff'
  }

  return color
}

const updateReservedBooks = async () => {
  const response = await fetch('http://localhost:8000/api/reserved_instances/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + authStore.getToken()
    }
  })
  const data = await response.json()
  reservedBooks.value = data
  console.log(reservedBooks.value)
}

onMounted(async () => {
  username.value = authStore.getUsername()
  await updateReservedBooks()
})

</script>

<style lang="scss" scoped>
.container {
  margin-top: 50px;
}

.w-85 {
  width: 90%;
}

.w-15 {
  width: 10%;
}
</style>
