<template>
<div>
  <form class="flex flex-col">
    <label for="text" class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Input:
    </label>
    <div class="h-64 relative rounded w-full bg-primary-50 transition duration-500 focus-within:bg-primary-40">
      <textarea 
        name="text" 
        id="text" 
        class="model-input rounded p-4 text-primary-10 font-normal resize-none focus:outline-none focus:text-text focus:font-medium focus:shadow duration-500" 
        placeholder="Insert text here..." 
        v-model="text" 
      />
    </div>

    <div class="sm:flex sm:justify-between">
      <div class="flex flex-col justify-center w-full mt-2">
        <Slider class="font-medium" v-model="prob" :min="0" :max="1" :step="0.01">
          <label for="slider" class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
            Replacement Chance:
            <span class="font-medium text-sm text-neutral-30 ml-2">
              {{(prob * 100).toFixed(0)}}%
            </span>
          </label>
        </Slider>

        <Toggle class="font-medium" v-model="ignore">
          <label for="switch" class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
            Ignore StopWords:
            <span class="font-medium text-sm text-neutral-30 ml-2">
              {{ignore}}
            </span>
          </label>
        </Toggle>
      </div>

      <div class="flex flex-col justify-center w-full mt-2">
        <button 
          class="w-1/2 py-1 px-4 mt-4 mx-auto sm:mr-0 sm:ml-auto sm:mt-0 border-2 border-primary-40 text-primary-10 text-xl font-medium cursor-pointer rounded-full hover:border-3 hover:text-primary-10 hover:bg-primary-90 focus:outline-none focus:bg-neutral-10 focus:text-primary-90 transition-all duration-500" 
          @click.prevent="submit"
        >
          Submit
        </button>
      </div>
    </div>
  </form>

  <Loading v-if="responseState.loading" />

  <div 
    class="my-16 text-primary-10 font-medium text-lg" 
    v-else-if="responseState.resultExists && !responseState.error"
  >
    <h1 class="font-bold text-2xl text-secondary-10 mb-3 text-left">
      Results
    </h1>
    <div class="grid gap-4">
      <div>  
        <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
          Output:
        </h2>
        <div>{{responseState.result.output}}</div>
      </div>
      <div v-if="responseState.result.numChanged > 0">
        <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
          Number Changed:
          <span class="ml-2 text-primary-10 font-medium text-lg">
            {{responseState.result.numChanged}}
          </span>
        </h2>
      </div>
      <div v-if="responseState.result.notPresent.length > 0">
        <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
          Words not found:
        </h2>
        <WordList :value="responseState.result.notPresent" />
      </div>
      <div v-if="responseState.result.stopwordsSkipped.length > 0">  
        <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
          Stop Words Skipped:
        </h2>
        <WordList :value="responseState.result.stopwordsSkipped" />
      </div>   
    </div>     
  </div>
  
  <div class="my-16 text-left text-text" v-else-if="responseState.error">
    <p class="font-bold text-2xl text-secondary-10 mt-4 mb-6">
      Error
    </p>
    <p class="text-lg">
      {{responseState.result}}
    </p>
  </div>
</div>
</template>

<script>
import { WordList, Slider, Toggle, Loading } from '@/components/ui'
import { useControlModel } from '@/composables/useModel'
import { ref } from '@vue/composition-api'
export default {
  components: {
    Slider,
    Toggle,
    WordList,
    Loading
  },
  setup() {
    const text = ref('')
    const ignore = ref(true)
    const prob = ref(0.4)
    
    const { responseState, postData } = useControlModel()

    function submit() {
      postData({
        text: text.value,
        ignore: ignore.value,
        prob: parseFloat(prob.value)
      })
    }

    return {
      text,
      ignore,
      prob,
      responseState,
      submit
    }
  }
}
</script>

<style lang="postcss" scoped>
.grid-min-auto {
  grid-template: 1fr / auto 1fr;
}

.model-input {
  --border-size: 3px;
  width: calc(100% - (2 * var(--border-size)));
  height: calc(100% - (2 * var(--border-size)));
  margin: var(--border-size);
  background-color: rgb(255, 224, 252);
}

.model-input:focus {
  --border-size: 5px;
  background-color: rgb(255, 234, 253);
}

.dark .model-input {
  background-color: #352538;
}

.dark .model-input:focus {
  background-color: #211424;
}
</style>