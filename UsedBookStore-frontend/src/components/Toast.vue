<template>
    <div class="my-toast card p-0" :class="{ 'my-toast--visible': visible }" :style="positionStyle">
        <!-- <component :is="icon" class="toast__icon" /> -->
        <div class="card-header d-flex justify-content-between">
            <h5 class="toast__title m-0">{{  title }}</h5>
            <button type="button" class="btn-close" @click="closeToast" aria-label="Close"></button>
        </div>
        <div class="toast__content card-body">
            <p class="toast__text m-0">{{ text }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import { useToastStore } from '../stores/toastStore.js'

const props = defineProps({
    id: {
        type: Number,
        required: true
    },
    color: {
        type: String,
        required: true
    },
    icon: {
        type: [Object, String],
        required: false
    },
    title: {
        type: String,
        required: true
    },
    subtitle: {
        type: String,
        required: true
    },
    text: {
        type: String,
        required: true
    },
    left: {
        type: Number,
        required: false
    },
    right: {
        type: Number,
        required: false
    },
    top: {
        type: Number,
        required: false
    },
    bottom: {
        type: Number,
        required: false
    },
    position: {
        type: String,
        default: 'bottom-right'
    },
    timeToClose: {
        type: Number,
        required: false
    },
})

const visible = ref(true)
const borderColor = ref('')
const bodyColor = ref('')

const toastStore = useToastStore()

const positionStyle = computed(() => {
    const positions = {
        'top-left': {
            top: props.top !== undefined ? `${props.top}px` : '1rem',
            left: props.left !== undefined ? `${props.left}px` : '1rem'
        },
        'top-center': {
            top: props.top !== undefined ? `${props.top}px` : '1rem',
            left: '50%',
            transform: 'translateX(-50%)'
        },
        'top-right': {
            top: props.top !== undefined ? `${props.top}px` : '1rem',
            right: props.right !== undefined ? `${props.right}px` : '1rem'
        },
        'middle-left': {
            top: '50%',
            left: props.left !== undefined ? `${props.left}px` : '1rem',
            transform: 'translateY(-50%)'
        },
        'middle-center': {
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)'
        },
        'middle-right': {
            top: '50%',
            right: props.right !== undefined ? `${props.right}px` : '1rem',
            transform: 'translateY(-50%)'
        },
        'bottom-left': {
            bottom: props.bottom !== undefined ? `${props.bottom}px` : '1rem',
            left: props.left !== undefined ? `${props.left}px` : '1rem'
        },
        'bottom-center': {
            bottom: props.bottom !== undefined ? `${props.bottom}px` : '1rem',
            left: '50%',
            transform: 'translateX(-50%)'
        },
        'bottom-right': {
            bottom: props.bottom !== undefined ? `${props.bottom}px` : '1rem',
            right: props.right !== undefined ? `${props.right}px` : '1rem'
        }
    }
    return positions[props.position]
})

const closeToast = () => {
    visible.value = false
    setTimeout(() => {
        toastStore.removeToast(props.id)
    }, 500)
}

onMounted(() => {
    borderColor.value = `var(--bs-${props.color}-border-subtle)`
    bodyColor.value = `var(--bs-${props.color})`

    if (props.timeToClose) {
        setTimeout(() => {
            closeToast()
        }, props.timeToClose)
    }
})
</script>

<style lang="scss" scoped>
.my-toast {
    position: fixed;
    min-width: 400px;
    max-width: 50%;
    // background-color: v-bind(bodyColor);
    color: v-bind(bodyColor);
    border: 3px solid v-bind(borderColor);
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    opacity: 0%;
    transition: opacity 0.3s ease-in-out;

    &--visible {
        opacity: 80%;
    }

    &__icon {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
    }

    &__content {
        display: block;
        // display: flex;
        // flex-direction: column;
    }

    &__title {
        margin-bottom: 0.25rem;
    }

    &__subtitle {
        margin-bottom: 0.5rem;
    }
}
</style>

