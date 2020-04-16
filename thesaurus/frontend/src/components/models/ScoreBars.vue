<template>
<div v-if="!allZero">
  <div v-for="(value, field, index) in value" :key="[name, field, index].join('-')">
    <div 
      class="grid grid-min-auto items-baseline" 
      :class="{
        'gap-2': size === 'base',
        'gap-1': size === 'sm',
      }"
    >
      <h2 
        class="w-max my-1 relative block text-secondary-20 capitalize"
        :class="{
          'text-lg font-semibold': size === 'base',
          'text-base font-regular ml-4': size === 'sm',
        }"
      >
        {{ field }}:
      </h2>
      <div>{{value}}</div>
    </div>
    <ProgressBar
      :value="value"
      :color="field"
      class="rounded overflow-hidden" 
      :class="{
        'h-8': size === 'base',
        'h-5 ml-4': size === 'sm',
      }"
    />
  </div>
</div>
<div v-else class="text-sm text-neutral-30" :class="{ 'ml-4': size === 'sm' }">
  All zero (neutral score)
</div>
</template>

<script>
import { ProgressBar } from '@/components/ui'
export default {
  props: {
    value: {
      type: Object
    },
    name: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'base'
    }
  },
  components: {
    ProgressBar
  },
  computed: {
    allZero() {
      return Object.values(this.value).reduce((prev, curr) => prev + curr, 0.0) === 0.0
    }
  }
}
</script>

<style lang="postcss" scoped>
.grid-min-auto {
  grid-template: 1fr / auto 1fr;
}
</style>