(() => {
  const PAGE_W = 280;
  const PAGE_H = 397;
  const Z = 2147483000;

  const pages = {
    'inside-cover.png': [
      ['Featured article: Antisense oligonucleotides', 16, 120, 31, 149, 59],
      ['RARE Inspiration', 4, 8, 145, 123, 15],
      ['Nothing is impossible', 16, 8, 164, 123, 15],
      ['The person behind the mask', 22, 8, 183, 123, 15],
      ['Can you really be ill enough to be pregnant?', 36, 8, 202, 123, 15],
      ['Guidelines, global voices', 48, 8, 221, 123, 15],
      ['More than awareness', 54, 8, 240, 123, 15],
      ['Spending years in the wrong clinic', 62, 8, 259, 123, 15],
      ['The power of consultation', 64, 8, 278, 123, 15],
      ['More than a birthright', 68, 8, 297, 123, 15],
      ['Positivity and perseverance', 75, 8, 316, 123, 16],
      ['One direction', 26, 140, 145, 130, 19],
      ['Building bridges of understanding', 58, 140, 168, 130, 19],
      ['From burden to breakthrough', 10, 140, 210, 130, 17],
      ['Healthy skin for all', 33, 140, 229, 130, 17],
      ['Beyond the molecule', 40, 140, 248, 130, 17],
      ['Systemic gaps in complex care', 44, 140, 267, 130, 17],
      ['Prioritising funding', 72, 140, 286, 130, 19],
      ['eRARE learnings', 80, 140, 327, 130, 16],
      ['Book review and more views', 82, 140, 346, 130, 16],
      ['UCB — Inspired by patients. Driven by science.', 'https://www.ucb.com/', 184, 294, 88, 37],
      ['Email the RARE Revolution editorial team', 'mailto:editor@rarerevolutionmagazine.com', 72, 343, 139, 18],
      ['Visit RARE Revolution Magazine', 'https://rarerevolutionmagazine.com/', 62, 361, 157, 24]
    ],
    'page-03.png': [
      ['Email the RARE Revolution editor', 'mailto:editor@rarerevolutionmagazine.com', 72, 334, 86, 11],
      ['Visit RARE Revolution Magazine', 'https://rarerevolutionmagazine.com/', 165, 334, 108, 61],
      ['UCB — Inspired by patients. Driven by science.', 'https://www.ucb.com/', 70, 370, 91, 22]
    ]
  };

  const overlay = document.createElement('div');
  overlay.id = 'rrm-front-spread-fixed-hotspots';
  Object.assign(overlay.style, {
    position: 'fixed', inset: '0', zIndex: String(Z), pointerEvents: 'none'
  });
  document.documentElement.appendChild(overlay);

  function setReactInputValue(input, value) {
    const descriptor = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
    if (descriptor && descriptor.set) descriptor.set.call(input, String(value));
    else input.value = String(value);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function goToPage(pageNumber) {
    // Use an application-level event so hotspots work in every view mode,
    // including mobile where the page-jump input is hidden.
    window.dispatchEvent(new CustomEvent('rrm:navigate', {
      detail: { page: Number(pageNumber) }
    }));

    // Backward-compatible fallback for older cached builds.
    const input = document.querySelector('input[placeholder^="Go to page"]');
    if (!input) return;
    setReactInputValue(input, pageNumber);
    input.dispatchEvent(new InputEvent('input', {
      bubbles: true, inputType: 'insertText', data: String(pageNumber)
    }));
    requestAnimationFrame(() => {
      const form = input.closest('form');
      if (form?.requestSubmit) form.requestSubmit();
      else form?.dispatchEvent(new Event('submit', {
        bubbles: true, cancelable: true
      }));
    });
  }

  function stop(event) { event.stopPropagation(); }

  function makeElement(item, rect) {
    const [label, destination, x, y, width, height] = item;
    const element = typeof destination === 'number'
      ? document.createElement('button')
      : document.createElement('a');

    if (typeof destination === 'number') {
      element.type = 'button';
      element.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        goToPage(destination);
      });
    } else {
      element.href = destination;
      element.target = '_blank';
      element.rel = 'noopener noreferrer';
      element.addEventListener('click', stop);
    }

    ['pointerdown', 'mousedown', 'touchstart', 'mouseup', 'touchend'].forEach((name) => {
      element.addEventListener(name, stop, { passive: name.startsWith('touch') });
    });

    element.title = label;
    element.setAttribute('aria-label', label);
    Object.assign(element.style, {
      position: 'fixed',
      left: `${rect.left + rect.width * x / PAGE_W}px`,
      top: `${rect.top + rect.height * y / PAGE_H}px`,
      width: `${rect.width * width / PAGE_W}px`,
      height: `${rect.height * height / PAGE_H}px`,
      zIndex: String(Z + 1),
      display: 'block', padding: '0', margin: '0', border: '0',
      background: 'transparent', pointerEvents: 'auto', cursor: 'pointer',
      appearance: 'none'
    });
    return element;
  }

  function getPageKey(src) {
    if (!src) return null;
    if (src.includes('inside-cover.png') || /[?&]pnum=2(?:&|$)/.test(src)) {
      return 'inside-cover.png';
    }
    if (src.includes('page-03.png') || /[?&]pnum=3(?:&|$)/.test(src)) {
      return 'page-03.png';
    }
    return null;
  }

  function update() {
    overlay.replaceChildren();
    document.querySelectorAll('img').forEach((img) => {
      const src = img.currentSrc || img.src || '';
      const key = getPageKey(src);
      if (!key) return;
      const rect = img.getBoundingClientRect();
      if (rect.width < 20 || rect.height < 20 || rect.bottom <= 0 || rect.top >= innerHeight) return;
      pages[key].forEach((item) => overlay.appendChild(makeElement(item, rect)));
    });
  }

  let pending = false;
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; update(); });
  }

  new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['src', 'style', 'class'] });
  window.addEventListener('resize', schedule);
  window.addEventListener('scroll', schedule, true);
  window.addEventListener('load', schedule);
  setInterval(schedule, 500);
  schedule();
})();
