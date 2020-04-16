<template>
<div class="relative">
  <div class="midway" v-html="midwaySlides" />
  <div class="link-home">
    <router-link exact to="/">home</router-link>
  </div>
</div>
</template>

<script>
import gsap from 'gsap';
import ScrollToPlugin from "gsap/ScrollToPlugin.js"
import midway from '@/assets/midway-slides.txt';

gsap.registerPlugin(ScrollToPlugin);

export default {
  data() {
    return {
      midwaySlides: midway,
      listener: null
    }
  },
  methods: {
    scrollto(el, offset) {
      gsap.to(el, {
        duration: 0.5, 
        scrollTo: offset, 
        ease: "power3",
        onStart: () => {
          el.style.setProperty('--snap-type', 'none')
        },
        onComplete: () => {
          el.style.setProperty('--snap-type', 'y mandatory')
        }
      });
    },
    next() {
      const el = document.querySelector('.midway')
      const offset = el.scrollTop + window.innerHeight;
      this.scrollto(el, offset)
    },
    prev() {
      const el = document.querySelector('.midway')
      const offset = el.scrollTop - window.innerHeight;
      this.scrollto(el, offset)
    },
    goto(n) {
      
      const el = document.querySelector('.midway')
      const offset = document.querySelectorAll('.midway-slide-title')[n].offsetTop;
      
      gsap.to(el, {
        duration: 1, 
        scrollTo: offset, 
        ease: "power3.out",
        onStart: () => {
          el.style.setProperty('--snap-type', 'none')
        },
        onComplete: () => {
          el.style.setProperty('--snap-type', 'y mandatory')
        }
      });

    }
  },
  mounted () {
    const nums = document.querySelectorAll(".number");
    console.log(nums)
    for(let i = 0; i < nums.length; i++) {
      nums[i].innerHTML = `${i + 1} / ${nums.length}`
    }
    
    const titleKeys = ['Digit1', 'Digit2', 'Digit3', 'Digit4', 'Digit5', 'Digit6', 'Digit7', 'Digit8']
    const nextKeys = ['Space', 'ArrowRight', 'ArrowDown', 'Period']
    const prevKeys = ['ArrowLeft', 'ArrowUp', 'Comma']
    this.listener = document.addEventListener('keydown', (e) => {
      if(nextKeys.includes(e.code)) {
        e.preventDefault()
        this.next()
      }
      if(prevKeys.includes(e.code)) {
        e.preventDefault()
        this.prev()
      }
      if(titleKeys.includes(e.code)) {
        e.preventDefault()
        this.goto(parseInt(e.code.replace("Digit", "")) - 1)
      }
    });
  },
  beforeDestroy () {
    document.removeEventListener(this.listener)
  },
}
</script>

<style lang="postcss" scoped>

.midway {
  --snap-type: y mandatory;
  scroll-snap-type: var(--snap-type);
  overflow: scroll;
  @apply h-screen w-screen leading-normal font-medium text-left text-primary-10;
}
.midway >>> .midway-slide {
  scroll-snap-align: start;
  @apply relative h-screen w-screen text-xl font-medium py-4 px-4;
}
.midway >>> div:nth-child(even) { 
  @apply bg-neutral-80; 
}
.link-home {
  bottom: 1rem;
  left: 1rem;
  @apply absolute text-secondary-30 text-lg;
}
.midway >>> .number {
  background: transparent !important;
  bottom: 1rem;
  right: 1rem;
  @apply absolute text-secondary-30 text-base;
}
.midway >>> #midway {
  font-size: 3rem !important;
  font-weight: 600 !important;
}
.midway >>> .midway-slide-title {
  scroll-snap-align: start;
  @apply relative h-screen w-screen text-lg text-left font-medium flex flex-col justify-center items-start px-4;
}
.midway >>> .midway-slide-title h1, .midway >>> .midway-slide-title h2 {
  padding-top: 0 !important;
  margin-top: 0 !important;
  @apply mb-4;
}
.midway >>> .midway-slide-title p {
  @apply text-xl font-semibold;
}
.midway >>> h1 {
  top: 40%;
  left: 50%;
  transform: translate(-50%);
  @apply absolute leading-loose font-black text-2xl text-secondary-10 uppercase;
}
.midway >>> h2 {
  @apply leading-loose font-black text-2xl text-secondary-10 pt-10 mb-5 uppercase;
}
.midway >>> h3 {
  @apply leading-loose font-semibold text-2xl text-secondary-20 my-2;
}
.midway >>> p {
  @apply mt-3;
}
.midway >>> a {
  @apply text-primary-40 underline;
}
.midway >>> ul{
  list-style: inside;
  margin: 0.2rem 0 0.5rem;
}

@screen sm {
  .midway {
    @apply leading-relaxed text-xl;
  }
  .midway >>> #midway {
    font-size: 4rem !important;
  }
  .midway >>> h1, .midway >>> h2 {
    @apply text-4xl pt-20 mb-10;
  }
  .midway >>> h3 {
    @apply text-3xl;
  }
  .midway >>> .number {
    @apply text-lg;
  }
  .midway >>> .midway-slide {
    @apply text-2xl py-10 px-20;
  }
  .midway >>> p {
    @apply leading-loose mt-6;
  }
  .midway >>> .midway-slide-title {
    @apply text-center items-center;
  }
  .midway >>> .midway-slide-title h3 {
    @apply text-3xl;
  }
  .midway >>> .midway-slide-title p {
    @apply text-2xl;
  }
}
</style>