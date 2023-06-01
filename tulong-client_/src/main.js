import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import { Button, Upload, Message } from 'element-ui';
import routers from './router';
import store from './store';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App';

Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(Upload);
Vue.use(Button);
Vue.component(Message.name, Message);
Vue.prototype.$message = Message;
const router = new VueRouter({
  mode: 'history',
  routes: routers,
});

new Vue({
  store,
  router,
  render: (h) => h(App),
}).$mount('#app');
