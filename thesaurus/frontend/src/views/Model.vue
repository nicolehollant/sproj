<template>
<div class="about text-pink-200">
  <Navbar />
  <div class="px-6 py-4 text-left max-w-3xl m-auto">
    <div class="flex font-bold text-2xl text-primary-10 mt-4 mb-6 text-center items-baseline justify-between">
      <div>Model: </div>
      <label for="dropdown" class="rounded border-2 border-primary-50 px-2 flex items-center focus-within:shadow-outline">
        <select name="dropdown" id="dropdown" @change="(e) => modelIndex = e.target.value" class="py-1 w-full appearance-none bg-transparent focus:outline-none">
          <option :value="i" v-for="(model, i) in models" :key="model">
            {{model}}
          </option>
        </select>
        <fa-icon class="w-3 h-3 ml-2 pointer-events-none" icon="chevron-down" />
      </label>
    </div>
    <component :is="currentModel" />
  </div>
</div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import { ControlModel, ScoreModel, LdaModel, ReplaceModel } from '@/components/models'
import { ref, computed } from '@vue/composition-api'
export default {
  components: {
    Navbar,
    ControlModel,
    ScoreModel,
    LdaModel,
    ReplaceModel
  },
  setup() {
    const models = ['Arbitrary Replacement', 'Score Raw', 'Score LDA', 'Targeted Replacement']
    const modelIndex = ref(0)
    const currentModel = computed(() => {
      if (models[modelIndex.value] === 'Arbitrary Replacement') return ControlModel
      if (models[modelIndex.value] === 'Score Raw') return ScoreModel
      if (models[modelIndex.value] === 'Score LDA') return LdaModel
      if (models[modelIndex.value] === 'Targeted Replacement') return ReplaceModel
    })
    return { models, modelIndex, currentModel }
  }
}
</script>