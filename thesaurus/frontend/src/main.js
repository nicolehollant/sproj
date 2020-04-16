import Vue from 'vue'
import App from './App.vue'
import router from './router'
import '@/assets/css/tailwind.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faSpellCheck, faHome, faBook, faEdit, faBars, faInfoCircle, faSun, faMoon, faChevronDown } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import ClickOutside from 'vue-click-outside'
import VueCompositionApi from '@vue/composition-api'

library.add(faUserSecret, faSpellCheck, faHome, faBook, faEdit, faBars, faInfoCircle, faSun, faMoon, faChevronDown)

Vue.component('fa-icon', FontAwesomeIcon)
Vue.directive('on-click-outside', ClickOutside)

Vue.use(VueCompositionApi)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
