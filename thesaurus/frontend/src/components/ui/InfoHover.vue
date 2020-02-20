<template>
<div class="info__circle" v-on-click-outside="() => active = false">
  <button @click="() => active = !active">
    <fa-icon icon="info-circle" class="info__circle"/>
  </button>
  <div class="info__body" :class="{ 'info__body--active': active }">
    <slot/>
  </div>
</div>
</template>

<script>
export default {
  data: () => ({ active: false })
}
</script>

<style lang="postcss" scoped>
.info__circle {
  @apply inline relative
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