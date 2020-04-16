<template>
<div class="about text-pink-200">
  <Navbar />
  <div class="px-6 py-4 text-left max-w-3xl m-auto">
    <h1 class="font-bold text-2xl text-primary-10 mt-4 mb-6 text-center">
      {{ model }}
    </h1>
    <!-- <ControlModel /> -->
    <component :is="currentModel" />
  </div>
</div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import { ControlModel, ScoreModel, LdaModel } from '@/components/models'
import { ref, computed } from '@vue/composition-api'
export default {
  components: {
    Navbar,
    ControlModel,
    ScoreModel,
    LdaModel
  },
  setup() {
    const models = ['Arbitrary Replacement', 'Score Raw', 'Score LDA']
    const model = ref('Score LDA')
    // const model = ref('Score Raw')
    // const model = ref('Arbitrary Replacement')
    const currentModel = computed(() => {
      if (model.value === 'Arbitrary Replacement') return ControlModel
      if (model.value === 'Score Raw') return ScoreModel
      if (model.value === 'Score LDA') return LdaModel
    })
    return { models, model, currentModel }
  }
}
</script>