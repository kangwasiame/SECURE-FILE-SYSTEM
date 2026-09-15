document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.querySelector('.upload input[type="file"]');
  const fileLabel = document.querySelector('.upload label');
  if (fileInput && fileLabel) {
    fileInput.addEventListener('change', () => {
      fileLabel.textContent = fileInput.files.length ? fileInput.files[0].name : 'Choose a file';
    });
  }

  if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost')) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/static/service-worker.js');
    });
  }

  const scenes = document.querySelectorAll('[data-demo-scene]');
  const stepButtons = document.querySelectorAll('[data-demo-step]');
  const previous = document.querySelector('.demo-prev');
  const next = document.querySelector('.demo-next');
  const walkthrough = document.querySelector('.walkthrough');
  let currentStep = 1;
  let timer;
  let isPlaying = true;
  const stepDuration = 4500;

  if (walkthrough && scenes.length && stepButtons.length) {
    const controls = walkthrough.querySelector('.demo-controls');
    const play = document.createElement('button');
    play.className = 'demo-play';
    play.type = 'button';
    play.setAttribute('aria-label', 'Pause walkthrough');
    play.textContent = 'Pause';
    controls.insertBefore(play, controls.querySelector('.demo-progress'));

    const progress = document.createElement('span');
    progress.className = 'demo-timer';
    progress.setAttribute('aria-hidden', 'true');
    controls.appendChild(progress);

    function setPlaying(playing) {
      isPlaying = playing;
      play.textContent = playing ? 'Pause' : 'Play';
      play.setAttribute('aria-label', `${playing ? 'Pause' : 'Play'} walkthrough`);
      walkthrough.classList.toggle('is-playing', playing);
    }

    function stopTimer() {
      window.clearInterval(timer);
      timer = undefined;
      setPlaying(false);
    }

    function startTimer() {
      window.clearInterval(timer);
      timer = window.setInterval(() => showStep(currentStep + 1), stepDuration);
      setPlaying(true);
    }

    play.addEventListener('click', () => (isPlaying ? stopTimer() : startTimer()));
    walkthrough.addEventListener('mouseleave', () => {
      if (isPlaying) startTimer();
    });
    walkthrough.addEventListener('keydown', (event) => {
      if (event.key === ' ' && event.target === walkthrough) {
        event.preventDefault();
        play.click();
      }
    });
  }

  function showStep(step) {
    currentStep = step < 1 ? scenes.length : step > scenes.length ? 1 : step;
    scenes.forEach((scene) => scene.classList.toggle('visible', Number(scene.dataset.demoScene) === currentStep));
    stepButtons.forEach((button) => button.classList.toggle('active', Number(button.dataset.demoStep) === currentStep));
  }

  if (scenes.length && stepButtons.length) {
    const advance = () => showStep(currentStep + 1);
    stepButtons.forEach((button) => button.addEventListener('click', () => showStep(Number(button.dataset.demoStep))));
    if (previous) previous.addEventListener('click', () => showStep(currentStep - 1));
    if (next) next.addEventListener('click', advance);
    showStep(1);
    if (walkthrough) {
      walkthrough.tabIndex = 0;
      timer = window.setInterval(advance, stepDuration);
      walkthrough.addEventListener('mouseenter', () => window.clearInterval(timer));
    }
  }
});
