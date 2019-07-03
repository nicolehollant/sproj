<template>
  <div class="hello h-full bg-gray-800">

    <header class="w-full p-8 bg-pink-700 shadow-lg flex align-center justify-center items-center">
      <h2 class="text-gray-400 cursor-pointer"><router-link to="/">Home</router-link></h2>
      <h1 class="text-3xl flex-1 font-hairline text-white">Thesaurus</h1>
      <h2 class="opacity-0">Home</h2>
    </header>


    <!-- <h1 class="text-3xl mt-10 mb-4 font-bold uppercase text-pink-300">{{ word }}</h1> -->
    <input type="text" :value="word"
      class="text-3xl mt-10 mb-4 font-bold uppercase text-pink-300 text-center bg-transparent border-b-2 border-solid border-pink-500 outline-none"
    />

    <div v-for="(key, index) in Object.keys(entry)" :key="index">
      <div class="mx-16 my-12">
        <div class="max-w-4xl m-auto">
        <h2 class="text-2xl my-4 text-gray-300 text-left font-hairline capitalize">{{ key }}</h2>
        <div class="bg-pink-900 pt-2 pb-8 rounded shadow-md">
          <div v-for="pos in Object.keys(entry[key])" :key="pos+entry.key">
            <div v-if="entry[key][pos].length > 0" class="mx-8">
              <h3 class="text-xl py-2 text-gray-300 text-left lowercase">{{ pos }}</h3>
              <ul class="flex flex-wrap justify-center bg-gray-400 p-2 rounded">
                <li class="m-4 text-pink-900 text-lg"
                  v-for="nym in entry[key][pos]" :key="pos+entry.key+nym">
                  {{nym}}
                </li>
              </ul>
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
      entry: {}
    }
  },
  mounted () {
    // fetch();
    this.entry = {
        "antonyms": {
            "adjective": [
                "warm"
            ],
            "adverb": [],
            "noun": [],
            "verb": [
                "heat"
            ]
        },
        "synonyms": {
            "adjective": [
                "coolheaded",
                "nerveless",
                "cold",
                "unagitated",
                "unemotional",
                "unfriendly",
                "air-conditioned",
                "air-cooled",
                "caller",
                "chill",
                "chilly",
                "cold",
                "composed",
                "fashionable",
                "precooled",
                "stylish",
                "unqualified",
                "unresponsive",
                "water-cooled"
            ],
            "adverb": [],
            "noun": [
                "aplomb",
                "assuredness",
                "poise",
                "sang-froid",
                "calm",
                "calmness",
                "cold",
                "coldness",
                "composure",
                "equanimity",
                "frigidity",
                "frigidness",
                "low temperature"
            ],
            "verb": [
                "chill",
                "cool down",
                "cool off",
                "alter",
                "change",
                "change state",
                "modify",
                "turn"
            ]
        }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
