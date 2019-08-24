import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueRouter from 'vue-router'

import App from './App.vue'
import NodeLinkGraph from './components/NodeLinkGraph'
import HeatmapGraph from './components/HeatmapGraph'



Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(VueRouter)

var router = new VueRouter({
  routes: [
    { path: '/home', component: NodeLinkGraph },
    { path: '/heatmap', component: HeatmapGraph },
    { path:'/', redirect:'/home' }
  ]
});

new Vue({
  render: h => h(App),
  router: router
}).$mount('#app')
