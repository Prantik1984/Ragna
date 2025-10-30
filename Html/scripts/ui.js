const dropZone  = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadBtn');
const dialog = document.getElementById('dialog');
const apiUrl="http://127.0.0.1:9000"
const loadingOverlay = document.getElementById('loadingOverlay');

function setLoading(isLoading) {
  loadingOverlay.classList.toggle('hidden', !isLoading);
  uploadBtn.disabled = isLoading;
  dropZone.classList.toggle('opacity-60', isLoading);
  dropZone.style.pointerEvents = isLoading ? 'none' : 'auto';
}

function showDialog(title, message, isError = false) {
  // dialogTitle.textContent = title;
  // dialogMessage.textContent = message;

  // // Color style based on error/success
  // dialogTitle.className = isError ? 'text-red-600 text-xl font-semibold mb-2'
  //                                 : 'text-green-600 text-xl font-semibold mb-2';

  dialog.classList.remove('hidden');
}

dialogClose.addEventListener('click', () => {
  dialog.classList.add('hidden');
});

function showSection(id) {
  document.querySelectorAll('#home, #documents, #settings, #help')
    .forEach(el => el.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
}



dropZone.addEventListener('click', () => fileInput.click());

uploadButton.addEventListener('click',async()=>{
  const files = fileInput.files;
  if (!files.length) {
    
    return;
  }

  var uploadableFile=files[0];

  const formData = new FormData();
  formData.append('file', uploadableFile, uploadableFile.name);
  setLoading(true);
  try
  {
    const response = await fetch(apiUrl+'/upload/pdfs', {
      method: 'POST',
      body: formData
    });
   // setLoading(false);
  }
  catch (error) {
     // setLoading(false);
      showDialog("","");
  }
});