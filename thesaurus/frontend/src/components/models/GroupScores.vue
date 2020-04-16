<template>
<div class="grid gap-2">
  <div v-if="value.topic_num" class="grid gap-1">  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Topic Number: {{ value.topic_num }} 
    </h2>
    <p class="font-semibold text-base">
      Topic Likelihood: {{ value.probability }}
      <span v-if="value.dominant">(dominant topic)</span>
    </p>
    <p class="font-semibold text-base">Topic Definition:</p>
    <div style="max-height: 16rem" class="overflow-scroll border border-neutral-50 rounded p-2">
      <div v-for="(item, i) in value.topic_keywords" :key="item[0]" class="grid grid-cols-2">
        <div>{{ i + 1 }}. {{ item[0] }}: </div>
        <div>{{ item[1] }}</div>
      </div>
    </div>
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Input Score:
    </h2>
    <ScoreBars size="sm" :value="value.scores.input" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Keywords Given Keywords:
    </h2>
    <ScoreBars size="sm" :value="value.scores.keywords_given_keywords" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Keywords Given Topic:
    </h2>
    <ScoreBars size="sm" :value="value.scores.keywords_given_topic" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Topic Score:
    </h2>
    <ScoreBars size="sm" :value="value.scores.topic" />
  </div>
</div>
</template>

<script>
import ScoreBars from '@/components/models/ScoreBars.vue'
export default {
  name: "GroupScores",
  props: {
    value: {
      type: Object
    }
  },
  components: {
    ScoreBars
  }
}
</script>
