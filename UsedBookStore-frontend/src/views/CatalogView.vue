<template>
  <div class="container-xxl" :bs-data-theme="themeStore.theme">
    <h1 class="text-center mb-3">Каталог</h1>
    <div class="row row-cols-4 g-4">
      <div class="col" v-for="(data, index) in products" :key="index">
        <ProductCard v-bind="data" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useThemeStore } from '../stores/theme.js'
import { useToastStore } from '../stores/toastStore.js'
import ProductCard from '../components/ProductCard.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const DEFAULT_COVER = 'http://127.0.0.1:8000/media/covers/default_cover.jpg'

const products = ref([])

onMounted(async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/catalog/')
  products.value = response.data
  for (let i = 0; i < products.value.length; i++) {
    products.value[i].id = products.value[i].pk
    if (products.value[i].cover === null){
      products.value[i].cover = DEFAULT_COVER
    }
  }
})

const themeStore = useThemeStore()
const toastStore = useToastStore()
</script>

<style lang="scss" scoped></style>
