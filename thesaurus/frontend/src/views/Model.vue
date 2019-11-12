<template>
  <div class="about text-pink-200">
    <Navbar/>
    <div class="px-6 py-4 text-left max-w-3xl m-auto">
      <h1 class="font-bold text-2xl text-purple-100 mt-4 mb-6 text-center">Arbitrary Replacement</h1>
      <div class="form">

        <label for="text" class="option-label">Input:</label>
        <div class="model-input-wrapper">
          <textarea name="text" id="text" class="model-input" placeholder="Insert text here..." v-model="text"></textarea>
        </div>

        <div class="options-wrapper">
          <div class="options">
            <Slider class="option-wrapper" :value="0.4" :min="0" :max="1" :step="0.01" @input="(e) => prob = e">
              <label for="slider" class="option-label">
                Replacement Chance: <span class="label-val">{{(prob * 100).toFixed(0)}}%</span>
              </label>
            </Slider>

            <Toggle class="option-wrapper" :value="ignore" @input="(e) => ignore = e">
              <label for="switch" class="option-label">
                Ignore StopWords: <span class="label-val">{{ignore}}</span>
              </label>
            </Toggle>
          </div>

          <div class="options">
            <button class="submit-button" @click="submit">Submit</button>
          </div>
        </div>
      </div>

      <div class="loading" v-if="loading"></div>

      <div class="results" v-else-if="resultExists && !error">
        <div class="divider" />
        <h1 class="font-bold text-2xl text-purple-100 mb-3 text-left">Results</h1>
        <div class="result-pair">  
          <h2 class="option-label">Output:</h2>
          <div>{{result.output}}</div>
        </div>        
        <div class="result-pair" v-if="result.numChanged > 0">
          <h2 class="option-label">Number Changed: <span class="text-pink-100 font-medium text-lg">{{result.numChanged}}</span></h2>
        </div>
        <div class="result-pair" v-if="result.notPresent.length > 0">
          <h2 class="option-label">Words not found:</h2>
          <WordList :value="result.notPresent" />
        </div>
        <div class="result-pair" v-if="result.stopwordsSkipped.length > 0">  
          <h2 class="option-label">Stop Words Skipped:</h2>
          <WordList :value="result.stopwordsSkipped" />
        </div>        
      </div>
      
      <div class="error" v-else-if="error">
        <h1 class="font-bold text-2xl text-purple-100 mt-4 mb-6 text-center">Error</h1>
        <p>{{result}}</p>
      </div>
      
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Slider from '@/components/ui/Slider.vue'
import Toggle from '@/components/ui/Toggle.vue'
import WordList from '@/components/ui/WordList.vue'
export default {
  components: {
    Navbar,
    Slider,
    Toggle,
    WordList
  },
  data() {
    return {
      text: "",
      prob: 0.4,
      ignore: true,
      result: {},
      error: false,
      loading: false,
      resultExists: false
    }
  },
  methods: {
    submit() {
      this.loading = true
      this.applyModel()
    },
    applyModel() {
      console.log("Getting something")
      let prod = true;
      if(process.env.NODE_ENV == "dev") prod = false;
      let url = `http://localhost:5000/control`;
      if(prod) url = `https://sproj.model.colehollant.com/control`;
      console.log(url);
      let code = -1
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: this.text,
          ignore: this.ignore,
          prob: parseFloat(this.prob)
        })
      })
      .then(response => {
        let res = response.json()
        code = response.status
        return res
      })
      .catch((error) => {
        console.error('Error:', error)
      }).then((response) => {
        if(code !== 200) {
          this.error = true;
          this.result = response;
          this.loading = false;
          this.resultExists = false;
          console.log("FAILED")
          return
        }
        this.error = false;
        let res = response.data;
        this.result = res;
        this.loading = false;
        this.resultExists = true;
        console.log('Success:', JSON.stringify(this.entry))
      });
    }
  },
}
</script>

<style lang="postcss" scoped>
h2{
  @apply font-bold text-xl text-purple-300 mt-4 mb-1;
}
p::before {
  content: "";
  width: 1.5ch;
  display: inline-block;
}
p{
  @apply text-lg;
}
.result-entry {
  @apply mb-8;
}
.form {
  @apply flex flex-col;
}
.ignore {
  @apply block m-4;
}

.model-input-wrapper {
  --border-size: 3px;
  height: 250px;
  transition: 0.5s ease;
  @apply relative rounded w-full bg-pink-500;
}
.model-input-wrapper:focus-within {
  @apply bg-pink-400;
}
.model-input {
  resize: none;
  background-color: #352538;
  width: calc(100% - (2 * var(--border-size)));
  height: calc(100% - (2 * var(--border-size)));
  margin: var(--border-size);
  transition: 0.5s ease;
  @apply rounded p-4 text-pink-100 font-normal;
}
.model-input:focus {
  --border-size: 5px;
  background-color: #211424;
  @apply outline-none text-pink-200 font-medium shadow ;
}

.submit-button {
  width: 50%;
  transition: all 0.5s ease;
  border-width: 2px;
  @apply outline-none border-solid border-pink-500 rounded-full py-1 px-4 mt-4 mx-auto cursor-pointer text-pink-300 text-xl font-medium;
}
.submit-button:hover {
  background-color: #211424;
  border-width: 3px;
  @apply text-pink-100 font-semibold border-pink-400;
}
.submit-button:focus {
  @apply outline-none;
}

.options {
  @apply flex flex-col justify-center w-full mt-2;
}
.option-wrapper {
  @apply font-medium;
}
.option-label {
  width: max-content;
  @apply relative block font-semibold text-lg text-purple-300 mt-1 mb-2;
}
.label-val {
  @apply font-medium text-sm text-gray-500 ml-2; 
}
.divider {
  width: 66%;
  height: 2px;
  @apply rounded my-8 mx-2;
}
.results {
  margin-bottom: 25vh;
  @apply text-pink-100 font-medium text-lg;
}
.result-pair {
  @apply mb-4;
}

.loading {
  @apply rounded-full w-24 h-24 border-gray-700 border-t-4 my-8 mx-auto;

  border-width: 16px;
  border-top: 16px solid #ed64a6;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


@media (min-width: 500px) {
.options-wrapper {
  @apply flex justify-between;
}
.submit-button {
  @apply mr-0 ml-auto mt-0;
}
}
</style>