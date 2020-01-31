<template>
<div v-if="headers.length > 0">
  <div class="title">Headers</div>
  <div class="table__wrapper">
    <table>
      <tr class="header" v-for="(header, index) in headers" :key="`header-${header.key}-${index}`">
        <td class="key">{{header.key}}</td>
        <td class="value">{{header.value}}</td>
      </tr>
    </table>
  </div>
</div>
</template>

<script>
export default {
  props: {
    headers: {
      type: Array,
      default: () => ([])
    },
  },
}
</script>

<style lang="postcss" scoped>
.title {
  @apply font-bold text-xl text-blue-300 my-2
}
.table__wrapper {
  @apply bg-gray-800 text-indigo-100 py-3 border-l-4 border-purple-600 rounded shadow
}
.header {
  font-family: monospace;
  @apply text-lg
}
.key, .value {
  @apply px-3
}
.key::after {
  content: ":";
  @apply inline-block
}
</style>