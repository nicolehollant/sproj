<template>
<label :class="$attrs.class">
  <slot/>
  <div
    :class="{ 'bg-secondary-70': value, 'bg-neutral-80': !value }"
    v-on:keydown.space="$emit('input', !value)"
    class="relative block rounded-full w-12 h-6 cursor-pointer border border-neutral-60 focus:outline-none focus:shadow-outline"
    style="transition-duration: 100ms"
    tabindex="0"
  >
    <div 
      :class="{ 'is-active': value }"
      class="w-1/2 h-full left-0 top-0 bg-primary-50 border border-neutral-50 rounded-full"
      style="transition-duration: 150ms"
    />
    <input 
      type="checkbox" 
      class="invisible w-0 h-0 absolute pointer-events-none"
      :value="value" 
      @input="$emit('input', !value)"
    >
  </div>
</label>
</template>

<script>
export default {
  name: "Toggle",
  props: {
    value: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style lang="postcss" scoped>
.is-active {
  transform: translateX(100%);
}
</style>