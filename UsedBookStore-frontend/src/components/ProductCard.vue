<template>
    <div class="card h-100">
        <RouterLink :to="`/catalog/${props.id}/`" class="text-decoration-none text-body-emphasis ">
            <img :src="props.cover" alt="Тут должна быть облажка книги..." class="card-img-top">
            <div class="card-body " style="--bs-link-hover-color-rgb: 25, 135, 84;" >
                <div class="d-flex justify-content-between">
                  <h5 class="card-title">{{ processedPrice }}</h5>
                  <div class="condition-marker" :style="{'background-color': conditionColor}" @mouseover="showTooltip" @mouseout="hideTooltip">
                    <Tooltip :content="`${props.bestCondition} качество`" :placement="placement" :visible="conditionTooltipVisibility" />
                  </div>
                </div>
                <h6 class="card-text" :class="[{'link-primary': hover}]" @mouseover="hover = true" @mouseleave="hover = false">{{ title }}</h6>
                <p class="card-text d-flex justify-content-between"><small class="text-body-secondary">{{ processedAuthors }}</small><small class="text-body-secondary">{{ count }} в наличии</small></p>
                <p><small></small></p>
            </div>
            <!-- <div>
              <div class="condition-marker" :style="{'background-color': '#2E7D32'}"></div>
              <div class="condition-marker" :style="{'background-color': '#81C784'}"></div>
              <div class="condition-marker" :style="{'background-color': '#c7b726'}"></div>
              <div class="condition-marker" :style="{'background-color': '#FF9800'}"></div>
              <div class="condition-marker" :style="{'background-color': '#F44336'}"></div>
            </div> -->
        </RouterLink>
    </div>
</template>

<script setup>
import {ref, computed, onMounted, watch} from 'vue'
import Tooltip from './Tooltip.vue'

const hover = ref(false)

const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  cover: {
    type: String,
    required: true
  },
  publisher: {
    type: String,
    required: false
  },
  published_year: {
    type: Number,
    required: false
  },
  genres: {
    type: Array,
    required: true
  },
  authors: {
    type: Array,
    required: true
  },
  count: {
    type: Number,
    default: 5,
  },
  degree_of_wear: {
    type: Number,
    required: true
  },
  bestCondition: {
    type: String,
    default: "Идеальное"
  },
  minPrice: {
    type: String,
    required: true
  },
  maxPrice: {
    type: String,
    required: true
  },
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

const conditionColor = ref('#fff')
const processedPrice = computed(() => props.minPrice === props.maxPrice ? `${props.minPrice} ₽` : `${props.minPrice} ₽ - ${props.maxPrice} ₽`)
const processedAuthors = computed(() => props.authors.join(', '))

onMounted(() => {
  hideTooltip()
  if (props.bestCondition) {
    switch (props.degree_of_wear) {
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
    }
  }
})

</script>

<style lang="scss" scoped>
.condition-marker {
  position : relative;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin-left: 10px;
  color: #c7b726;
}

</style>