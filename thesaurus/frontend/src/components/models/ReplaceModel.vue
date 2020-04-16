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

    <div class="sm:flex sm:justify-between mt-2">
      <div class="flex flex-col justify-center w-full mt-2">
        <label for="dropdown" class="rounded border-2 border-primary-50 px-2 text-secondary-20 flex items-center focus-within:shadow-outline">
          <select name="dropdown" id="dropdown" @change="(e) => affectIndex = e.target.value" class="py-1 w-full appearance-none bg-transparent focus:outline-none">
            <option :value="i" v-for="(affect, i) in affectList" :key="affect">
              {{affect}}
            </option>
          </select>
          <fa-icon class="w-3 h-3 ml-2 pointer-events-none" icon="chevron-down" />
        </label>
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
    <pre>{{ responseState.result }}</pre>
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
import { Loading } from '@/components/ui'
import { useAlterTargetModel } from '@/composables/useModel'
import { ref } from '@vue/composition-api'
export default {
  components: {
    Loading,
  },
  setup() {
    const text = ref('')
    const affectIndex = ref(0)
    const affectList = ['sadness', 'joy', 'fear', 'anger']
    
    const { responseState, postData } = useAlterTargetModel()

    function submit() {
      postData({
        text: text.value,
      }, affectList[affectIndex.value])
    }

    return {
      text,
      affectIndex,
      responseState,
      submit,
      affectList
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