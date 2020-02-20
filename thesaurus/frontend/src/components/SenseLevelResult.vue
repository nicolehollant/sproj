<template>
<div class="senselevel senselevel--results-box">
  
  <h2 class="senselevel--category">
    Sense Associations 
    <InfoHover>
      <div>
        <div>
          <p><b class="text-blue-500">sense</b> is the way in which the word is used.</p>
          <p class="text-sm text-blue-200 my-1 ml-1 pl-2 border-l-2 border-teal-700">ex: "cool" can be used in the sense of "quiet, chill, blunt" or in the sense of "cold, pinching, biting"</p>
        </div>
        <div>
          <p><b class="text-blue-500">associations</b> are the affects associated with the word used in the given sense</p>
          <p class="text-sm text-blue-200 my-1 ml-1 pl-2 border-l-2 border-teal-700">ex: when "cool" is used in the sense of "quiet, chill, blunt" it has a <span class="text-green-300 italic">positive</span> association</p>
        </div>
        <div>
          <p><b class="text-blue-500">shared synonyms</b> is a list of synonyms shared between the synonyms of the current word and the synonyms of each word of the given sense</p>
        </div>
      </div>
    </InfoHover>
  </h2>

  <div class="senselevel--pos__wrapper">
    <div class="senselevel--results__entries" 
      v-for="(index, senses) in entry" 
      :key="`senselevel--entry-${senses}`"
    >
      <div 
        class="senselevel--entry__sense senselevel--pos" 
        v-if="entry[senses].sense"
      >
        <span>sense: </span>
        <span 
          class="senselevel--entry__sense-word"
          v-for="sense in entry[senses].sense" 
          :key="`senselevel--entry-${senses}-${sense}`"
          v-on:click="()=>$emit('setword', sense)"
        >
          {{commaSeparated(sense, entry[senses].sense)}}
        </span>
      </div>

      <div
        class="senselevel--entry__wrapper"
        v-if="entry[senses].associations"
      >
        <div class="senselevel--entry__associations senselevel--pos">
          <span>associations: </span>
          <span 
            class="senselevel--entry__sense-word"
            v-for="association in entry[senses].associations" 
            :key="`senselevel--entry-${senses}-${association}`"
            v-on:click="()=>$emit('setword', association)"
          >
            {{commaSeparated(association, entry[senses].associations)}}
          </span>
        </div>

        <div class="associated__vals" v-if="!!entry[senses] && !!entry[senses].sense" :key="ready">
          <div class="associated__vals--header">Shared Synonyms</div>
          <div>{{ getMap(entry[senses].sense) }}</div>
        </div>
      </div>
      <div class="senselevel--error__wrapper" v-else>
        <div>No associations</div>
        <div class="associated__vals mt-2" v-if="!!entry[senses] && !!entry[senses].sense" :key="ready">
          <div class="associated__vals--header">Shared Synonyms</div>
          <div>{{ getMap(entry[senses].sense) }}</div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import InfoHover from '@/components/ui/InfoHover.vue'

export default {
  components: {
    InfoHover,
  },
  props: {
    synonyms: {
      type: Array,
      required: false
    },
    entry: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      senseMap: {},
      ready: 0
    }
  },
  methods: {
    getMap(senses) {
      if(!Array.isArray(senses)) return null
      if(senses.join("__") in this.senseMap) return this.senseMap[senses.join("__")].join(", ")
      return null
    },
    commaSeparated(elem, arr) {
      if(elem === arr[arr.length - 1]) {
        return elem + ""
      } else {
        return elem + ", "
      }
    },
    fetchWord(word, sense) {
      let prod = true;
      if(process.env.NODE_ENV == "dev") prod = false;
      let url = `http://localhost:3000/thesaurus/api/v1/words/${word.trim()}`;
      if(prod) url = `https://sproj.api.colehollant.com/thesaurus/api/v1/words/${word.trim().toLowerCase()}`;
      fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      })
      .then(response => {
        let res = response.json()
        return res
      })
      .catch((error) => {
        console.error('Error:', error)
      }).then((response) => {
        let res = response.data;
        for(const synonym of this.getAllSynonyms(res.synonyms)) {
          if(!this.senseMap[sense].includes(synonym) && this.synonyms.includes(synonym)) {
            this.senseMap[sense].push(synonym)
          }
        }
        this.ready++
      });
    },
    getAllSynonyms(synonyms) {
      if (typeof synonyms !== 'object') return null
      return Object.values(synonyms).reduce((prev, curr) => prev.concat(curr), [])
    }
  },
  mounted () {
    if(this.synonyms) {
      for(const senses of this.entry) {
        if(senses.sense) {
          this.senseMap[senses.sense.join("__")] = []
          for(const sense of senses.sense) {
            this.fetchWord(sense, senses.sense.join("__"))
          }
        }
      }
    }
  },
}
</script>

<style lang="postcss" scoped>
.text-semilight{
  color: rgb(253, 203, 229);
}
.text-light{
  color: #dec4f0;
}
.senselevel--pos__wrapper{
  box-shadow: 4px 4px 10px -1px rgba(104, 0, 95, 0.5);
  background: linear-gradient(155deg, rgb(117, 42, 81) 30%, rgb(88, 33, 87) 70%);
  min-width: min-content;
  @apply pt-2 pb-8 rounded;
}
.wrapper {
  background-color: rgba(59, 12, 33, 0.6);
  min-width: min-content;
  @apply border-l-4 flex flex-wrap justify-start p-2 rounded;
}
.senselevel--entry__wrapper{
  border-color: rgba(216, 69, 145, 0.7);
  @apply wrapper
}
.senselevel--error__wrapper {
  @apply wrapper border-purple-500 text-purple-400 italic lowercase flex-col items-start
}

.senselevel--category {
  @apply text-semilight text-2xl my-4 text-left capitalize;
}

.senselevel--pos {
  @apply text-xl py-2 text-light text-left lowercase;
}

.senselevel--entry {
  @apply m-4 text-pink-300 text-xl cursor-pointer;
}
.senselevel--entry:hover {
  @apply text-pink-500;
}
.senselevel--entry__sense-word {
  @apply text-pink-200 cursor-pointer;
}
.senselevel--entry__sense-word:hover {
  @apply text-pink-500;
}
.senselevel--results__entries {
  @apply mx-4;
}

.senselevel--results-box {
  @apply max-w-3xl m-auto;
}

.associated__vals {
  @apply text-left text-sm text-purple-200 italic
}
.associated__vals--header {
  text-transform: none;
  @apply text-left text-base text-purple-300 font-medium font-medium not-italic
}

@media (min-width: 768px) {
  .senselevel--results__entries {
    @apply mx-8;
  }
}
</style>