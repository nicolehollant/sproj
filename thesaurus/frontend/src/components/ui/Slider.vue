<template>
<div class="slider-wrapper">
  <slot/>
  <input 
    type="range" 
    class="slider" 
    name="slider" 
    id="slider" 
    :min="min" 
    :max="max" 
    :step="step" 
    v-model="val" 
    @input="$emit('input', val)"
  >
</div>
</template>

<script>
export default {
  data() {
    return {
      val: null
    }
  },
  props: {
    min: {
      type: null,
      default: 0
    },
    max: {
      type: null,
      default: 100
    },
    step: {
      type: null,
      default: 1
    },
    value: {
      type: null,
      default: 50
    },
  },
  mounted () {
    this.val = this.value;
  },
}
</script>

<style lang="postcss" scoped>
.slider {
  -webkit-appearance: none;
  appearance: none;
  opacity: 0.8;
  transition: opacity .3s ease;
  @apply block outline-none w-full h-2 bg-purple-800 my-2 rounded;
}
.slider:hover {
  opacity: 1;
}
.thumb {
  @apply w-3 h-3 bg-pink-500 rounded-full cursor-pointer;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  @apply thumb;
}
.slider::-moz-range-thumb {
  @apply thumb;
}
.slider::-webkit-slider-thumb:hover {
  @apply bg-pink-300;
}
.slider::-moz-range-thumb:hover {
  @apply bg-pink-300;
}
</style>