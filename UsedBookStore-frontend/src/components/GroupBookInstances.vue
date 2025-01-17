<template>
  <div>
    <div class="card" v-if="displayMode === 'short'">
      <div class="card-header" @click="changeDisplayMode">
        <div class="condition-marker" @mouseover="showTooltip" @mouseout="hideTooltip">
          <Tooltip :content="`${props.condition_description} качество`" :placement="placement"
            :visible="conditionTooltipVisibility" />
          <h5 class="condition-marker-text">{{ props.condition_description }}</h5>
        </div>
        <div class="condition-marker-placeholder"></div>
      </div>
      <div class="card-body">
        <div class="d-flex justify-content-between">
          <h5 class="card-text m-0">{{ sale_price }}</h5>
          <CaretDownIcon width="25" height="25" class="" @mouseover="showTooltip" @click="changeDisplayMode"
            @mouseout="hideTooltip" />
        </div>
      </div>
      <div class="d-flex justify-content-between flex-column text-body-secondary card-footer">
        <small>{{ props.in_stock }} в наличии</small>
        <small>{{ props.reserved }} зарезервировано</small>
      </div>
      <div class="card-footer py-0" @click="changeDisplayMode">
        <div class="condition-marker-footer " :style="{ 'background-color': conditionColor }" @mouseover="showTooltip"
          @mouseout="hideTooltip">
        </div>
        <div class="condition-marker-footer-placeholder"></div>
      </div>
    </div>
  </div>

  <div class="card" v-if="displayMode === 'full'">
    <div class="card-header" @click="changeDisplayMode">
      <div class="condition-marker" @mouseover="showTooltip" @mouseout="hideTooltip">
        <Tooltip :content="`${props.condition_description} качество`" :placement="placement"
          :visible="conditionTooltipVisibility" />
        <h5 class="condition-marker-text">{{ props.condition_description }}</h5>
      </div>
      <div class="condition-marker-placeholder"></div>
    </div>
    <div class="card-header d-flex justify-content-between pb-0">
      <h5>В наличии</h5>
      <CaretDownIcon class="condition-marker-icon-downward" width="25" height="25" @click="changeDisplayMode" />
    </div>
    <div class="card-body g-4 pb-0">
      <div v-if="inStockInstances.length === 0">
        <h5 class="text-body-secondary">Нет в наличии</h5>
      </div>
      <div v-else>
        <div v-for="instance, index in inStockInstances" :key="index">
          <div v-if="index < inStockInstances.length - 1" class="d-flex justify-content-between">
            <h5>{{ instance.sale_price }} ₽</h5>
            <button class="btn p-0 mx-0 submit" v-if="!(reservedInstancesByUser.includes(instance.pk))"
              @click="reserveInstance(instance.pk)">
              <CartPlusIcon width="25" height="25" class="cart-icon" />
            </button>
            <button class="btn p-0 mx-0 cancel" v-else @click="cancelReserveInstance(instance.pk)">
              <CartMinusIcon width="25" height="25" class="cart-icon" />
            </button>
          </div>
          <div v-if="index >= inStockInstances.length - 1" class="d-flex justify-content-between mb-0">
            <h5>{{ instance.sale_price }} ₽</h5>
            <button class="btn p-0 mx-0">
              <CartPlusIcon v-if="!(reservedInstancesByUser.includes(instance.pk))" width="25" height="25"
                class="cart-icon submit" @click="reserveInstance(instance.pk)" />
              <CartMinusIcon v-else width="25" height="25" class="cart-icon cancel"
                @click="cancelReserveInstance(instance.pk)" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-header pb-0">
      <h5>Зарезервировано</h5>
    </div>
    <div class="card-body">
      <div v-if="reservedInstances.length === 0">
        <h5 class="text-body-secondary">Нет в резерве</h5>
      </div>
      <div v-for="instance, index in reservedInstances" :key="index">
        <h5 v-if="index < reservedInstances.length - 1" class="d-flex justify-content-between">
          {{ instance.sale_price }} ₽
          <button class="btn p-0 mx-0">
            <CartMinusIcon v-if="reservedInstancesByUser.includes(instance.pk)" width="25" height="25"
              class="cart-icon cancel" @click="cancelReserveInstance(instance.pk)" />
          </button>
        </h5>
        <h5 v-else class="mb-0 d-flex justify-content-between">
          <div>
            {{ instance.sale_price }} ₽
          </div>
          <button class="btn p-0 mx-0">
            <CartMinusIcon v-if="reservedInstancesByUser.includes(instance.pk)" width="25" height="25"
              class="cart-icon cancel" @click="cancelReserveInstance(instance.pk)" />
          </button>
        </h5>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';

