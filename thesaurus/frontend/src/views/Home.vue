<template>
  <div class="home text-pink-200">
    <Navbar/>
    <div class="px-6 py-4 text-left max-w-3xl m-auto">
      <h1 class="font-bold text-2xl text-purple-100 mt-4 mb-6 text-center">MY SPROJ!!</h1>
      <h2>Welcome!</h2>
      <p>This is some home page for my sproj for now. It's gonna get scrapped eventually, but I need a place to start, and well... you've found it :)</p>
      <h2>What's all this then?</h2>
      <p>Currently it's next to nothing! But I have a <router-link to="/thesaurus" class="text-pink-400">thesaurus</router-link> that's (hopefully) up and running</p>
      <h2>What's the goal?</h2>
      <p>I'm tryna build a model to shift the tone of a body of text. And hopefully that's mathy enough to stamp it on a degree or something</p>
      <h2>What's to come?</h2>
      <p>Well, I sure hope I put in an actual model that does something. Other than that? I suppose I'll eventually put up my writing and some auxiliary garbage</p>
      <p>But, regardless, I hope you enjoy :-)</p>
      <h2>Not Navbar Worthy</h2>
      <p>I don't want to clutter my navbar with garbage that I don't much care about, so here are some side bits</p>
      <nav>
        <li><router-link to="/midway" class="text-pink-400">midway presentation</router-link></li>
        <li><a href="https://github.com/colehollant/sproj" class="text-pink-400">github</a></li>
      </nav>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'home',
  components: {
    Navbar
  }
  
}
</script>

<style lang="postcss" scoped>
h2{
  @apply font-bold text-xl text-purple-300 mt-5 mb-1;
}
p{
  @apply text-lg;
}
nav {
  @apply text-lg mt-2;
}
</style>
