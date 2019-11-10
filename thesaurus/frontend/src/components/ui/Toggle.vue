<template>
<div class="switch-wrapper">
  <slot/>
  <label for="switch" class="switch-label" :class="{'active': value}">
    <div class="switch-button"></div>
  </label>
  <input type="checkbox" class="switch" name="switch" id="switch" :value="value" @input="$emit('input', !value)">
</div>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style lang="postcss" scoped>
.switch {
  visibility: hidden;
  width: 0;
  height: 0;
  position: absolute;
  pointer-events: none;
}
.switch-label {
  transition: 0.2s ease;
  @apply relative block rounded-full w-12 h-6 bg-gray-800 border-2 border-gray-700 cursor-pointer;
}
.switch-button {
  width: 50%;
  transition: 0.2s ease;
  @apply absolute left-0 top-0 block h-full bg-pink-500 rounded-full;
}
.switch-label.active {
  @apply bg-purple-800;
}
.switch-label.active .switch-button {
  transform: translateX(100%);
}
</style>