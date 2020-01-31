<template>
<div v-if="!!response">
  <div class="title">Response</div>
  <div class="status__row">
    <div class="status__prompt">Status: </div>
    <div class="status">{{response.status}}</div>
    <div class="code">{{response.code}}</div>
  </div>
  <pre class="body">{{JSON.stringify(JSON.parse(response.body), null, 2)}}</pre>
</div>
</template>

<script>
export default {
  props: {
    response: {
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
  @apply text-sm text-indigo-100 font-medium border-l-4 border-teal-600 pl-3 py-3 bg-gray-800 rounded shadow
}
.title {
  @apply font-bold text-xl text-blue-300 my-2
}
.status__row {
  @apply flex text-teal-400 font-semibold text-base mb-1
}
.status {
  @apply mr-2
}
.status__prompt {
  @apply font-medium text-indigo-300 mr-1
}
</style>