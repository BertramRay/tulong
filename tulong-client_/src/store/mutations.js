/* eslint-disable no-param-reassign */

const mutations = {
  setArtboardImgUrl(state, val) {
    state.artboardImgUrl = val;
  },
  setExtractImgList(state, val) {
    state.extractImgList = val;
  },
  setCurrentImgId(state, val) {
    state.currentImgId = val;
  },
};
export default mutations;
