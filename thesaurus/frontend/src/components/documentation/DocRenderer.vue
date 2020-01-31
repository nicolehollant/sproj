<template>
<div class="docs">
  <div>
    <div class="docs__header">
      <div class="docs__header--title">{{ envdocs.info.name }}</div>
      <div class="docs__header--description">{{ docs.info.description }}</div>
    </div>
    <Folder 
      v-for="item in envdocs.item" 
      :key="item.name" 
      :folder="item"
      class="docs__folder"
    />
  </div>
</div>
</template>

<script>
import Folder from './Folder.vue'
export default {
  components: {
    Folder,
  },
  props: {
    docs: {
      type: Object,
      default: () => ({ message: "oops" })
    },
  },
  computed: {
    envdocs() {
      // const env = {
      //   '{{thesaurus-base}}': 'https://sproj.api.colehollant.com/api/v1/'
      // }

      return JSON.parse(
        JSON.stringify(this.docs).replace(/{{thesaurus-base}}/g,'https://sproj.api.colehollant.com/thesaurus/api/v1')
      )
    }
  },
}
</script>

<style lang="postcss" scoped>
.docs {
  @apply leading-relaxed text-lg font-medium max-w-4xl mb-10 mx-auto text-left text-pink-200
}
.docs__header {
  @apply mx-4 my-8
}
.docs__folder {
  @apply my-2
}
.docs__header--description {
  @apply font-semibold text-lg text-purple-300 my-2
}
.docs__header--title {
  @apply font-bold text-2xl text-indigo-200 mt-4 mb-2 uppercase;
}
@screen sm {
  .docs {
    @apply p-4
  }
  .docs__folder {
    @apply my-8
  }
  .docs__header {
    @apply mx-0
  }
  .docs__header--description {
    @apply font-bold text-2xl
  }
  .docs__header--title {
    @apply font-black text-3xl mt-8;
  }
}
</style>