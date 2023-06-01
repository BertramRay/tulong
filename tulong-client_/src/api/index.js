import config from '../../config';
// eslint-disable-next-line no-undef
const $$ = config[NODE_ENV].api;
export default {
  POST_UPLOAD: `${$$}/upload`,
  POST_EXTRACT: `${$$}/extract`,
  POST_STYLE_DETECT: `${$$}/detect`,
};
