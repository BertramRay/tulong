import { Message as $message } from 'element-ui';
import { postData } from '@/common/net';
import API from '@/api';

// 公共请求
const actions = {
  // 上传设计稿图片
  async uploadUIImage({ commit }, data) {
    const res = await postData(API.POST_UPLOAD, data);
    commit('artboardImgUrl', res.data.url);
    return res;
  },
  initArtboard({ commit }, url) {
    commit('setArtboardImgUrl', url);
    commit('setExtractImgList', []);
  },
  async extract({ dispatch }, data) {
    try {
      const res = await postData(API.POST_EXTRACT, data);
      dispatch('addImgTargetList', res.data.out_rects);
    } catch (error) {
      if (error.code) {
        $message({
          message: '服务异常，请稍后再试！',
          type: 'error',
        });
      } else {
        $message({
          message: '服务异常，请稍后再试！',
          type: 'error',
        });
        throw error;
      }
    }
  },
  async styleDetect({ state, dispatch }, data) {
    try {
      const res = await postData(API.POST_STYLE_DETECT, data);
      dispatch('setImgTargetStyle', {
        id: state.currentImgId,
        style: res.data.style_data,
      });
    } catch (error) {
      if (error.code) {
        $message({
          message: '服务异常，请稍后再试！',
          type: 'error',
        });
      } else {
        $message({
          message: '服务异常，请稍后再试！',
          type: 'error',
        });
        throw error;
      }
    }
  },
  focusImgTarget({ commit }, id) {
    commit('setCurrentImgId', id);
  },
  addImgTargetList({ commit, state }, data) {
    const list = [...data, ...state.extractImgList];
    commit('setExtractImgList', list);
  },
  setImgTargetStyle({ commit, state }, { id, style }) {
    const list = [...state.extractImgList];
    const idx = list.findIndex((item) => item.id === id);
    console.log('idx', idx);
    // eslint-disable-next-line no-bitwise
    if (!~idx) return;
    list[idx] = {
      ...list[idx],
      style,
    };
    commit('setExtractImgList', list);
  },
  removeImgTarget({ commit, state }, id) {
    const list = state.extractImgList.filter((item) => item.id !== id);
    commit('setExtractImgList', list);
  },
};

export default actions;
