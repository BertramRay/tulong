<template>
  <div class="bg-box">
    <span v-if="name" class="attr-name">{{ name }}</span>
    <span class="attr-val" :style="bgBoxStyle"></span>
  </div>
</template>
<script>
export default {
  props: ['name', 'val', 'type'],
  computed: {
    bgBoxStyle() {
      const style = {};
      switch (this.type) {
        case 'image':
          style.backgroundImage = `url(${this.val})`;
          break;
        case 'color':
          style.backgroundColor = `rgba(${this.val.join(',')}`;
          break;
        default:
          break;
      }
      return style;
    },
  },
};
</script>
<style lang="scss">
.bg-box {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #999;
  margin-right: 12px;
  .attr-name {
    margin-right: 8px;
  }
  .attr-val {
    width: 18px;
    height: 12px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    border: solid 1px #999;
    border-radius: 2px;
  }
}
</style>
