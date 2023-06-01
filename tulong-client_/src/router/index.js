const Home = () => import('@/views/home');
// const Upload = () => import('@/views/upload');
const Platform = () => import('@/views/platform');
export default [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Tulong|首页',
    },
  },
  // {
  //   path: "/upload",
  //   name: "Upload",
  //   component: Upload,
  //   meta: {
  //     title: "Tulong|上传"
  //   }
  // },
  {
    path: '/platform',
    name: 'Platform',
    component: Platform,
    meta: {
      title: 'Tulong|平台',
    },
  },
];
