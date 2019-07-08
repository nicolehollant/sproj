<template>
  <div class="home h-full bg-gray-800">
    <header class="w-full p-8 bg-pink-700 shadow-lg flex align-center justify-center items-center">
      <h2 class="text-gray-400 cursor-pointer"><router-link to="/">Home</router-link></h2>
      <h1 class="text-3xl flex-1 font-hairline text-white">Thesaurus</h1>
      <h2 class="opacity-0">Home</h2>
    </header>
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
  },
  data() {
    return {
      response: ""
    }
  },
  methods: {
    fetchData() {
      // fetch()
      console.log("Getting something")
    }
  },
  mounted () {
    this.fetchData();
  },
}
</script>
