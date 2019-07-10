<template>
  <div class="hello" :key="wordkey">
    <div>
      <input type="text" v-model="m_word" v-on:keyup.enter="fetchWord"
        class="word-input text-3xl mt-10 mb-4 font-bold uppercase text-pink-200 text-center bg-transparent border-b-2 border-solid border-pink-500 outline-none"
      />
    </div>
    <button type="submit" @click="fetchWord"
      class="submit-button outline-none border-2 border-solid border-pink-500 rounded-full py-1 px-4 focus:outline-none cursor-pointer text-pink-300 text-xl font-bold hover:bg-pink-900 hover:text-gray-300"
    >
      Take A Look
    </button>

    <div v-if="dne">
      <h2 class="text-semilight text-2xl text-center my-12 font-hairline capitalize">Sorry, we couldn't find that for you :(</h2>
    </div>
    <div v-else>
    <div v-for="(key, index) in Object.keys(entry)" :key="index" class="mx-6 my-12">
      <div class="max-w-3xl m-auto">

        <div v-if="notEmpty(entry[key])">
        <h2 class="text-semilight text-2xl my-4 text-left font-hairline capitalize">{{ key }}</h2>
        <div class="nym-box-wrapper bg-pink-900 pt-2 pb-8 rounded">
          <div v-for="pos in Object.keys(entry[key])" :key="pos+entry.key">
            <div v-if="entry[key][pos].length > 0" class="mx-4 md:mx-8">
              <h3 class="text-xl py-2 text-light text-left lowercase">{{ pos }}</h3>
              <ul class="nym-box flex flex-wrap justify-center bg-gray-400 p-2 rounded">
                <li class="m-4 text-pink-300 text-xl" v-for="nym in entry[key][pos]" :key="pos+entry.key+nym">
                  <button @click="()=>setWord(nym)" class="focus:outline-none hover:text-pink-500">{{nym}}</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
        </div>


      </div>
    </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
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
      let url = `http://localhost:3000/thesaurus/api/v1/words/${this.m_word.trim()}`;
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
    setWord(nym){
      this.m_word=nym.trim().toLowerCase();
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
}
.submit-button {
  transition: all 0.2s ease-in-out;
}

.nym-box-wrapper{
  
  box-shadow: 4px 4px 10px -1px rgba(104, 0, 95, 0.5);
  background: linear-gradient(155deg, rgb(117, 42, 81) 30%, rgb(88, 33, 87) 70%);
}
.nym-box{
  background-color: rgba(59, 12, 33, 0.6);
  border-color: rgba(216, 69, 145, 0.7);
  @apply border-l-4;
  /* @apply bg-gray-800 border border-pink-500; */
}

</style>
