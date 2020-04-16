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
        <Slider class="font-medium" v-model="threshold" :min="0" :max="1" :step="0.01">
          <label for="slider" class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
            Threshold:
            <span class="font-medium text-sm text-neutral-30 ml-2">
              {{(threshold * 100).toFixed(0)}}%
            </span>
          </label>
        </Slider>

        <TextInput type="number" class="font-medium" name="numkeywords" v-model="numKeywords" min="0" max="100">
          <label for="numkeywords" class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
            Number of Keywords:
          </label>
        </TextInput>
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
          Stemmed Input:
        </h2>
        <WordList :value="responseState.result.input_stemmed" />
      </div>
      <div>
        <h2 class="w-max relative block font-semibold text-2xl text-secondary-40">
          <label for="dropdown" class="rounded border-2 border-primary-50 px-2 text-secondary-20 flex items-center focus-within:shadow-outline">
            <select name="dropdown" id="dropdown" @change="changeTopic" class="appearance-none bg-transparent focus:outline-none">
              <option :value="i" v-for="(topic, i) in topics" :key="topic.label">
                {{topic.label}}
              </option>
            </select>
            <fa-icon class="w-3 h-3 ml-2 pointer-events-none" icon="chevron-down" />
          </label>
        </h2>
        <NetScores :value="selectedTopic.topic" v-if="Object.keys(selectedTopic.topic).length > 0 && selectedTopic.label === 'Net Scores'" />
        <GroupScores :value="selectedTopic.topic" v-else-if="Object.keys(selectedTopic.topic).length > 0" />
      </div>
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
import NetScores from '@/components/models/NetScores.vue'
import GroupScores from '@/components/models/GroupScores.vue'
import { Loading, WordList, TextInput, Slider } from '@/components/ui'
import { useLdaModel } from '@/composables/useModel'
import { ref, watch, onMounted, computed } from '@vue/composition-api'
export default {
  components: {
    Loading,
    WordList,
    GroupScores,
    NetScores,
    TextInput,
    Slider
  },
  setup() {
    const text = ref('')
    const numKeywords = ref(10)
    const topicIndex = ref(0)
    const threshold = ref(0.01)

    const { responseState, postData } = useLdaModel()

    const topics = ref([{
      label: 'Net Scores',
      topic: {}
    }])
    const selectedTopic = computed(() => topics.value[topicIndex.value])

    function changeTopic(e) {
      topicIndex.value = e.target.value
    }

    function submit() {
      topicIndex.value = 0
      postData({
        text: text.value,
        threshold: Number(threshold.value),
        num_keywords: Number(numKeywords.value)
      })
    }

    onMounted(() => {
      watch(
        () => responseState.result,
        () => {
          const netTopic = responseState.result.net_scores === undefined ? {} : responseState.result.net_scores 
          const res = [{ 
            label: 'Net Scores',
            topic: netTopic
          }]
          if (responseState.result.topics) {
            for (const topic of responseState.result.topics) {
              console.log({ topic })
              res.push({ label: `topic-${topic.topic_num}`, topic })
            }
          }
          topics.value = res
        }
      )
    })

    return {
      text,
      responseState,
      submit,
      topics,
      selectedTopic,
      changeTopic,
      threshold,
      numKeywords
    }
  }
}
</script>

<style lang="postcss" scoped>
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

