<template>
  <div class="home-wrap">
    <h1>组件样式检测工具</h1>
    <p>Tulong，一款为开发切图准备的，面向图片的UI样式检测平台</p>
    <div class="banner"></div>
    <div class="btn-group">
      <el-upload
        class="btn-upload"
        accept="image/jpg, image/jpeg, image/png"
        :show-file-list="false"
        :action="API.POST_UPLOAD"
        :on-error="handleError"
        :before-upload="handleBeforeUpload"
        :on-success="forward"
      >
        <el-button round type="primary">上传图片体验</el-button>
        <p slot="tip">只能上传jpg/png文件，且不超过10M</p>
      </el-upload>
    </div>
    <h2>产品特色</h2>
    <ul class="feature-list">
      <li class="feature-item">
        <i class="icon-crop"></i>
        <h3>辅助抠图</h3>
        <p>可通过框选高效抠图</p>
      </li>
      <li class="feature-item">
        <i class="icon-shape"></i>
        <h3>样式检测</h3>
        <p>支持组件样式识别</p>
      </li>
      <li class="feature-item">
        <i class="icon-ocr"></i>
        <h3>文字识别</h3>
        <p>支持OCR和文字样式识别</p>
      </li>
      <li class="feature-item">
        <i class="icon-code"></i>
        <h3>代码复制</h3>
        <p>自动生成组件代码</p>
      </li>
    </ul>
  </div>
</template>
<script>
import { mapActions } from 'vuex';
import API from '@/api';

export default {
  data() {
    return {
      API,
    };
  },
  methods: {
    ...mapActions(['initArtboard']),
    forward(res) {
      this.initArtboard(res.data.url);
      this.$router.push({ path: 'platform' });
    },
    handleError() {
      this.$message('上传图片失败');
    },
    handleBeforeUpload(file) {
      const isLt = file.size / 1024 / 1024 < 10;
      if (!isLt) this.$message('图片大小不能超过10M!');
    },
  },
};
</script>
<style lang="scss">
.home-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  > h1 {
    font-size: 34px;
    color: #2a3242;
  }
  > h2 {
    font-size: 28px;
    color: #2a3242;
  }
  > p {
    font-size: 18px;
    line-height: 28px;
    color: #999;
    margin: 10px 0;
  }
  .banner {
    width: 800px;
    height: 450px;
    background-image: url(../assets/img/banner.png);
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
  }
}
.btn-group {
  p {
    margin-top: 8px;
    color: #999;
    font-size: 12px;
  }
}
.btn-upload {
  padding: 20px 0 36px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.feature-list {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  .feature-item {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: solid 1px #dfdfdf;
    border-radius: 4px;
    width: 200px;
    height: 200px;
    margin: 0 10px;
    padding: 15px 0;
    > i {
      display: block;
      width: 64px;
      height: 64px;
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
      &.icon-crop {
        background-image: url(../assets/img/icon-crop.png);
      }
      &.icon-shape {
        background-image: url(../assets/img/icon-shape.png);
      }
      &.icon-ocr {
        background-image: url(../assets/img/icon-ocr.png);
      }
      &.icon-code {
        background-image: url(../assets/img/icon-code.png);
      }
    }
    > h3 {
      color: #2a3242;
      font-size: 18px;
      margin: 12px 0 6px 0;
    }
    > p {
      color: #999;
      font-size: 14px;
    }
  }
}
</style>
