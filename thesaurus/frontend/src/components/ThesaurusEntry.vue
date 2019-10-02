<template>
  <div class="hello" :key="wordkey">
    <div>
      <input type="text" v-model="m_word" v-on:keyup.enter="fetchWord" class="word-input"/>
    </div>

    <button type="submit" @click="fetchWord" class="submit-button">
      Take A Look
    </button>

    <div v-if="dne">
      <h2 class="error-text">Sorry, we couldn't find that for you :(</h2>
    </div>

    <div v-else>
      <ThesaurusResult :entry="entry" @event_from_child="setWord"/>
    </div>
  </div>
</template>

<script>
import ThesaurusResult from "@/components/ThesaurusResult.vue"
export default {
  name: 'HelloWorld',
  components: {
    ThesaurusResult
  },
  props: {
    word: String
  },
  data() {
    return {
      m_word: this.word,
      entry: {},
      wordkey: 0,
      dne: true,
      exists: [false, false]
    }
  },
  methods: {
    fetchWord() {
      console.log("Getting something")
      let prod = true;
      if(process.env.NODE_ENV == "dev") prod = false;
      // should actually do this at a state level
      let url = `http://localhost:3000/thesaurus/api/v1/words/${this.m_word.trim()}`;
      if(prod) url = `https://sproj.api.colehollant.com/thesaurus/api/v1/words/${this.m_word.trim().toLowerCase()}`;
      console.log(url);
      fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .catch((error) => {
        this.dne = true;
        console.error('Error:', error)
      }).then((response) => {
        if(response.message!=="Word retrieved"){
          this.dne = true;
          this.wordkey++;
          return;
        }
        let res = response.data.result;
        this.parseWord(res);
        this.wordkey++;
        console.log('Success:', JSON.stringify(this.entry))
      });
    },
    parseWord(res){
      this.entry.antonyms = res.antonyms;
      this.entry.synonyms = res.synonyms;
      this.exists[0] = this.notEmpty(this.entry.antonyms);
      this.exists[1] = this.notEmpty(this.entry.synonyms);
      let doesNotExist = true;
      for (const exist of this.exists) {
        if(exist) doesNotExist = false;
      }
      this.dne = doesNotExist;
    },
    notEmpty(o){
      for(let key of Object.keys(o)){
        if(o[key].length > 0) return true;
      }
      return false
    },
    setWord(e) {
      console.log(e)
      this.m_word=e.trim().toLowerCase();
      this.fetchWord()
    }
  },
  mounted () {
    this.fetchWord()
  },
}
</script>

<style scoped lang="postcss">
.text-semilight{
  color: rgb(253, 203, 229);
}
.text-light{
  color: #dec4f0;
}
.word-input{
  margin-left: 2rem;
  margin-right: 2rem;
  max-width: calc(100vw - 4rem);
  @apply text-3xl mt-10 mb-4 font-bold uppercase text-pink-200 text-center bg-transparent border-b-2 border-solid border-pink-500 outline-none;
}
.submit-button {
  transition: all 0.2s ease-in-out;
  @apply outline-none border-2 border-solid border-pink-500 rounded-full py-1 px-4 cursor-pointer text-pink-300 text-xl font-bold;
}
.submit-button:hover {
  @apply bg-pink-900 text-gray-300;
}
.submit-button:focus {
  @apply outline-none;
}
.error-text {
  @apply text-semilight text-2xl text-center my-12 font-hairline capitalize;
}
</style>
