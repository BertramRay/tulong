<template>
  <canvas
    ref="artboardCanvas"
    class="artboard-wrap"
    :style="{
      width: width + 'px',
      height: height + 'px',
    }"
    :width="width * 2"
    :height="height * 2"
  />
</template>
<script>
export default {
  data() {
    return {
      canvas: null,
      ctx: null,
    };
  },
  props: ['width', 'height', 'artboardImg', 'extractImgList', 'currentImgId'],
  mounted() {
    this.canvas = this.$refs.artboardCanvas;
    this.initCanvas();
    this.ctx = this.canvas.getContext('2d');
    this.updateCanvas();
  },
  updated() {
    this.updateCanvas();
  },
  watch: {
    extractImgList() {
      this.updateCanvas();
    },
    currentImgId() {
      this.updateCanvas();
    },
  },
  methods: {
    initCanvas() {},
    drawArtboard() {
      const { ctx, artboardImg, width, height } = this;
      ctx.drawImage(artboardImg, 0, 0, width, height);
    },
    drawFrames() {
      const { ctx, extractImgList, currentImgId } = this;
      if (!extractImgList.length) return;
      extractImgList.forEach(({ x, y, w, h, id }) => {
        if (id === currentImgId) {
          ctx.strokeStyle = '#00aadd';
          ctx.lineWidth = 2;
        } else {
          ctx.strokeStyle = '#888';
          ctx.lineWidth = 1;
        }
        ctx.strokeRect(x * 0.5, y * 0.5, w * 0.5, h * 0.5);
      });
    },
    updateCanvas() {
      console.log('canvas updated');
      const { ctx, width, height } = this;
      if (!ctx) return;
      ctx.save();
      ctx.scale(2, 2);
      ctx.clearRect(0, 0, width, height);
      this.drawArtboard();
      this.drawFrames();
      ctx.restore();
    },
  },
};
</script>
<style lang="scss"></style>
