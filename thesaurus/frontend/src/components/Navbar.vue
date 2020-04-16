<template>
    <div class="navbar">
        <nav class="navbar--link__wrapper">
            <router-link aria-label="Home" exact to="/" class="navbar--link">Home</router-link>
            <router-link aria-label="Thesaurus" to="/thesaurus" class="navbar--link">Thesaurus</router-link>
            <router-link aria-label="Model" to="/model" class="navbar--link">Model</router-link>
            <router-link aria-label="Writing" to="/writing" class="navbar--link">Writing</router-link>
        </nav>
        <nav class="navbar--link__wrapper-mobile">
                <router-link aria-label="Home" exact to="/" class="navbar--link">
                    <fa-icon icon="home" />
                </router-link>
                <router-link aria-label="Thesaurus" to="/thesaurus" class="navbar--link">
                    <fa-icon icon="spell-check" />
                </router-link>
                <router-link aria-label="Model" to="/model" class="navbar--link">
                    <fa-icon icon="edit" />
                </router-link>
                <router-link aria-label="Writing" to="/writing" class="navbar--link">
                    <fa-icon icon="book" />
                </router-link>
        </nav>
    </div>
</template>

<style lang="postcss">
.navbar {
    border-top: 4px solid var(--primary-50);
    @apply w-full shadow-lg p-6 bg-primary-90;
}
.navbar--link__wrapper, .navbar--link__wrapper-mobile {
    @apply m-auto max-w-5xl flex justify-around items-center;
}
.navbar--link__wrapper {
    @apply hidden;
}
.navbar--link {
    transition-duration: 150ms;
    @apply text-xl cursor-pointer text-primary-20 px-1 rounded;
}
.navbar--link:focus {
    @apply outline-none bg-primary-80 text-secondary-10
}
.router-link-active{
    @apply text-secondary-20 font-semibold;
}
@screen sm {
    .navbar {
        @apply p-8;
    }
    .navbar--link__wrapper-mobile {
        @apply hidden;
    }
    .navbar--link__wrapper {
        @apply flex;
    }
}
</style>
