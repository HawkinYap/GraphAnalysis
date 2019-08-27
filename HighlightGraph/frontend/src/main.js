import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueRouter from 'vue-router'

import App from './App.vue'
import Home from './components/Home'
import Introduction from './components/Introduction'
import NodeLinkGraph from './components/NodeLinkGraph'
import Test from './components/Test'
import HeatmapGraph from './components/HeatmapGraph'



Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(VueRouter)

var router = new VueRouter({
  routes: [
    { path: '/intro', name: 'intro', component: Introduction},
    { path: '/nodelink', name: 'nodelink', component: NodeLinkGraph },
    { path: '/test', name: 'test', component: Test },
    { path: '/heatmap', name: 'heatmap', component: HeatmapGraph },
    { path: '/home', name: 'home', component: Home },
    { path:'/', redirect:'/home' }
  ]
});

new Vue({
  render: h => h(App),
  router: router
}).$mount('#app')
