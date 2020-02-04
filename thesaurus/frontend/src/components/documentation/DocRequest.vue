<template>
<div class="request-wrapper" v-if="!!request.request">
  <div class="request__header">
    <div class="name">{{request.name}}</div>
  </div>
  <div class="request">
    <div class="request__url">
      <div :class="`request__badge request__badge--${request.request.method}`">{{request.request.method}}</div>
      <div class="request__text">
        <div class="url">{{request.request.url.raw}}</div>
      </div>
    </div>
    <div class="request__section">
      <div class="description">{{request.request.description}}</div>
    </div>
    <Headers :headers="request.request.header" class="request__section"/>
    <Body :body="request.request.body" class="request__section"/>
    <Response :response="response" class="request__section" v-for="(response, index) of request.response" :key="`response-${request.name}-${index}`"/>
  </div>
</div>
</template>

<script>
import Headers from './Headers.vue'
import Response from './Response.vue'
import Body from './Body.vue'
export default {
  components: {
    Headers,
    Body,
    Response
  },
  props: {
    request: {
      type: Object,
      default: () => ({})
    },
  },
}
</script>

<style lang="postcss" scoped>
.request-wrapper {
  @apply mb-8
}
.name {
  @apply text-xl font-black text-indigo-200
}
.description {
  background: #00000030;
  width: max-content;
  max-width: 100%;
  @apply text-base text-teal-300 font-medium mt-4 mb-2 py-3 px-4 shadow rounded
}
.description__title {
  @apply font-bold text-xl text-blue-300 my-2
}
.request__header {
  @apply mb-2
}
.request__url {
  @apply flex flex-col break-words
}
.request {
  @apply flex flex-col
}
.request__badge {
  width: 3.5rem;
  height: min-content;
  @apply text-xs uppercase py-1 flex justify-center items-center rounded font-semibold border-2 mr-2 shadow mb-2
}
.request__badge--GET {
  @apply bg-green-600 border-green-800 text-green-100
}
.request__badge--POST {
  @apply bg-yellow-600 border-yellow-800 text-yellow-100
}
.request__badge--PUT {
  @apply bg-blue-600 border-blue-800 text-blue-100
}
.request__badge--DELETE {
  @apply bg-red-600 border-red-800 text-red-100
}
.url {
  @apply text-base text-indigo-400 break-all
}
.request__section {
  @apply my-1
}

@screen md {
  .request__url {
    @apply flex flex-row items-center
  }
  .request__badge {
    @apply mb-0
  }
  .request__section {
    @apply ml-16
  }
}
</style>