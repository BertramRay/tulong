<template>
  <div class="platfrom-wrap">
    <element-wrap />
    <div class="preview">
      <preview
        v-if="imgLoaded"
        :artboard-img="artboardImg"
        @chooseArea="handleChooseArea"
      />
    </div>
    <attribute-panel />
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex';
import { ElementWrap, Preview, AttributePanel } from '@/components';

export default {
  components: {
    ElementWrap,
    Preview,
    AttributePanel,
  },
  data() {
    return {
      imgLoaded: false,
      artboardImg: new Image(),
    };
  },
  created() {
    this.loadImg();
  },
  computed: {
    ...mapState(['artboardImgUrl']),
  },
  methods: {
    ...mapActions(['extract']),
    loadImg() {
      if (!this.artboardImgUrl) return;
      console.log('loading img');
      this.imgLoaded = false;
      this.artboardImg.onload = () => {
        this.imgLoaded = true;
        console.log('loaded img');
      };
      this.artboardImg.src = this.artboardImgUrl;
    },
    handleChooseArea(frame) {
      this.extract({ frame });
    },
  },
  watch: {
    artboardImgUrl() {
      this.loadImg();
    },
  },
};
</script>
<style lang="scss">
.platfrom-wrap {
  display: flex;
  height: 100%;
}
.preview {
  display: flex;
  justify-content: center;
  padding: 24px 0;
  box-sizing: border-box;
  overflow-y: auto;
  flex: 1;
  height: 100%;
  background-color: #e4e4e4;
}
</style>
