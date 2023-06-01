<template>
  <div id="app">
    <header-bar />
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
import { HeaderBar } from '@/components';

export default {
  name: 'App',
  components: {
    HeaderBar,
  },
  data() {
    return {};
  },
};
</script>

<style>
@import './css/common.scss';
html,
body,
#app {
  height: 100%;
}
#app {
  display: flex;
  flex-direction: column;
}
.container {
  flex: 1;
  overflow-y: auto;
}
</style>
