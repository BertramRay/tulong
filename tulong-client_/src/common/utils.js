export async function saveImgFile(file) {
  return new Promise(resolve => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = res => {
      localStorage.setItem('artboardImg', res);
      resolve();
    };
  });
}
export async function getImgFile() {
  return new Promise(resolve => {
    const imgData = localStorage.getItem('artboardImg');
    const img = new Image();
    img.src = imgData;
    img.onload = () => {
      resolve();
    };
  });
}
