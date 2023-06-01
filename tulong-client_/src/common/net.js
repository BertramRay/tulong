import axios from 'axios';

axios.defaults.timeout = 15000;
axios.defaults.withCredentials = true;
async function postData(url, data = null) {
  // commit('fetch_loading', { name });
  // try {
  // const formdata = new FormData();
  // for (let key in data) {
  //     formdata.append(key, data[key]);
  // }
  const { data: resBody } = await axios.post(url, data);
  console.log(resBody);
  if (resBody.code === '00000') {
    return resBody;
  }
  throw resBody;
  // } catch (err) {
  //     throw err;
  // }
}
async function getData(url, data = null) {
  let queryStrings = data ? ['?'] : '';
  if (queryStrings) {
    Object.keys(data).forEach((key) => {
      queryStrings.push(`${key}=${data[key]}`);
      queryStrings.push('&');
    });
    queryStrings = queryStrings.slice(0, -1).join('');
  }
  // try {
  const { data: resBody } = await axios.get(url + queryStrings);
  if (resBody.code === '00000') {
    return resBody;
  }
  throw resBody;
  // } catch (err) {
  //     throw err;
  // }
}
export { postData, getData };
