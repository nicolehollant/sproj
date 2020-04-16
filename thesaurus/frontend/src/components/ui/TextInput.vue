<template>
<div class="text-input__wrapper">
  <slot />
  <input :type="$attrs.type || 'text'" 
    :name="$attrs.name"
    :id="$attrs.id" 
    :ref="$attrs.ref"
    :placeholder="$attrs.placeholder"
    :max="$attrs.max"
    :min="$attrs.min"
    class="text-input focusable h-10 lg:h-12"
    :class="{'has-error': error !== ''}"
    v-model="m_value"
    @input="$emit('input', m_value)"
  >
  <p v-if="error !== ''" class="text-orange-500 font-medium text-sm text-center mt-1">{{error}}</p>
</div>
</template>

<script>
export default {
  props: {
    value: {
      type: null,
      default: ''
    },
    error: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      m_value: this.value
    }
  },
}
</script>

<style lang="postcss" scoped>
.text-input__wrapper {
  @apply w-full text-left;
}
.text-input {
  -webkit-appearance: none;
  background-color: rgb(255, 224, 252);
  @apply w-full px-2 font-normal rounded border-2 border-primary-50 text-primary-10 appearance-none;
}
.text-input::placeholder {
  @apply text-neutral-20;
}
.has-error {
  @apply border-orange-500
}
.text-input:focus {
  background-color: rgb(255, 234, 253);
  @apply font-medium border-primary-60 text-text outline-none
}

.dark .text-input {
  background-color: #352538;
}

.dark .text-input:focus {
  background-color: #211424;
}
</style>