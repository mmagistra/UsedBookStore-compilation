<template>
    <div>
        <div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <h3 class="card-text"> Стоимость: {{ props.sale_price }} ₽</h3>
                    <div class="condition-marker" :style="{ 'background-color': conditionColor }"
                        @mouseover="showTooltip" @mouseout="hideTooltip">
                        <Tooltip :content="`${props.condition.description} качество`" :placement="placement"
                            :visible="conditionTooltipVisibility" />
                    </div>
                </div>
                <div class="d-flex justify-content-between flex-column">
                    <small class="text-body-secondary">6 в наличии</small>
                    <small class="text-body-secondary">1 зарезервировано</small>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

import Tooltip from './Tooltip.vue'

const props = defineProps ({
  pk: {
    type: Number,
    required: true
  },
  condition: {
    type: Object,
    required: true
  },
  storage_cell: {
    type: String,
    required: true
  },
  purchase_price: {
    type: String,
    required: true
  },
  sale_price: {
    type: String,
    required: true
  },
  status: {
    type: String,
    required: true
  }
})

const conditionColor = ref('#fff')


onMounted(() => {

    console.log(props)
    
    // Condition color
    hideTooltip()
    if (props.condition) {
        switch (props.condition.degree_of_wear) {
        case 1:
            conditionColor.value = '#2E7D32'
            break
        case 2:
            conditionColor.value = '#81C784'
            break
        case 3:
            conditionColor.value = '#FFEB3B'
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
  position : absolute;
  top: -1px;
  right: -1px;
  max-width: 15%;
  max-height: 102%;
  min-width: 15%;
  min-height: 102%;
  border-radius: 0% 6px 6px 0%;
  margin-left: 10px;
  border: 1px solid v-bind(conditionColor);
}
</style>