<template>
    <div class="toast-group">
        <div v-for="(toast, index) in toasts.value">
            <Toast v-bind="toast" :key="toast.id" :bottom="getBottomPosition(index)"/>
        </div>
        <!-- <Toast v-for="(toast, index) in toasts.value" :key="index" v-bind="toast" :bottom="getBottomPosition(index)" /> -->
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

import { useToastStore } from '../stores/toastStore.js'
import Toast from './Toast.vue'

const toastStore = useToastStore()
const toasts = toastStore.getToasts()

const toastHeights = ref([])

const getBottomPosition = computed(() => (index) => {
    let bottomPosition = 0
    for (let i = 0; i < index; i++) {
        bottomPosition += toastHeights.value[i] + 10
    }
    return bottomPosition
})

watch(toastStore, () => {
    toasts.value = toastStore.getToasts()
    updateToastHeights()
})

const updateToastHeights = () => {
    const toastElements = document.querySelectorAll('.my-toast')
    toastHeights.value = []
    for (const toastElement of toastElements) {
        toastHeights.value.push(toastElement.offsetHeight)
        // toastHeights.value.push(100)
    }
}

const renderToasts = () => {
    toasts.value = toastStore.getToasts()
    updateToastHeights()
}
onMounted(() => {
    toastStore.uploadToasts()
    updateToastHeights()
    window.addEventListener('resize', updateToastHeights)
})
</script>

<style scoped>
.toast-group {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    display: flex;
    flex-direction: column-reverse;
    gap: 0.5rem;
}

.toast {
    margin-bottom: 0.5rem;
}
</style>
