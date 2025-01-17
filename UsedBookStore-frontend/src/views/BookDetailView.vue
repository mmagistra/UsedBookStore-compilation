<template>
    <div class="container-xxl">
        <div class="card mb-3">
            <div class="row g-0">
                <div class="col-md-4">
                    <img :src="product.cover" alt="Тут должна быть облажка книги..." class="card-img-top">
                </div>
                <div class="card-body col-md-8">
                    <h5 class="card-title">{{ product.title }}</h5>
                    <h6 class="card-text" v-if="!showFullDescription" v-html="product.short_description"></h6>
                    <h6 class="card-text" v-else v-html="product.description"></h6>
                    <button @click="showFullDescription = !showFullDescription"
                        class="btn btn-link ps-0 text-decoration-none card-text"
                        v-if="product.short_description_exists">Показать/Скрыть</button>
                    <div class="mb-2">
                        <span class="badge text-bg-primary me-1">Жанры:</span>
                        <span v-for="(genre, index) in product.genres" :key="index"
                            class="badge text-bg-secondary me-1">{{ genre }}</span>
                    </div>
                    <div class="mb-2">
                        <span class="badge rounded-pill text-bg-primary me-1">Авторы:</span>
                        <span v-for="(author, index) in product.authors" :key="index"
                            class="badge rounded-pill text-bg-secondary me-1">{{ author }}</span>
                    </div>
                    <div class="mb-2">
                        <span class="badge rounded-pill text-bg-primary me-1">Издательство:</span>
                        <span class="badge rounded-pill text-bg-secondary me-1">{{ product.publisher }}</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row row-cols-1 row-cols-xl-5 g-4">
            <div class="col" v-for="(instance, index) in instanceGroupsByCondition" :key="index">
                <GroupBookInstances v-bind="instance" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

import GroupBookInstances from '../components/GroupBookInstances.vue'

const showFullDescription = ref(false)

const route = useRoute()
const book_id = ref(route.params.book_id)
const product = ref({})
const instanceGroupsByCondition = ref({})
const CONDITION_COUNT = 5

onMounted(async () => {
    const response = await axios.get(`http://127.0.0.1:8000/api/catalog/${book_id.value}/`)

    product.value = response.data
    product.value.description = product.value.description.replace(/\n/g, '<br>')
    if (product.value.description.length > 800) {
        product.value.short_description = product.value.description.slice(0, 800) + '...'
        product.value.short_description_exists = ref(true)
    }
    else {
        product.value.short_description = product.value.description
        product.value.short_description_exists = ref(false)
    }

    const condition_response = await axios.get(`http://127.0.0.1:8000/api/conditions/`)

    const conditions_data = condition_response.data
    let conditions = []

    for (let i = 0; i < conditions_data.length; i++) {
        conditions[i] = {
            degree_of_wear: conditions_data[i].degree_of_wear,
            description: conditions_data[i].description
        }
    }

    // Instabce groups
    for (let i = 0; i < CONDITION_COUNT; i++) {
        let cur_instances = product.value.instances.filter(
            instance => instance.condition.degree_of_wear === (i + 1) & (instance.status === 'in_stock' || instance.status === 'reserved')
        )
        let minPrice = Math.min(...cur_instances.map(instance => instance.sale_price))
        minPrice = minPrice === Infinity ? 0 : minPrice
        let maxPrice = Math.max(...cur_instances.map(instance => instance.sale_price))
        maxPrice = maxPrice === -Infinity ? 0 : maxPrice
        let in_stock = cur_instances.filter(instance => instance.status === 'in_stock').length
        let reserved = cur_instances.filter(instance => instance.status === 'reserved').length
        instanceGroupsByCondition.value[i] = {
            condition: conditions[i].degree_of_wear,
            condition_description: conditions[i].description,
            minPrice: minPrice,
            maxPrice: maxPrice,
            in_stock: in_stock,
            reserved: reserved,
            instances: cur_instances,
        }
    }

})

</script>

<style lang="scss" scoped></style>