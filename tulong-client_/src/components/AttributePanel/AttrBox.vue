<template>
  <div class="attr-box">
    <span v-if="name" class="attr-name">{{ name }}</span>
    <span class="attr-val">
      <slot />
    </span>
  </div>
</template>
<script>
export default {
  props: ['name'],
};
</script>
<style lang="scss">
.attr-box {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #999;
  margin-right: 12px;
  .attr-name {
    margin-right: 8px;
  }
  .attr-val {
    color: #666;
  }
}
</style>
