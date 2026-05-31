// Slide navigation logic
let currentSlide = 1;
const totalSlides = 11;

function changeSlide(direction) {
  const next = currentSlide + direction;
  if (next < 1 || next > totalSlides) return;
  
  const currentEl = document.getElementById(`slide-${currentSlide}`);
  const nextEl = document.getElementById(`slide-${next}`);
  
  currentEl.classList.remove('active');
  currentEl.classList.add('exit');
  
  // Set initial position for next slide
  nextEl.style.transform = direction > 0 ? 'translateX(40px)' : 'translateX(-40px)';
  nextEl.classList.remove('exit');
  
  requestAnimationFrame(() => {
    nextEl.classList.add('active');
    nextEl.style.transform = '';
  });
  
  setTimeout(() => {
    currentEl.classList.remove('exit');
  }, 500);
  
  currentSlide = next;
  document.getElementById('navIndicator').textContent = `${currentSlide} / ${totalSlides}`;
  document.getElementById('prevBtn').disabled = currentSlide === 1;
  document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
    e.preventDefault();
    changeSlide(1);
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault();
    changeSlide(-1);
  } else if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  } else if (e.key === 'Home') {
    while (currentSlide > 1) changeSlide(-1);
  } else if (e.key === 'End') {
    while (currentSlide < totalSlides) changeSlide(1);
  }
});

// Touch support
let touchStartX = 0;
document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
document.addEventListener('touchend', (e) => {
  const diff = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 50) changeSlide(diff > 0 ? 1 : -1);
});

// Init
document.getElementById('prevBtn').disabled = true;
