<template>
  <div class="hello">
    <div>
      <input type="text" :value="word"
        class="word-input text-3xl mt-10 mb-4 font-bold uppercase text-pink-200 text-center bg-transparent border-b-2 border-solid border-pink-500 outline-none"
      />
    </div>
    <button type="submit"
      class="submit-button outline-none border-2 border-solid border-pink-500 rounded-full py-1 px-4 focus:outline-none cursor-pointer text-pink-300 text-xl font-bold hover:bg-pink-900 hover:text-gray-300"
    >
      Take A Look
    </button>

    <div v-for="(key, index) in Object.keys(entry)" :key="index" class="mx-6 my-12">
      <div class="max-w-3xl m-auto">
        <h2 class="text-2xl my-4 text-gray-300 text-left font-hairline capitalize">{{ key }}</h2>
        <div class="bg-pink-900 pt-2 pb-8 rounded shadow-md">
          <div v-for="pos in Object.keys(entry[key])" :key="pos+entry.key">
            <div v-if="entry[key][pos].length > 0" class="mx-4 md:mx-8">
              <h3 class="text-xl py-2 text-gray-300 text-left lowercase">{{ pos }}</h3>
              <ul class="flex flex-wrap justify-center bg-gray-400 p-2 rounded">
                <li class="m-4 text-pink-900 text-lg"
                  v-for="nym in entry[key][pos]" :key="pos+entry.key+nym">{{nym}}
                </li>
              </ul>
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

<style scoped lang="postcss">

.word-input{
  margin-left: 2rem;
  margin-right: 2rem;
  max-width: calc(100vw - 4rem);
}
.submit-button{
  transition: all 0.2s ease-in-out;
}
</style>
