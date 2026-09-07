import { PAGES } from '../data/navigation.js';

export default function Nav({ active, brandFont = "'Lora',serif" }) {
  return (
    <header className="gc-header">
      <nav className="gc-nav" aria-label="Main navigation">
        <a href="index.html" className="gc-nav-brand" style={{ fontFamily: brandFont }}>Groovy Commutator</a>
        <div className="gc-nav-links">
          {PAGES.map((p) => (
            <a key={p.key} href={p.href} aria-current={p.key === active ? 'page' : undefined} className={'gc-nav-link' + (p.key === active ? ' active' : '')}>
              {p.label}
            </a>
          ))}
        </div>
      </nav>
    </header>
  );
}
