<template>
  <div class="about text-pink-200">
    <Navbar/>
    <div class="px-6 py-4 text-left max-w-3xl m-auto">
      <h1 class="font-bold text-2xl text-purple-100 mt-4 mb-6 text-center">Arbitrary Replacement Results</h1>
      <h2>Original:</h2>
      <p>
        To be or not to be that is the question Whether tis nobler in the mind to suffer The slings and arrows of outrageous fortune Or to take Arms against a Sea of troubles And by opposing end them to die to sleep No more and by a sleep to say we end The heart ache and the thousand natural shocks That Flesh is heir to Tis a consummation Devoutly to be wished
      </p>
      <h2>Changed:</h2>
      <div class="result-entry">
        <p>
          To be american state not to atomic number 4 that letter the challenge Whether tis nobler hoosier state the care to get The weapon system and arrows of outrageous fate Or to abide Arms against a Sea of pregnancy And by opposing cease them to snuff it to sleep No more and by a sleep late to convey we end The warmheartedness suffer and the thousand achiever shocks That form ace heir to Tis a consummation Devoutly to be wished
        </p>
      </div>
      <div class="result-entry">
        <p>
          To be or non to atomic number 4 that is the question Whether tis nobler metallic element the mind to support The slingshot and arrows of exorbitant luck Or to be intimate instrumentation against vitamin a Sea of natural event And by opposed end them to die to sleep No more and by fat-soluble vitamin sleep to say we content The tenderness perceive and the m natural shocks That Flesh 1 heir to Tis a mop up Devoutly to be wished
        </p>
      </div>
      <div class="result-entry">
        <p>
          To be beaver state non to be that iodin the reflect Whether tis nobler in the take care to suffer The catapult and arrows of outrageous fortune Or to take Arms against a Sea of strike And by opposing end them to cash in one's chips to rest element more and past a sleep to express we section The heart yearn and the thousand natural shocks That physique is heir to Tis a windup piously to be express
        </p>
      </div>

      <h2>Original:</h2>
      <div class="result-entry">
        <p>
          Freeman and slave patrician and plebeian lord and serf guild master and journeyman in a word oppressor and oppressed stood in constant opposition to one another carried on an uninterrupted now hidden now open fight a fight that each time ended either in a revolutionary re constitution of society at large or in the common ruin of the contending classes 
        </p>
        <p>
          In the earlier epochs of history we find almost everywhere a complicated arrangement of society into various orders a manifold gradation of social rank In ancient Rome we have patricians knights plebeians slaves in the Middle Ages feudal lords vassals guild masters journeymen apprentices serfs in almost all of these classes again subordinate gradations
        </p>
      </div>
      <h2>Changed:</h2>
      <div class="result-entry">
        <p>
          citizen and worker noble and plebeian nobleman and villein lodge master and skilled worker in a order oppressor and burdened stood in constant opposition to one another carried on an uninterrupted today unseeable now undefendable fight purine engagement that each time ended either in a revolutionary rhenium constitution of society at magnanimous operating theatre indiana the communal ruin of the competitive classes 
        </p>
        <p>
          In the earlier epochs of history we get word almost everyplace a complicated arrangement of society into various orders antiophthalmic factor manifold gradation of gregarious rank In ancient Rome we have aristocrat knights plebeians slaves in the Middle Ages feudal lords follower guild masters journeymen apprentices serfs in most all of these classes again subordinate gradations
        </p>
      </div>
      <div class="result-entry">
        <p>
          Freeman and mortal patrician and vulgar godhead and serf lodge passe-partout and journeyman in a word oppressor and oppressed stood in constant opposition to one another carried along an continual straightaway hidden now open fight antiophthalmic factor tilt that each time concluded either fashionable ampere subverter re constitution of social group at large operating theatre in the common destroy of the contending classes 
        </p>
        <p>
          In the in the beginning epochs of history we find almost everywhere a complicated arrangement of society into various orders ampere manifold grade of friendly rank stylish ancient Rome we give birth adult knights common person slaves in the center Ages feudal lords vassals guild masters journeymen learner serfs metal nearly all of these classes over again subordinate gradations
        </p>
      </div>
      <div class="result-entry">
        <p>
          freewoman and break one's back patrician and plebeian lord and villein association student and journeyman in a word unpleasant person and oppressed stood inch uninterrupted foe to incomparable another carried along associate degree constant now hidden present afford fight a press that all moment complete either in vitamin a revolutionist re constitution of society element large or in the common ruin of the contending classes 
        </p>
        <p>
          fashionable the early epochs of history we feat almost all over a complicated group of society into various orders vitamin a manifold gradation of social rank atomic number 49 ancient Rome we have patricians chessman plebeians slaves linear unit the Middle Ages feudal lords follower guild masters journeymen apprentices serfs in most all of these classes again subordinate gradations
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
export default {
  components: {
    Navbar
  }
}
</script>

<style lang="postcss" scoped>
h2{
  @apply font-bold text-xl text-purple-300 mt-4 mb-1;
}
p::before {
  content: "";
  width: 1.5ch;
  display: inline-block;
}
p{
  @apply text-lg;
}
.result-entry {
  @apply mb-8;
}
</style>