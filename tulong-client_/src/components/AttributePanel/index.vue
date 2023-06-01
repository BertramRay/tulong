<template>
  <div class="attr-wrap" v-if="currentImg">
    <h3 class="title-wrap">节点属性</h3>
    <section>
      <h4 class="subtitle-wrap">预览</h4>
      <div class="pic-wrap">
        <div
          class="icon"
          :style="{
            height: `${(currentImg.h * 200) / currentImg.w}px`,
          }"
        >
          <i
            :style="{
              backgroundImage: `url(${currentImg.url})`,
            }"
          ></i>
        </div>
        <el-button @click="handleDownloadClick">下载图片</el-button>
      </div>
    </section>
    <section>
      <h4 class="subtitle-wrap">尺寸</h4>
      <div class="attr-row">
        <attr-box name="X">{{ currentImg.x }}</attr-box>
        <attr-box name="Y">{{ currentImg.y }}</attr-box>
        <attr-box name="宽">{{ currentImg.w }}</attr-box>
        <attr-box name="高">{{ currentImg.h }}</attr-box>
      </div>
    </section>
    <section>
      <h4 class="subtitle-wrap">外观</h4>
      <div v-if="!currentImg.style" class="attr-row">
        <el-button size="small" @click="handleStyleDetectClick">
          样式检测
        </el-button>
      </div>
      <template v-else>
        <!-- 背景&圆角样式 -->
        <div class="attr-row">
          <bg-box
            v-if="currentImg.style.backgroundColor"
            name="背景：填充"
            type="color"
            :val="currentImg.style.backgroundColor"
          />
          <bg-box v-else name="背景：图片" type="image" :val="currentImg.url" />
          <attr-box v-if="currentImg.style.borderRadius" name="圆角">
            {{ currentImg.style.borderRadius.join(', ') }}
          </attr-box>
        </div>
        <!-- 边框样式 -->
        <div class="attr-row" v-if="currentImg.style.borderWidth">
          <attr-box name="描边：厚度">{{
            currentImg.style.borderWidth
          }}</attr-box>
          <bg-box
            name="填充"
            type="color"
            :val="currentImg.style.borderColor"
          />
        </div>
      </template>
    </section>
    <section>
      <h4 class="subtitle-wrap">字体</h4>
      <div v-if="!currentImg.textStyle" class="attr-row">
        <el-button disabled size="small" @click="handleTextStyleDetectClick">
          文字检测（待开放）
        </el-button>
      </div>
      <template v-else>
        <div class="attr-row"></div>
      </template>
    </section>
    <section>
      <h4 class="subtitle-wrap">样式代码</h4>
      <div class="attr-row">
        <el-button disabled size="small" @click="handleCodeDetectClick">
          生成css代码（待开放）
        </el-button>
      </div>
    </section>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import AttrBox from './AttrBox';
import BgBox from './BgBox';

export default {
  data() {
    return {};
  },
  components: {
    AttrBox,
    BgBox,
  },
  computed: {
    ...mapGetters(['currentImg']),
  },
  methods: {
    ...mapActions(['styleDetect']),
    handleDownloadClick() {
      const link = document.createElement('a');
      link.download = this.currentImg.id;
      link.href = this.currentImg.url;
      link.click();
    },
    handleStyleDetectClick() {
      this.styleDetect({ img_id: this.currentImg.id });
    },
    handleTextStyleDetectClick() {},
    handleCodeDetectClick() {},
  },
};
</script>
<style lang="scss">
.attr-wrap {
  width: 320px;
  height: 100%;
  background-color: #f7f7f7;
  border-left: solid 1px #d0d0d0;
  > section {
    border-bottom: solid 2px #efefef;
    padding-bottom: 12px;
  }
}
.attr-row {
  display: flex;
  align-items: center;
  padding-left: 20px;
  padding-bottom: 6px;
}
.pic-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  .icon {
    position: relative;
    width: 200px;
    background-size: cover;
    background-image: url(../../assets/img/icon-bg.png);
    border: solid 1px #d0d0d0;
    margin-bottom: 8px;
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
</style>
