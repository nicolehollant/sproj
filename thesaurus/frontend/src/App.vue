<template>
  <div id="app" :class="theme">
    <router-view/>
    <button aria-label="toggle dark mode" @click="toggleTheme" class="fixed bottom-0 right-0 m-4 w-10 h-10 rounded-full shadow-xl text-primary-10 bg-primary-90 focus:outline-none focus:shadow-outline">
      <fa-icon :icon="theme === 'light' ? 'sun' : 'moon'" />
    </button>
  </div>
</template>

<script>
import { ref, onMounted } from '@vue/composition-api'
export default {
  name: "App",
  setup() {
    const theme = ref('light')
    function applyBodyColor() {
      document.bgColor = theme.value === 'light' ? '#fdcbe5' : '#362533'
      document.body.style.backgroundColor = theme.value === 'light' ? '#fdcbe5' : '#362533'
    }
    function toggleTheme() {
      theme.value = theme.value === 'light' ? 'dark' : 'light'
      applyBodyColor()
    }
    onMounted(applyBodyColor)
    return { theme, toggleTheme }
  }
}
</script>

<style lang='postcss'>
.light {
  --text-color: #362533e0;
  --neutral-90: #fdcbe5;
  --neutral-80: #c9abd8;
  --neutral-70: #b594c1;
  --neutral-60: #a17eaa;
  --neutral-50: #8d6a93;
  --neutral-40: #79577b;
  --neutral-30: #644664;
  --neutral-20: #4d354b;
  --neutral-10: #362533;

  --primary-90: #fff0f3;
  --primary-80: #fed1dd;
  --primary-70: #fcb2ca;
  --primary-60: #f691b8;
  --primary-50: #ed70a8;
  --primary-40: #de4e98;
  --primary-30: #c62f86;
  --primary-20: #a1136d;
  --primary-10: #70004f;

  --secondary-90: #e8e5ff;
  --secondary-80: #c8befc;
  --secondary-70: #a795f4;
  --secondary-60: #876ae3;
  --secondary-50: #6742ca;
  --secondary-40: #4a1faa;
  --secondary-30: #320584;
  --secondary-20: #25005e;
  --secondary-10: #180038;
}

.dark {
  --text-color: #fed1dde0;
  --neutral-10: #fdcbe5;
  --neutral-20: #c9abd8;
  --neutral-30: #b594c1;
  --neutral-40: #a17eaa;
  --neutral-50: #8d6a93;
  --neutral-60: #79577b;
  --neutral-70: #644664;
  --neutral-80: #4d354b;
  --neutral-90: #362533;

  --primary-10: #fff0f3;
  --primary-20: #fed1dd;
  --primary-30: #fcb2ca;
  --primary-40: #f691b8;
  --primary-50: #ed70a8;
  --primary-60: #de4e98;
  --primary-70: #c62f86;
  --primary-80: #a1136d;
  --primary-90: #70004f;

  --secondary-10: #e8e5ff;
  --secondary-20: #c8befc;
  --secondary-30: #a795f4;
  --secondary-40: #876ae3;
  --secondary-50: #6742ca;
  --secondary-60: #4a1faa;
  --secondary-70: #320584;
  --secondary-80: #25005e;
  --secondary-90: #180038;
}

.dark > *, .light > *, #app {
  transition: 1s ease;
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
}


#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  min-height: 100vh;
  @apply bg-neutral-90 text-text
}
</style>
