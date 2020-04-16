<template>
<div class="grid gap-2">
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Input Score:
    </h2>
    <ScoreBars size="sm" :value="value.input" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Keywords Given Keywords:
    </h2>
    <ScoreBars size="sm" :value="value.keywords_given_keywords" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Keywords Given Topic:
    </h2>
    <ScoreBars size="sm" :value="value.keywords_given_topic" />
  </div>
  <div>  
    <h2 class="w-max mt-1 mb-2 relative block font-semibold text-lg text-secondary-20">
      Topic Score:
    </h2>
    <ScoreBars size="sm" :value="value.topic" />
  </div>
</div>
</template>

<script>
import ScoreBars from '@/components/models/ScoreBars.vue'
export default {
  name: "NetScores",
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
