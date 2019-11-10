<template>
<div>
  <span class="word" v-for="(word, index) in value" :key="`wordlist-${word}-${index}`">
    {{ word }}
  </span>
</div>
</template>

<script>
export default {
  props: {
    value: {
      type: Array,
      default: () => []
    },
  },
}
</script>

<style lang="postcss" scoped>
.word {
  @apply mr-1;
}
</style>