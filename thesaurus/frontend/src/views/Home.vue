<template>
  <div class="flex flex-col sm:flex-row h-screen">
    <div class="border-t-4 border-primary-50 shadow-lg sm:shadow-none sm:border-none py-4 sm:py-0 sm:w-3/5 text-left flex flex-shrink-0 bg-primary-90 sm:bg-neutral-90">
      <div class="my-auto mx-6 grid gap-4">
        <h1 class="text-3xl sm:text-5xl text-secondary-20 font-bold">
          Welcome
        </h1>
        <p class="hidden sm:block text-2xl">
          There's some stuff to see :)
        </p>
      </div>
    </div>
    <div class="flex-1 sm:bg-primary-90 flex items-start mt-4 sm:mt-0 sm:items-center">
      <nav class="grid gap-2 w-full">
        <router-link 
          aria-label="Home" 
          exact 
          to="/"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Home
        </router-link>
        <router-link 
          aria-label="Thesaurus" 
          to="/thesaurus"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Thesaurus
        </router-link>
        <router-link 
          aria-label="Model" 
          to="/model"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Model
        </router-link>
        <router-link 
          aria-label="Writing" 
          to="/writing"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Writing
        </router-link>
        <router-link 
          aria-label="Docs" 
          to="/docs"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Docs
        </router-link>
        <router-link 
          aria-label="midway" 
          to="/midway"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Midway
        </router-link>
        <a 
          href="https://github.com/colehollant/sproj"
          class="home-navlink text-2xl hover:bg-primary-80 py-3"
        >
          Github
        </a>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',  
}
</script>

<style lang="postcss" scoped>
.home-navlink {
  transition-duration: 150ms;
  @apply cursor-pointer text-primary-20 px-1 rounded;
}
.home-navlink:focus {
  @apply outline-none bg-primary-80 text-secondary-10
}
.router-link-active{
  @apply text-secondary-20 font-semibold;
}
</style>
