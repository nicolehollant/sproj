<template>
    <div class="navbar">
        <nav class="navbar--link__wrapper">
            <router-link exact to="/" class="navbar--link">Home</router-link>
            <router-link to="/thesaurus" class="navbar--link">Thesaurus</router-link>
            <router-link to="/model" class="navbar--link">Model</router-link>
        </nav>
    </div>
</template>

<style lang="postcss">
.navbar {
    border-top: 4px solid rgba(216, 69, 145, 1);
    background-color: rgb(117, 42, 81);
    @apply w-full shadow-lg p-8;
}
.navbar--link__wrapper {
    @apply m-auto max-w-5xl flex justify-around items-center;
}
.navbar--link{
    color: rgb(63, 17, 40);
    @apply text-xl cursor-pointer;
}
.router-link-active{
    @apply text-pink-100 font-semibold;
}
</style>
