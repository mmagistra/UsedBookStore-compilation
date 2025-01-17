<template>
    <div class="tooltip" :class="{ tooltipVisible: props.visible, [props.placement]: true }">
        <div>{{ props.content }}</div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    placement: {
        type: String,
        default: 'top'
    },
    visible: {
        type: Boolean,
        required: true
    },
    content: {
        type: String,
        required: true,
    },
})

</script>

<style lang="scss" scoped>
.tooltip {
  text-align: center;
  position: absolute;
  z-index: 1;
  background-color: var(--bs-body-bg);
  border: 1px solid var(--bs-secondary-bg);
  border-radius: 10px;
  padding: 10px;
  display: none;
}

.tooltip.tooltipVisible {
  display: block;
  opacity: 1;
}

.tooltip.bottom {
  margin-top: 10px;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.tooltip.top {
  margin-bottom: 10px;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.tooltip.right {
  margin-left: 10px;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
}

.tooltip.left {
  margin-right: 10px;
  top: 50%;
  right: 100%;
  transform: translateY(-50%);
}
</style>