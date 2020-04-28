<template>
<div class="docs">
  <div class="filter" v-if="navActive"></div>
  <div class="docs__nav" :class="{ 'docs__mobile--active': navActive }" v-on-click-outside="dismissNav">
    <div class="docs__nav--header">
      <router-link exact to="/">HOME</router-link>
      <button aria-label="navigation toggle" @click="toggleNav" class="docs__nav--hamburger">
        <fa-icon icon="bars" />
      </button>
    </div>
    <div class="docs__nav--main" v-if="!!selected">
      <button 
        :aria-label="item.name"
        v-for="item in envdocs.item" 
        :key="`navlink-${item.name}`" 
        class="docs__navlink"
        :class="{ 'docs__navlink--active': item.name === selected.name }"
        @click="() => selectItem(item)"
      >{{ item.name }}</button>
    </div>
    <div class="docs__nav--requests" v-if="!!selected">
      <div class="docs__nav--subheader">Requests:</div>
      <button 
        :aria-label="item.name"
        v-for="item in selected.item" 
        :key="`request-${item.name}`" 
        class="docs__folder--link"
        @click="() => selectRequest(item)"
      >{{ item.name }}</button>
    </div>
  </div>
  <div class="docs__main" id="docs__main">
    <div class="docs__header">
      <div class="docs__header--title">{{ envdocs.info.name }}</div>
      <div class="docs__header--description">{{ docs.info.description }}</div>
    </div>
    <Folder 
      :folder="selected"
      class="docs__folder"
    />
  </div>
</div>
</template>

<script>
import gsap from 'gsap';
import ScrollToPlugin from "gsap/ScrollToPlugin.js"
import Folder from './Folder.vue'

gsap.registerPlugin(ScrollToPlugin);

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
      // could be nice to make a map of these through a form?
      // const env = {
      //   '{{thesaurus-base}}': 'https://sproj.api.colehollant.com/api/v1/'
      // }
      return JSON.parse(
        JSON.stringify(this.docs).replace(/{{thesaurus-base}}/g,'https://sproj.api.colehollant.com/thesaurus/api/v1')
      )
    }
  },
  data() {
    return {
      selected: null,
      navActive: false
    }
  },
  methods: {
    selectItem(item) {
      this.selected = item
      this.scrollto(document.getElementById('docs__main'), 0)
    },
    scrollto(el, offset) {
      gsap.to(el, {
        duration: 0.5, 
        scrollTo: offset, 
        ease: "power3",
      });
    },
    selectRequest(item) {
      if(this.navActive && window.innerWidth <= 768) {
        this.dismissNav()
        this.scrollto(window, document.getElementById(`request-${item.name}`).offsetTop - 16 - 91)
      } else {
        this.scrollto(document.getElementById('docs__main'), document.getElementById(`request-${item.name}`).offsetTop - 16)
      }
    },
    dismissNav() {
      this.navActive = false
    },
    toggleNav() {
      this.navActive = !this.navActive
    }
  },
  mounted () {
    this.selected = this.envdocs.item[0];
  },
}
</script>

<style lang="postcss" scoped>
.docs {
  @apply leading-relaxed text-lg font-medium text-left text-pink-200
}
.docs__nav {
  @apply fixed top-0 left-0 w-full z-20
}
.filter {
  opacity: 0.5;
  @apply fixed top-0 left-0 w-full h-screen z-0 bg-black
}
.docs__mobile--active.docs__nav {
  width: calc(100% - 8rem);
  border-left: 4px solid rgba(216, 69, 145, 1);
  background-color: rgb(117, 42, 81);
  overflow: auto;
  @apply shadow-xl h-screen
}
.docs__nav--header {
  background-color: rgb(117, 42, 81);
  border-top: 4px solid rgba(216, 69, 145, 1);
  @apply w-full px-4 py-6 text-2xl font-black text-indigo-200 flex justify-between shadow-xl
}
.docs__mobile--active .docs__nav--header {
  border-top: none;
  box-shadow: none;
}
.docs__nav--requests {
  @apply mb-24
}
.docs__nav--main, .docs__nav--requests {
  @apply hidden
}
.docs__mobile--active .docs__nav--main, .docs__mobile--active .docs__nav--requests {
  @apply block
}
.docs__nav--main {
  @apply p-2
}
.docs__navlink {
  transition: all 0.3s ease;
  border-color: transparent;
  @apply block w-full p-2 my-1 cursor-pointer text-left rounded-lg border-2 font-medium text-indigo-100
}
.docs__navlink:hover {
  @apply border-gray-800 shadow bg-pink-900
}
.docs__navlink--active, .docs__navlink:focus {
  @apply outline-none border-gray-900 shadow-xl bg-pink-900 text-indigo-300
}
.docs__navlink--active {
  @apply font-semibold
}
.docs__nav--icon {
  @apply w-8
}
.docs__folder--link {
  @apply block text-sm p-2 text-left break-words leading-tight font-medium w-full text-pink-300
}
.docs__folder--link:hover, .docs__folder--link:focus {
  background-color: #00000028;
  @apply outline-none
}
.docs__main {
  width: calc(100vw - var(--grid-gap) - var(--nav-width));
  padding-right: var(--grid-gap);
  overflow: auto;
  margin-top: 91px;
}
.docs__header {
  @apply mx-4 my-8
}
.docs__folder {
  @apply my-2
}
.docs__nav--subheader {
  @apply font-semibold text-xl p-2 text-indigo-200
}
.docs__header--description {
  @apply font-semibold text-lg text-secondary-30 my-2
}
.docs__header--title {
  @apply font-bold text-2xl text-secondary-20 mt-4 mb-2 uppercase;
}
@screen md {

  .filter {
    @apply hidden
  }

  .docs {
    --grid-gap: 2rem;
    --nav-width: 12rem;
    display: grid;
    grid-column-gap: var(--grid-gap);
    grid-template-columns: var(--nav-width) 1fr;
    @apply fixed top-0 left-0 w-full h-screen leading-relaxed text-lg font-medium text-left text-pink-200
  }

  .docs__main {
    margin-top: 0;
  }

  .docs__mobile--active.docs__nav, .docs__nav {
    border-left: 4px solid rgba(216, 69, 145, 1);
    background-color: rgb(117, 42, 81);
    overflow: auto;
    @apply shadow-xl block relative w-full
  }

  .docs__nav--main, .docs__nav--requests {
    @apply block
  }

  .docs__nav--header {
    border-top: none;
    box-shadow: none;
  }

  .docs__nav--hamburger {
    pointer-events: none;
    @apply hidden
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