/* =============================================
   EKG Multi-Agente — Upload Logic (app.js)
   Connects frontend to FastAPI backend
   ============================================= */

// ── API URL dinámica: localhost en dev, Cloud Run en producción ───────────
const CLOUD_RUN_URL = 'https://ekg-backend-30374884403-uc.a.run.app';
const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8080/analyze'
  : `${CLOUD_RUN_URL}/analyze`;


document.addEventListener('DOMContentLoaded', () => {
  const uploadCard   = document.getElementById('uploadCard');
  const fileInput    = document.getElementById('fileElem');
  const fileBtn      = document.getElementById('fileSelectBtn');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar  = document.getElementById('progressBar');
  const progressLbl  = document.getElementById('progressLabel');
  const statusMsg    = document.getElementById('statusMsg');

  // ── Open file dialog ──────────────────────────────────
  fileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
  });
  uploadCard.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

  // ── Drag & drop ───────────────────────────────────────
  ['dragenter', 'dragover'].forEach(ev => {
    uploadCard.addEventListener(ev, (e) => {
      e.preventDefault();
      e.stopPropagation();
      uploadCard.classList.add('dragover');
    });
  });
  ['dragleave', 'drop'].forEach(ev => {
    uploadCard.addEventListener(ev, (e) => {
      e.preventDefault();
      e.stopPropagation();
      uploadCard.classList.remove('dragover');
    });
  });
  uploadCard.addEventListener('drop', (e) => {
    handleFiles(e.dataTransfer.files);
  });

  // ── Main upload handler ───────────────────────────────
  async function handleFiles(files) {
    if (!files || files.length === 0) return;
    const file = files[0];

    // Client-side validation
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      return showStatus('Tipo de archivo no soportado. Usa JPG o PNG.', 'error');
    }
    if (file.size > 10 * 1024 * 1024) {
      return showStatus('El archivo supera los 10 MB permitidos.', 'error');
    }

    // Save image preview for result page
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => sessionStorage.setItem('ekgImage', reader.result);

    // Show progress UI
    setProgress(true);
    animateChips('active', ['ritmo', 'morfologia', 'isquemia', 'intervalos']);
    setProgressBar(15, 'Enviando imagen al servidor…');

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Simulate visual progress while waiting for backend
      let fakeProgress = 15;
      const fakeInterval = setInterval(() => {
        if (fakeProgress < 70) {
          fakeProgress += 5;
          setProgressBar(fakeProgress, getProgressLabel(fakeProgress));
        }
      }, 1200);

      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      clearInterval(fakeInterval);

      if (!response.ok) {
        let detail = `Error HTTP ${response.status}`;
        try { const err = await response.json(); detail = err.detail || detail; } catch {}
        throw new Error(detail);
      }

      const result = await response.json();

      // Mark all agents done, síntesis active → then done
      animateChips('done', ['ritmo', 'morfologia', 'isquemia', 'intervalos']);
      animateChips('active', ['sintesis']);
      setProgressBar(90, 'Generando síntesis clínica…');

      await delay(800);

      animateChips('done', ['sintesis']);
      setProgressBar(100, 'Análisis completo. Redirigiendo…');

      // Store result and navigate
      sessionStorage.setItem('ekgResult', JSON.stringify(result));
      await delay(700);
      window.location.href = 'result.html';

    } catch (err) {
      setProgress(false);
      resetChips();
      showStatus(`Error en el análisis: ${err.message}`, 'error');
      console.error('[EKG] Error:', err);
    }
  }

  // ── Helpers ───────────────────────────────────────────
  function setProgress(visible) {
    progressWrap.classList.toggle('visible', visible);
    uploadCard.style.pointerEvents = visible ? 'none' : 'auto';
    uploadCard.style.opacity = visible ? '0.5' : '1';
  }

  function setProgressBar(pct, label) {
    progressBar.style.width = `${pct}%`;
    if (label) progressLbl.textContent = label;
  }

  function getProgressLabel(pct) {
    if (pct < 30) return 'Analizando ritmo y morfología…';
    if (pct < 50) return 'Evaluando isquemia e intervalos…';
    if (pct < 70) return 'Procesando hallazgos clínicos…';
    return 'Casi listo…';
  }

  function animateChips(state, agentIds) {
    agentIds.forEach(id => {
      const chip = document.getElementById(`chip-${id}`);
      if (!chip) return;
      chip.classList.remove('active', 'done');
      if (state) chip.classList.add(state);
    });
  }

  function resetChips() {
    ['ritmo', 'morfologia', 'isquemia', 'intervalos', 'sintesis'].forEach(id => {
      const chip = document.getElementById(`chip-${id}`);
      if (chip) chip.classList.remove('active', 'done');
    });
  }

  function showStatus(msg, type) {
    statusMsg.textContent = msg;
    statusMsg.className = `status-msg visible ${type}`;
  }

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
});
