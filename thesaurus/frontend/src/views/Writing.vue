<template>
<div>
  <Navbar/>
  <div class="markdown" v-html="content"></div>
</div>
</template>

<script>
// added markdown-it, but would rather fix my markdown thing instead...
// note: raw-loader was needed for the whole 'import writing'
// prob wanna shrink text before sm
import Navbar from '@/components/Navbar.vue'
import writing from '@/assets/writing/all-writing.txt';

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      content: ""
    }
  },
  mounted () {
    var md = require('markdown-it')();
    // snagged from https://stackoverflow.com/questions/5653207/remove-html-comments-with-regex-in-javascript
    let reducedWriting = writing.replace(new RegExp(
    '<!--[\\s\\S]*?(?:-->)?'
    + '<!---+>?'  // A comment with no body
    + '|<!(?![dD][oO][cC][tT][yY][pP][eE]|\\[CDATA\\[)[^>]*>?'
    + '|<[?][^>]*>?',  // A pseudo-comment
    'g'), '')
    this.content = md.render(reducedWriting);
  },
}
</script>

<style lang="postcss" scoped>
.markdown {
  @apply leading-relaxed text-lg font-medium p-4 max-w-4xl mb-10 mx-auto text-left text-primary-20 -mt-10;
}
.markdown >>> h1 {
  @apply font-black text-3xl text-secondary-30 mt-20 mb-2 uppercase;
}
.markdown >>> h2 {
  @apply font-bold text-2xl text-secondary-20 mt-12 mb-2;
}
.markdown >>> h3 {
  @apply font-bold text-xl text-secondary-20 mt-8 mb-2;
}
.markdown >>> h4{
  @apply font-bold text-lg text-secondary-20 mt-4 mb-1;
}
.markdown >>> p {
  @apply mb-8;
}
.markdown >>> code {
  @apply text-secondary-30;
}
.markdown >>> a {
  @apply text-secondary-30 underline;
}
.markdown >>> ul{
  margin: 0.2rem 0 0.5rem;
}
.markdown >>> blockquote{
  background: linear-gradient(155deg, rgb(248, 172, 213) 30%, rgb(192, 126, 191) 70%);
  box-shadow: 4px 4px 10px -1px rgba(104, 0, 95, 0.5);
  border-color: rgba(241, 55, 151, 0.9);
  @apply flex flex-col m-4 rounded-lg border-l-4 p-4;
}
.markdown >>> pre, .markdown >>> code {
  font-family: monospace, monospace;
}
.markdown >>> pre {
  overflow: auto;
  background: linear-gradient(155deg, rgb(248, 172, 213) 30%, rgb(192, 126, 191) 70%);
  box-shadow: 4px 4px 10px -1px rgba(104, 0, 95, 0.5);
  border-color: rgba(241, 55, 151, 0.9);
  @apply flex m-4 rounded-lg border-l-4 text-base p-4;
}
.dark .markdown >>> blockquote, .dark .markdown >>> pre {
  background: linear-gradient(155deg, rgb(117, 42, 81) 30%, rgb(88, 33, 87) 70%);
}
.markdown >>> pre code {
  @apply text-primary-10 !important;
}
.markdown >>> .codeWrap{
  margin: 2rem;
  display: flex;
}
.markdown >>> .codeWrap:after{
  content: "";
  width: 2rem;
}
.markdown >>> .indent{
  display: inline-block;
  width: 3ch;
}
.markdown >>> .newpage{
  display: block;
  height: 5em;
}
.markdown >>> .qed{
  float: right;
}

@screen sm {
  .markdown {
    @apply leading-relaxed text-xl;
  }
  .markdown >>> h1 {
    @apply text-4xl;
  }
  .markdown >>> h2 {
    @apply text-3xl;
  }
  .markdown >>> h3 {
    @apply text-2xl;
  }
  .markdown >>> h4{
    @apply text-xl;
  }
  .markdown >>> pre {
    @apply text-lg;
  }
}
</style>