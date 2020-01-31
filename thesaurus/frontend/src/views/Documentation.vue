<template>
<div class="docs">
  <Navbar />
  <DocRenderer :docs="docs" />
</div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import DocRenderer from '@/components/documentation/DocRenderer.vue'

export default {
  components: {
    Navbar,
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