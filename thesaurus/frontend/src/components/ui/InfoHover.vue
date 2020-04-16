<template>
<div class="info__circle" v-on-click-outside="() => active = false" :class="{
      'w-4 h-4': size === '1',
      'w-5 h-5': size === '2',
      'w-6 h-6': size === '3',
      'w-8 h-8': size === '4',
      'w-10 h-10': size === '5',
      'w-12 h-12': size === '6',
    }">
  <button 
    aria-label="toggle info box"
    @click="() => active = !active" 
    class="focus:outline-none focus:shadow-outline rounded-full"
  >
    <fa-icon icon="info-circle" class="info__circle"/>
  </button>
  <div class="info__body" :class="{ 'info__body--active': active }">
    <slot/>
  </div>
</div>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      validator: (a) => ['1', '2', '3', '4', '5', '6'].includes(a)
    }
  },
  data: () => ({ active: false })
}
</script>

<style lang="postcss" scoped>
.info__circle {
  @apply block relative
}
.info__body {
  text-transform: none;
  max-width: 20rem;
  width: max-content;
  min-width: 8rem;
  @apply absolute hidden left-0 rounded-lg border-2 border-indigo-800 bg-gray-900 text-base py-2 px-3 shadow-xl z-20
}
.info__body--active, .info__circle:hover .info__body {
  @apply block
}
</style>