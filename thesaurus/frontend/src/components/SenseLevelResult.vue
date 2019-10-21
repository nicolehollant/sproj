<template>
<div class="senselevel senselevel--results-box">
  
  <h2 class="senselevel--category">Sense Associations</h2>

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
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    entry: {
      type: Array,
      required: true
    }
  },
  methods: {
    commaSeparated(elem, arr) {
      if(elem === arr[arr.length - 1]) {
        return elem + ""
      } else {
        return elem + ", "
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
.senselevel--entry__wrapper{
  background-color: rgba(59, 12, 33, 0.6);
  border-color: rgba(216, 69, 145, 0.7);
  min-width: min-content;
  @apply border-l-4 flex flex-wrap justify-start p-2 rounded;
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
@media (min-width: 768px) {
  .senselevel--results__entries {
    @apply mx-8;
  }
}
</style>