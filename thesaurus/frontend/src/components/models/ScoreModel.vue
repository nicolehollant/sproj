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
      <ScoreBars :value="responseState.result" size="base" />
    </div> 
  </div>
  
  <div class="my-16 text-left text-text" v-else-if="responseState.error">
    <h1 class="font-bold text-2xl text-secondary-10 mt-4 mb-6">
      Error
    </h1>
    <p class="text-lg">
      {{responseState.result}}
    </p>
  </div>
</div>
</template>

<script>
import ScoreBars from '@/components/models/ScoreBars.vue'
import { Toggle, Loading } from '@/components/ui'
import { useRawScoreModel } from '@/composables/useModel'
import { ref } from '@vue/composition-api'
export default {
  components: {
    Toggle,
    Loading,
    ScoreBars
  },
  setup() {
    const text = ref('')
    const ignore = ref(true)
    
    const { responseState, postData } = useRawScoreModel()

    function submit() {
      postData({
        text: text.value,
        ignore: ignore.value,
      })
    }

    return {
      text,
      ignore,
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