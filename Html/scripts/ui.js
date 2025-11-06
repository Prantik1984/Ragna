const dropZone  = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadBtn');
const dialog = document.getElementById('dialog');
const apiUrl="http://127.0.0.1:9000"
const loadingOverlay = document.getElementById('loadingOverlay');
function showLoading(isLoading) {
  loadingOverlay.classList.toggle('hidden', !isLoading);
  uploadButton.disabled = isLoading;
  dropZone.classList.toggle('opacity-60', isLoading);
  dropZone.style.pointerEvents = isLoading ? 'none' : 'auto';
}

function showDialog(title, message, isError = false) {
  dialogTitle.textContent = title;
  dialogMessage.textContent = message;

  // Color style based on error/success
  dialogTitle.className = isError ? 'text-red-600 text-xl font-semibold mb-2'
                                  : 'text-green-600 text-xl font-semibold mb-2';

  dialog.classList.remove('hidden');
}

dialogClose.addEventListener('click', () => {
  dialog.classList.add('hidden');
});

function showSection(id) {
  document.querySelectorAll('#home, #documents, #settings, #help, #querry')
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
  showLoading(true);
  try
  {
    const response = await fetch(apiUrl+'/upload/pdfs', {
      method: 'POST',
      body: formData
    });
    const json = await response.json();
    showLoading(false);
    if (json["uploaded"]==true)
    {
      showUploadedDocuments(json["id"]);
    }
    else
    {
      showDialog("Error uploading file",error,true);
    }
    
    
  }
  catch (error) {
      console.log(error);
      showLoading(false);
      showDialog("Error uploading file",error,true);
  }
});

function showUploadedDocuments(id)
{
  const list = document.getElementById('uploadedDocsList');
  list.appendChild(addUploadedDocument(id));
  // list.innerHTML = '';
  // const docs = loadDocs();
  // docs.forEach(d => list.appendChild(addUploadedDocument(d)));
}

function loadDocs() {
  var docs=['1.pdf','2.pdf'];
  return docs;
  // try { return JSON.parse(localStorage.getItem(DOCS_KEY)) || []; }
  // catch { return []; }
}

function addUploadedDocument(doc)
{
  const wrapper = document.createElement('div');
  wrapper.className = 'flex items-center gap-2 bg-white/10 rounded-md px-2 py-2';

  const left = document.createElement('label');
  left.className = 'flex items-center gap-2 flex-1 cursor-pointer select-none min-w-0';

  const cb = document.createElement('input');
  cb.type = 'radio';
  cb.className = 'h-4 w-4 rounded';
  cb.setAttribute('name', `UploadedDocs`);
  cb.addEventListener('change', () => {
    console.log('Selected:', doc);
    showSection('querry');
  });

  const name = document.createElement('span');
  name.className = 'truncate';
  name.title=name.textContent = doc;

  const del = document.createElement('button');
  del.type = 'button';
  del.className = 'shrink-0 text-white/80 hover:text-white rounded px-2';
  del.setAttribute('aria-label', `Delete ${doc}`);
  del.innerHTML = '&times;';
  
  

  left.appendChild(cb)
  left.appendChild(name);
  wrapper.appendChild(left);
  wrapper.appendChild(del);
  // //cb.checked = !!doc.checked;
  // cb.addEventListener('change', () => {
  //  // updateDoc(doc.id, { checked: cb.checked });
  // });
  // const name = document.createElement('span');
  // name.className = 'truncate';
  // name.title = doc;
  // name.textContent = doc;
  // left.appendChild(cb);
  // left.appendChild(name);

  // const del = document.createElement('button');
  // del.type = 'button';
  // del.className = 'shrink-0 text-white/80 hover:text-white rounded px-2';
  // del.setAttribute('aria-label', `Delete ${doc}`);
  // del.innerHTML = '&times;';
  // del.addEventListener('click', async () => {
  //   // OPTIONAL: call your backend to delete, e.g.:
  //   // await fetch(`http://127.0.0.1:9000/upload/pdfs/${encodeURIComponent(doc.id)}`, { method: 'DELETE' });

  //  // removeDoc(doc.id);
  // });

  // wrapper.appendChild(left);
  // wrapper.appendChild(del);
  return wrapper;
}