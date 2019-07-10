<template>
    <div class="wrapper w-full shadow-lg p-8">
        <header class="m-auto max-w-5xl flex align-center justify-around items-center">
            <router-link exact to="/" class="navlink">Home</router-link>
            <router-link to="/thesaurus" class="navlink">Thesaurus</router-link>
            <router-link to="/about" class="navlink">About</router-link>
        </header>
    </div>
</template>

<style lang="postcss">

.navlink{
    color: rgb(63, 17, 40);
    @apply text-xl font-hairline cursor-pointer;
}
.router-link-active{
    @apply text-pink-100 font-semibold;
}
.wrapper{
    background-color: rgb(117, 42, 81);
}
</style>
