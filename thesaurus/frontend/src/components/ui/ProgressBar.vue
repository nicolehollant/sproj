<template>
<div class="w-full relative bg-neutral-80 border border-neutral-60" :class="$attrs.class">
  <div 
    class="absolute inset-y-0 left-0" 
    :style="`width: ${ value * 100 }%`" 
    :class="{
      'bg-blue-600': color === 'sadness',
      'bg-yellow-500': color === 'joy',
      'bg-red-600': color === 'anger',
      'bg-black': color === 'fear',
      'bg-primary-50': !['sadness','joy','anger','fear'].includes(color)
    }"
  />
</div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: {
    value: {
      type: Number
    },
    color: {
      type: String,
      validator: (a) => [
        'sadness',
        'joy',
        'anger',
        'fear'
      ].includes(a)
    }
  },
}
</script>