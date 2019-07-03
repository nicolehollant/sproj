<template>
  <div class="home">
    <ThesaurusEntry word="cool"/>
  </div>
</template>

<script>
// @ is an alias to /src
import ThesaurusEntry from '@/components/ThesaurusEntry.vue'

export default {
  name: 'home',
  components: {
    ThesaurusEntry
  }
}
</script>