import CartPlusIcon from './icons/CartPlusIcon.vue'
import CartMinusIcon from './icons/CartMinusIcon.vue'
import CaretDownIcon from './icons/CaretDownIcon.vue'

import Tooltip from './Tooltip.vue'

import { useAuthStore } from '@/stores/authStore';
import { useToastStore } from '@/stores/toastStore';

const props = defineProps({
  condition: {
    type: Number,
    required: true
  },
  condition_description: {
    type: String,
    required: true
  },
  minPrice: {
    type: Number,
    required: true
  },
  maxPrice: {
    type: Number,
    required: true
  },
  in_stock: {
    type: Number,
    required: true
  },
  reserved: {
    type: Number,
    required: true
  },
  instances: {
    type: Array,
    required: true
  }
})

const conditionColor = ref('#fff')
const sale_price = ref('')
const displayMode = ref('short')
const allInstances = ref([])
const inStockInstances = ref([])
const reservedInstances = ref([])
const reservedInstancesByUser = ref([])

watch(reservedInstancesByUser, (newValue) => {
  // Обновить часть шаблона при изменении reservedInstancesByUser
})

const authStore = useAuthStore()
const isAuth = ref(authStore.getIsAuth())

const toastStore = useToastStore()

const changeDisplayMode = () => {
  displayMode.value = displayMode.value === 'short' ? 'full' : 'short'
}

const reserveInstance = (pk) => {
  if (isAuth.value) {
    fetch('http://127.0.0.1:8000/api/reserved_instances/reserve/', {
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
          // Add instance pk to reservedInstancesByUser
          reservedInstancesByUser.value.push(pk)

          // Update instance status
          for (let i = 0; i < allInstances.value.length; i++) {
            if (allInstances.value[i].pk === pk) {
              allInstances.value[i].status = 'reserved'
            }
          }

          // Update inStockInstances and reservedInstances
          inStockInstances.value = []
          reservedInstances.value = []
          for (let i = 0; i < allInstances.value.length; i++) {
            if (allInstances.value[i].status === 'reserved') {
              reservedInstances.value.push(allInstances.value[i])
            }
            else if (allInstances.value[i].status === 'in_stock') {
              inStockInstances.value.push(allInstances.value[i])
            }
          }
          toastStore.addToast({
            'title': 'Успешно',
            'subtitle': '',
            'text': 'Книга успешно зарезервирована',
            'color': 'success',
            'icon': 'check',
          }, 5000)
          return
        }
        throw new Error('Failed to reserve book')
      }
    ).catch(
      (error) => {
        console.log(error)
        toastStore.addToast({
          'title': 'Ошибка',
          'subtitle': '',
          'text': 'Произошла ошибка при резервировании книги. Попробуйте еще раз',
          'color': 'danger',
          'icon': 'check',
        }, 5000)
      }
    )
  } else {
    toastStore.addToast({
      'title': 'Ошибка',
      'subtitle': '',
      'text': 'Вы должны быть авторизованы, чтобы зарезервировать книгу',
      'color': 'warning',
      'icon': 'check',
    }, 5000)
  }
}

