<script>
export default {
  functional: true,
  props: {
    entry: {
      type: Object,
      required: true
    }
  },
  render(h, {props, listeners}) {
    const hasResults = (obj) => {
      for(let key of Object.keys(obj)){
        if(obj[key].length > 0) return true;
      }
      return false
    }
    let entry = props.entry;
    return h("div", { staticClass: "my-12" }, [
      h("div", {
          staticClass: "thesaurus--results-box",
        }, [
        Object.keys(entry).map(key => {
          return hasResults(entry[key]) ? h("div", {}, [
            h("h2", {
              staticClass: "thesaurus--category",
              domProps: { "innerHTML": key },
            }),
            h("div", {
              staticClass: "thesaurus--pos__wrapper"
            }, Object.keys(entry[key]).map(pos => {
              if(entry[key][pos].length > 0) {
                return h("div", { staticClass: "mx-4 md:mx-8"}, [
                  h("h3", { staticClass: "thesaurus--pos" }, pos),
                  h("ul", { "class": "thesaurus--entry__wrapper" }, 
                    entry[key][pos].map(word => {
                      return h("li", {
                        attrs: { tabindex: 0 },
                        staticClass: "thesaurus--entry",
                        domProps: { "innerHTML": word },
                        on: {
                          keydown: (e) => {
                            if(e.key === 'Enter' || e.key === ' ') {
                              const emit_event = listeners.event_from_child;
                              emit_event(word);
                            }
                          },
                          click: () => {
                            const emit_event = listeners.event_from_child;
                            emit_event(word);
                          }
                        }
                      })
                    })
                  )
                ])
              }
            }))
          ]) : null
        })
        ] 
      )
    ])
  }
}
</script>

<style lang="postcss" scoped>
/* .text-semilight{
  color: rgb(253, 203, 229);
}
.text-light{
  color: #dec4f0;
} */
.thesaurus--pos__wrapper{
  box-shadow: 4px 4px 10px -1px rgba(104, 0, 95, 0.5);
  background: linear-gradient(155deg, rgb(248, 172, 213) 30%, rgb(192, 126, 191) 70%);
  min-width: min-content;
  @apply pt-2 pb-8 rounded;
}
.dark .thesaurus--pos__wrapper{
  box-shadow: 4px 4px 10px -1px rgba(138, 5, 127, 0.5);
  background: linear-gradient(155deg, rgb(117, 42, 81) 30%, rgb(88, 33, 87) 70%);
}
.thesaurus--entry__wrapper{
  background-color: rgba(233, 177, 228, 0.6);
  border-color: rgba(216, 69, 145, 0.7);
  min-width: min-content;
  @apply border-l-4 flex flex-wrap justify-center p-2 rounded;
}
.dark .thesaurus--entry__wrapper{
  background-color: rgba(59, 12, 33, 0.6);
  border-color: rgba(216, 69, 145, 0.7);
}

.thesaurus--category {
  @apply text-primary-10 text-2xl my-4 text-left capitalize;
}

.thesaurus--pos {
  @apply text-xl py-2 text-secondary-20 text-left lowercase;
}

.thesaurus--entry {
  @apply m-4 text-primary-20 text-xl cursor-pointer;
}
.thesaurus--entry:hover {
  @apply text-primary-10 underline;
}
.thesaurus--entry:focus {
  @apply outline-none underline
}

.thesaurus--results-box {
  @apply max-w-3xl m-auto;
}
</style>

<!--
<template functional>
<div class="thesaurus--results-box">
  <div 
    v-for="(key, i) in Object.keys(props.entry)" 
    :key="[key, i].join('-')"
  >
    <div v-if="Object.entries(props.entry[key]).map(([k, v]) => v.length > 0).reduce((a, c) => (a || c))">
      <h2 class="thesaurus--category">
        {{ key }}
      </h2>
      <div class="thesaurus--pos__wrapper">
        <div 
          v-for="(pos, j) in Object.keys(props.entry[key])" 
          :key="[pos, props.entry.key, j].join('-')"
        >
          <div 
            v-if="props.entry[key][pos].length > 0" 
            class="mx-4 md:mx-8"
          >
            <h3 class="thesaurus--pos">
              {{ pos }}
            </h3>
            <ul class="thesaurus--entry__wrapper">
              <li 
                class="thesaurus--entry" 
                v-for="(word, k) in props.entry[key][pos]" 
                :key="[pos, props.entry.key, word, k].join('-')" 
                v-on:keydown.enter="() => listeners.event_from_child(word)" 
                v-on:keydown.space="() => listeners.event_from_child(word)" 
                v-on:click="() => listeners.event_from_child(word)" 
                tabindex="0"
              >
                {{word}}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
-->