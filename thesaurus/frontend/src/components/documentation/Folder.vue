<template>
<div class="folder">
  <!-- NOTE: it might be nicer in the future to paginate these and remove the header from the card -->
  <div class="folder__header">
    <div class="name">{{ folder.name }}</div>
    <div class="description">{{ folder.description }}</div>
  </div>
  <DocRequest 
    v-for="(item, index) of folder.item" 
    :key="[folder.name, index].join('-')"
    :request="item"
  />
</div>
</template>

<script>
import DocRequest from './DocRequest.vue'
export default {
  components: {
    DocRequest,
  },
  props: {
    folder: {
      type: Object,
      default: () => ({})
    },
  },
  
}
</script>

<style lang="postcss" scoped>
.folder {
  @apply bg-gray-900 p-4 shadow
}
.folder__header {
  @apply mb-4
}
.name {
  @apply font-bold text-2xl text-purple-300 my-2
}
.description {
  @apply font-medium text-purple-400 text-lg border-l-4 border-blue-500 pl-3
}

@screen sm {
  .folder {
    @apply rounded-lg shadow-xl
  }
}
</style>