const cancelReserveInstance = (pk) => {
  if (isAuth.value) {
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
          // Remove instance pk from reservedInstancesByUser
          reservedInstancesByUser.value = reservedInstancesByUser.value.filter(instance => instance !== pk)

          // Update instance status
          for (let i = 0; i < allInstances.value.length; i++) {
            if (allInstances.value[i].pk === pk) {
              allInstances.value[i].status = 'in_stock'
            }
          }

          // Update inStockInstances and reservedInstances
          inStockInstances.value = []
          reservedInstances.value = []
          for (let i = 0; i < allInstances.value.length; i++) {
            if (allInstances.value[i].status === 'reserved') {
              reservedInstances.value.push(allInstances.value[i])
            }
            else if (allInstances.value[i].status === 'in_stock') {
              inStockInstances.value.push(allInstances.value[i])
            }
          }
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

onMounted(() => {
  fetch('http://127.0.0.1:8000/api/reserved_instances/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${authStore.getToken()}`
    }
  }).then(
    (response) => {
      if (response.ok) {
        return response.json()
      }
      throw new Error('Failed to get user reserved books')
    }
  ).then(
    (data) => {
      reservedInstancesByUser.value = []
      for (let i = 0; i < data.length; i++) {
        reservedInstancesByUser.value.push(data[i].pk)
      }
    }
  ).catch(
    (error) => {
      console.log(error)
    }
  )

  allInstances.value = props.instances

  sale_price.value = props.minPrice === props.maxPrice ? `${props.minPrice} ₽` : `${props.minPrice} ₽ - ${props.maxPrice} ₽`

  inStockInstances.value = allInstances.value.filter(instance => instance.status === 'in_stock')
  reservedInstances.value = allInstances.value.filter(instance => instance.status === 'reserved')

  if ((inStockInstances.value.length + reservedInstances.value.length) === 0) {
    sale_price.value = 'Нет экземпляров'
  }

  // Condition color
  hideTooltip()
  if (props.condition_description) {
    switch (props.condition) {
      case 1:
        conditionColor.value = '#2E7D32'
        break
      case 2:
        conditionColor.value = '#81C784'
        break
      case 3:
        conditionColor.value = '#c7b726'
        break
      case 4:
        conditionColor.value = '#FF9800'
        break
      case 5:
        conditionColor.value = '#F44336'
        break
      default:
        conditionColor.value = '#fff'
        console.log(conditionColor.value)
    }
  }
})

// Condition tooltip
const placement = ref('top')
const conditionTooltipVisibility = ref(false)
const showTooltip = () => {
  conditionTooltipVisibility.value = true
}
const hideTooltip = () => {
  conditionTooltipVisibility.value = false
}
</script>

<style lang="scss" scoped>
.card {
  border-color: v-bind(conditionColor);
  color: v-bind(conditionColor);
}

.condition-marker {
  // background
  background-color: v-bind(conditionColor);
  position: absolute;
  top: -1px;
  right: -1px;
  max-width: calc(100% + 2px);
  max-height: 47px;
  min-width: calc(100% + 2px);
  min-height: 47px;
  border-radius: 6px 6px 0 0%;
  border: 1px solid v-bind(conditionColor);
}

.condition-marker-icon-downward {
  position: relative;
  transform: scaleY(-1);
  top: -5px;
}

.condition-marker-footer {
  // background
  position: absolute;
  bottom: -1px;
  right: -1px;
  max-width: calc(100% + 2px);
  max-height: 22px;
  min-width: calc(100% + 2px);
  min-height: 22px;
  border-radius: 0 0% 6px 6px;
  border: 1px solid v-bind(conditionColor);
}

.condition-marker-footer-placeholder {
  bottom: -1px;
  right: -1px;
  max-width: calc(100% + 2px);
  max-height: 20px;
  min-width: calc(100% + 2px);
  min-height: 20px;
  border-radius: 0 0% 6px 6px;

  // text
  text-align: center;
  text-decoration-color: white;
  z-index: 1;
}

.condition-marker-text {
  // text
  margin: 10px auto 10px auto;
  text-align: center;
  text-decoration-color: white;
  text-emphasis-color: white;
  color: white;
  z-index: 1;
}

.condition-marker-placeholder {
  top: -1px;
  right: -1px;
  max-width: calc(100% + 2px);
  max-height: 30px;
  min-width: calc(100% + 2px);
  min-height: 30px;
  border-radius: 6px 6px 0 0%;

  // text
  text-align: center;
  text-decoration-color: white;
  z-index: 1;
}

.submit:hover {
  color: green;
}

.cancel:hover {
  color: red;
}

.cart-icon {
  position: relative;
  top: -6px
}

.btn {
  border: none;
}
</style>