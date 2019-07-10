<template>
  <div class="home h-full">
    <Navbar/>
    <ThesaurusEntry word="cool"/>
  </div>
</template>

<script>
import ThesaurusEntry from '@/components/ThesaurusEntry.vue'
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'home',
  components: {
    Navbar,
    ThesaurusEntry
  },
}
</script>
