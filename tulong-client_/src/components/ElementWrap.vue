<template>
  <div class="element-wrap">
    <h3 class="title-wrap">当前项目</h3>
    <div class="element-list">
      <li
        class="element-row"
        v-for="(extractImg, idx) in extractImgList"
        :class="currentImgId == extractImg.id ? 'chosen' : ''"
        @click="handleItemClick(extractImg.id)"
        @mouseover="handleItemMouseOver(idx)"
        @mouseout="handleItemMouseOut(idx)"
        :key="idx"
      >
        <div class="item-box row">
          <div class="icon">
            <i :style="{ backgroundImage: `url(${extractImg.url})` }" />
          </div>
          <span>{{ extractImg.name }}</span>
        </div>
        <div
          v-show="hoverList[idx]"
          @click.stop="handleRemoveClick(extractImg.id)"
          class="remove-btn"
        >
          ×
        </div>
      </li>
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      hoverList: [],
    };
  },
  watch: {
    extractImgList(newVal) {
      this.hoverList = new Array(newVal.length).fill(false);
    },
  },
  computed: {
    ...mapState(['extractImgList', 'currentImgId']),
  },
  methods: {
    ...mapActions(['focusImgTarget', 'removeImgTarget']),
    handleItemClick(id) {
      this.focusImgTarget(id);
    },
    handleItemMouseOver(idx) {
      this.$set(this.hoverList, idx, true);
      // this.hoverList[idx] = true;
    },
    handleItemMouseOut(idx) {
      this.$set(this.hoverList, idx, false);
      // this.hoverList[idx] = false;
    },
    handleRemoveClick(id) {
      this.removeImgTarget(id);
      this.focusImgTarget(null);
    },
  },
};
</script>
<style lang="scss">
.element-wrap {
  display: flex;
  flex-direction: column;
  width: 240px;
  height: 100%;
  overflow: hidden;
  background-color: #f7f7f7;
  border-right: solid 1px #d0d0d0;
}
.element-list {
  flex: 1;
  overflow-y: auto;
}
.element-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px;
  height: 64px;
  border-bottom: solid 1px #efefef;
  &:hover {
    background-color: #f1f9fe;
  }
  &.chosen {
    background-color: #e9f2fa;
  }
}
.item-box {
  color: #666;
  .icon {
    position: relative;
    width: 48px;
    height: 48px;
    background-size: cover;
    background-image: url(../assets/img/icon-bg.png);
    border: solid 1px #d0d0d0;
    margin-right: 8px;
    > i {
      position: absolute;
      left: 0;
      top: 0;
      display: block;
      width: 100%;
      height: 100%;
      background-position: center;
      background-size: contain;
      background-repeat: no-repeat;
    }
  }
}
.remove-btn {
  color: #666;
  font-size: 22px;
  cursor: pointer;
}
</style>
