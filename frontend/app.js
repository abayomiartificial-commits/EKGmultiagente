document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('fileElem');
  const fileSelectBtn = document.getElementById('fileSelectBtn');
  const progressBar = document.querySelector('.progress-bar');
  const progressContainer = document.getElementById('progress');
  const statusEl = document.getElementById('status');

  // Click to open file selector
  fileSelectBtn.addEventListener('click', () => fileInput.click());

  // Handle file selection via dialog
  fileInput.addEventListener('change', handleFiles);

  // Drag & drop handlers
  ['dragenter', 'dragover'].forEach(ev => {
    dropArea.addEventListener(ev, e => {
      e.preventDefault();
      e.stopPropagation();
      dropArea.classList.add('dragover');
    });
  });
  ['dragleave', 'drop'].forEach(ev => {
    dropArea.addEventListener(ev, e => {
      e.preventDefault();
      e.stopPropagation();
      dropArea.classList.remove('dragover');
    });
  });
  dropArea.addEventListener('drop', e => {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles({ target: { files } });
  });

  function handleFiles(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    // Basic validation
    const validTypes = ['image/jpeg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      showStatus('Tipo de archivo no soportado. Usa JPG o PNG.', 'danger');
      return;
    }
    if (file.size > 10 * 1024 * 1024) { // 10 MB
      showStatus('El archivo supera los 10 MB permitidos.', 'danger');
      return;
    }
    // Show progress placeholder (simulated)
    progressContainer.classList.remove('hidden');
    progressBar.style.width = '0%';
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      progressBar.style.width = `${progress}%`;
      if (progress >= 100) {
        clearInterval(interval);
        // Here we would call the backend API; for now just show success
        showStatus('Imagen cargada correctamente. Análisis pendiente...', 'success');
        // Redirect to result page with placeholder query param (to be replaced later)
        const reader = new FileReader();
        reader.onload = () => {
          // Save the base64 data to sessionStorage for the result page demo
          sessionStorage.setItem('ekgImage', reader.result);
          window.location.href = 'result.html';
        };
        reader.readAsDataURL(file);
      }
    }, 200);
  }

  function showStatus(message, type) {
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
    statusEl.classList.remove('hidden');
  }
});
