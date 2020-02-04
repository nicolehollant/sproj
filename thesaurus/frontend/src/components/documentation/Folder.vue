<template>
<div class="folder">
  <!-- NOTE: it might be nicer in the future to paginate these and remove the header from the card -->
  <div class="folder__header">
    <div class="name">{{ folder.name }}</div>
    <!-- <div class="description">{{ folder.description }}</div> -->
    <div class="description" v-html="description"></div>
  </div>
  <DocRequest 
    v-for="(item, index) of folder.item" 
    :key="[folder.name, index].join('-')"
    :request="item"
    :id="`request-${item.name}`"
  />
</div>
</template>

<script>
import md from 'markdown-it'
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
  computed: {
    description() {
      return md().render(this.folder.description);
    }
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
.description >>> code {
  @apply text-blue-200
}
.description >>> pre {
  background: #00000030;
  width: max-content;
  max-width: 100%;
  overflow: auto;
  @apply text-sm leading-tight my-2 -ml-3 py-1 pl-4 pr-8 rounded-lg shadow
}
.description >>> pre code {
  @apply text-teal-300
}

@screen md {
  .folder {
    @apply rounded-lg shadow-xl
  }
}
</style>