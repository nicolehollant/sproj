<template>
<div class="docs">
  <DocRenderer :docs="docs" />
</div>
</template>

<script>
import DocRenderer from '@/components/documentation/DocRenderer.vue'

export default {
  components: {
    DocRenderer
  },
  data() {
    return {
      docs: require('@/assets/documentation/docs.json')
    }
  },
}
</script>

<style lang="postcss" scoped>

</style>