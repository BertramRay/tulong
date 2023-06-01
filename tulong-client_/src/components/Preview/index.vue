<template>
  <div
    class="preview-wrap"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    :style="{
      height: artboardImg.height * scale + 'px',
    }"
  >
    <artboard
      :artboardImg="artboardImg"
      :extractImgList="extractImgList"
      :currentImgId="currentImgId"
      :width="artboardImg.width * scale"
      :height="artboardImg.height * scale"
      class="artboard"
    />
    <div
      v-show="showSelectFrame"
      class="select-box"
      :style="{
        left: frame.x * scale + 'px',
        top: frame.y * scale + 'px',
        width: frame.w * scale + 'px',
        height: frame.h * scale + 'px',
      }"
    ></div>
  </div>
</template>
<script>
import { mapState } from 'vuex';
import Artboard from './Artboard';

const SCALE = 0.5;
const TH = 5;
const getOffset = (e) => {
  const rect = e.currentTarget.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;
  // let boundRight = rect.width + rect.left,
  //     boundBottom = rect.height + rect.top;
  // offsetX = offsetX < 0 ?  0 : offsetX;
  // offsetY = offsetY < 0 ?  0 : offsetY;
  // offsetX = offsetX > boundRight ?  boundRight : offsetX;
  // offsetY = offsetY > boundBottom ?  boundBottom : offsetY;
  return [offsetX, offsetY];
};
export default {
  data() {
    return {
      scale: SCALE,
      showSelectFrame: false,
      showLocateFrame: false,
      selectFrame: {
        sx: 0,
        sy: 0,
        ex: 0,
        ey: 0,
      },
      mouseControl: {
        down: false,
        move: false,
      },
    };
  },
  props: ['artboardImg'],
  components: {
    Artboard,
  },
  computed: {
    ...mapState(['extractImgList', 'currentImgId']),
    frame() {
      const { scale, selectFrame } = this;
      const { sx, sy, ex, ey } = selectFrame;
      const x = Math.min(sx, ex);
      const y = Math.min(sy, ey);
      return {
        x: x / scale,
        y: y / scale,
        w: (Math.max(sx, ex) - x) / scale,
        h: (Math.max(sy, ey) - y) / scale,
      };
    },
    checkFrame() {
      return this.frame.w > TH && this.frame.h > TH;
    },
  },
  methods: {
    handleMouseDown(e) {
      this.showSelectFrame = false;
      this.mouseControl.down = true;
      const [offsetX, offsetY] = getOffset(e);
      this.selectFrame.sx = offsetX;
      this.selectFrame.sy = offsetY;
    },
    handleMouseMove(e) {
      if (!this.mouseControl.down) return;
      this.mouseControl.move = true;
      const [offsetX, offsetY] = getOffset(e);
      this.selectFrame.ex = offsetX;
      this.selectFrame.ey = offsetY;
      this.showSelectFrame = true;
    },
    handleMouseUp() {
      if (this.mouseControl.move && this.checkFrame) {
        this.$emit('chooseArea', this.frame);
      }
      this.mouseControl.move = false;
      this.showSelectFrame = false;
      this.mouseControl.down = false;
    },
  },
};
</script>
<style lang="scss">
.preview-wrap {
  position: relative;
}
.select-box {
  position: absolute;
  border: solid 2px #00aadd;
  background-color: rgba(#00aadd, 0.1);
  // box-sizing: border-box;
}
</style>
