<template>
<div v-if="!!body.raw">
  <div class="title">Body</div>
  <pre class="body">{{JSON.stringify(JSON.parse(body.raw), null, 2)}}</pre>
</div>
</template>

<script>
export default {
  props: {
    body: {
      type: Object,
      default: () => ({})
    },
  },
}
</script>

<style lang="postcss" scoped>
.body {
  max-height: 20rem;
  overflow: scroll;
  @apply text-sm text-indigo-100 font-medium border-l-4 border-blue-600 pl-3 py-3 bg-gray-800 rounded shadow
}
.title {
  @apply font-bold text-xl text-blue-300 my-2
}
</style>