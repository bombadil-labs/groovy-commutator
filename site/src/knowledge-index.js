export function matchesKnowledge(searchText, entryKind, query = '', kind = '') {
  const normalize = (text) => text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const terms = normalize(query).trim().split(/\s+/).filter(Boolean);
  const text = normalize(searchText);
  return (!kind || kind === entryKind) && terms.every((term) => text.includes(term));
}

if (typeof document !== 'undefined') {
  const form = document.querySelector('[data-knowledge-filters]');
  if (form) {
    const entries = [...document.querySelectorAll('[data-knowledge-entry]')];
    const count = document.querySelector('[data-knowledge-count]');
    const empty = document.querySelector('[data-knowledge-empty]');
    const update = () => {
      let shown = 0;
      for (const entry of entries) {
        const visible = matchesKnowledge(entry.dataset.search, entry.dataset.kind, form.elements.query.value, form.elements.kind.value);
        entry.hidden = !visible; if (visible) shown++;
      }
      count.textContent = `${shown} of ${entries.length} ${entries.length === 1 ? 'entry' : 'entries'}`;
      empty.hidden = shown !== 0;
    };
    form.hidden = false;
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    form.addEventListener('submit', (event) => event.preventDefault());
    form.addEventListener('reset', () => queueMicrotask(update));
    update();
  }
}
