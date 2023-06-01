<template>
  <header class="header">
    <router-link to="/home" class="row">
      <div class="logo"></div>
      <h1 class="title">Tulong</h1>
    </router-link>
    <el-upload
      v-if="$route.name == 'Platform'"
      accept="image/jpg, image/jpeg, image/png"
      :show-file-list="false"
      :action="API.POST_UPLOAD"
      :on-error="handleError"
      :before-upload="handleBeforeUpload"
      :on-success="forward"
    >
      <el-button>重新上传</el-button>
    </el-upload>
  </header>
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
      this.$router.go();
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
.header {
  display: flex;
  justify-content: space-between;
  padding: 0 32px;
  height: 72px;
  align-items: center;
  background-color: #f7f7f7;
  border-bottom: solid 1px #d0d0d0;
  color: #666;
  box-shadow: 0 1px 18px rgba($color: #000000, $alpha: 0.1);
}
.logo {
  width: 56px;
  height: 56px;
  background-image: url(../assets/img/logo.png);
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
.title {
  font-size: 32px;
  color: #f7f7f7;
  letter-spacing: 2px;
  text-shadow: 0 1.5px #2a3242, 1.5px 0 #2a3242, -1.5px 0 #2a3242,
    0 -1.5px #2a3242;
}
</style>
