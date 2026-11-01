/* EyeNet marketing microsites — shared behaviours */

(function photoStrip() {
  const strip = document.querySelector('.photo-strip');
  if (!strip) return;
  let isDown = false, startX, scrollLeft, userInteracting = false, resumeTimer;
  strip.addEventListener('mousedown', (e) => {
    isDown = true; userInteracting = true; strip.style.cursor = 'grabbing';
    startX = e.pageX - strip.offsetLeft; scrollLeft = strip.scrollLeft;
    clearTimeout(resumeTimer);
  });
  strip.addEventListener('mouseleave', () => { isDown = false; strip.style.cursor = 'grab'; scheduleResume(); });
  strip.addEventListener('mouseup', () => { isDown = false; strip.style.cursor = 'grab'; scheduleResume(); });
  strip.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - strip.offsetLeft;
    strip.scrollLeft = scrollLeft - (x - startX) * 1.5;
  });
  strip.addEventListener('touchstart', () => { userInteracting = true; clearTimeout(resumeTimer); }, { passive: true });
  strip.addEventListener('touchend', () => { scheduleResume(); }, { passive: true });
  function scheduleResume() {
    clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => { userInteracting = false; }, 3000);
  }
  const speed = 0.5;
  function autoScroll() {
    if (!userInteracting) {
      strip.scrollLeft += speed;
      if (strip.scrollLeft >= strip.scrollWidth - strip.clientWidth - 1) strip.scrollLeft = 0;
    }
    requestAnimationFrame(autoScroll);
  }
  strip.style.scrollBehavior = 'auto';
  requestAnimationFrame(autoScroll);
})();

function openLightbox(imageSrc, title, description) {
  const lightbox = document.getElementById('lightbox');
  if (!lightbox) return;
  document.getElementById('lightbox-image').src = imageSrc;
  document.getElementById('lightbox-title').textContent = title;
  document.getElementById('lightbox-description').textContent = description || '';
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLightbox(event) {
  if (!event || event.target.id === 'lightbox' || event.target.classList.contains('lightbox-close')) {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeLightbox();
});

const FONT = {
  A:[0b01110,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
  B:[0b11110,0b10001,0b11110,0b10001,0b10001,0b10001,0b11110],
  C:[0b01110,0b10001,0b10000,0b10000,0b10000,0b10001,0b01110],
  D:[0b11110,0b10001,0b10001,0b10001,0b10001,0b10001,0b11110],
  E:[0b11111,0b10000,0b11110,0b10000,0b10000,0b10000,0b11111],
  F:[0b11111,0b10000,0b11110,0b10000,0b10000,0b10000,0b10000],
  G:[0b01110,0b10001,0b10000,0b10111,0b10001,0b10001,0b01110],
  H:[0b10001,0b10001,0b11111,0b10001,0b10001,0b10001,0b10001],
  I:[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b11111],
  K:[0b10001,0b10010,0b11100,0b11000,0b11100,0b10010,0b10001],
  L:[0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b11111],
  M:[0b10001,0b11011,0b10101,0b10101,0b10001,0b10001,0b10001],
  N:[0b10001,0b11001,0b10101,0b10011,0b10001,0b10001,0b10001],
  O:[0b01110,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
  P:[0b11110,0b10001,0b10001,0b11110,0b10000,0b10000,0b10000],
  R:[0b11110,0b10001,0b10001,0b11110,0b11100,0b10010,0b10001],
  S:[0b01110,0b10001,0b10000,0b01110,0b00001,0b10001,0b01110],
  T:[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
  U:[0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
  V:[0b10001,0b10001,0b10001,0b10001,0b10001,0b01010,0b00100],
  W:[0b10001,0b10001,0b10001,0b10101,0b10101,0b11011,0b10001],
  X:[0b10001,0b10001,0b01010,0b00100,0b01010,0b10001,0b10001],
  Y:[0b10001,0b01010,0b00100,0b00100,0b00100,0b00100,0b00100],
  Z:[0b11111,0b00001,0b00010,0b00100,0b01000,0b10000,0b11111],
  ' ':[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000],
  '-':[0b00000,0b00000,0b00000,0b11111,0b00000,0b00000,0b00000]
};
const PIXEL = 3, GLYPH_W = 5, GLYPH_H = 7, SPACING = 2, VS = 1;

function renderPixelText(text, fillColor, opacity) {
  text = text.toUpperCase();
  const chars = text.split('');
  let totalW = 0;
  const glyphData = chars.map((ch) => FONT[ch] || FONT[' ']);
  for (let i = 0; i < chars.length; i++) totalW += GLYPH_W * PIXEL + (i < chars.length - 1 ? SPACING : 0);
  const totalH = GLYPH_H * PIXEL + (GLYPH_H - 1) * VS;
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${totalW} ${totalH}`);
  svg.setAttribute('width', totalW);
  svg.setAttribute('height', totalH);
  let cursorX = 0;
  for (let gi = 0; gi < glyphData.length; gi++) {
    const rows = glyphData[gi];
    for (let row = 0; row < GLYPH_H; row++) {
      const mask = rows[row];
      for (let col = 0; col < GLYPH_W; col++) {
        if (mask & (1 << (4 - col))) {
          const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          rect.setAttribute('x', cursorX + col * PIXEL);
          rect.setAttribute('y', row * (PIXEL + VS));
          rect.setAttribute('width', PIXEL);
          rect.setAttribute('height', PIXEL);
          rect.setAttribute('fill', fillColor);
          rect.setAttribute('opacity', opacity);
          svg.appendChild(rect);
        }
      }
    }
    cursorX += GLYPH_W * PIXEL + SPACING;
  }
  return svg;
}

function cloneLogoSvg(height) {
  const source = document.querySelector('.header-logo');
  if (!source) return document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  const svg = source.cloneNode(true);
  svg.removeAttribute('class');
  svg.setAttribute('style', 'display:block;height:' + height + 'px;width:auto;margin:0;');
  return svg;
}

function addEyenetChips(containerId, chipNames) {
  const container = document.getElementById(containerId);
  if (!container || !chipNames) return;
  chipNames.forEach((name) => {
    const chip = document.createElement('span');
    chip.className = 'eyenet-chip';
    const logoSvg = cloneLogoSvg(14);
    logoSvg.classList.add('chip-logo-svg');
    chip.appendChild(logoSvg);
    const subSvg = renderPixelText(name, '#ecfeff', 0.98);
    subSvg.classList.add('chip-sub-svg');
    chip.appendChild(subSvg);
    container.appendChild(chip);
  });
}

document.querySelectorAll('[data-chips]').forEach((el) => {
  const names = el.getAttribute('data-chips').split(',').map((s) => s.trim()).filter(Boolean);
  addEyenetChips(el.id, names);
});

document.querySelectorAll('[data-app-name]').forEach((el) => {
  const name = el.getAttribute('data-app-name');
  const logoSvg = cloneLogoSvg(28);
  logoSvg.classList.add('as-logo-svg');
  el.appendChild(logoSvg);
  const subSvg = renderPixelText(name, '#ecfeff', 0.98);
  subSvg.classList.add('as-sub-svg');
  el.appendChild(subSvg);
});

document.querySelectorAll('[data-dd-name]').forEach((el) => {
  const name = el.getAttribute('data-dd-name');
  const logoSvg = cloneLogoSvg(40);
  logoSvg.classList.add('dd-logo-svg');
  el.appendChild(logoSvg);
  const subSvg = renderPixelText(name, '#ecfeff', 0.98);
  subSvg.classList.add('dd-sub-svg');
  el.appendChild(subSvg);
});
