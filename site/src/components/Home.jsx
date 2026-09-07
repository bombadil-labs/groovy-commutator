import Nav from './Nav.jsx';
import { StaticRuleGrid } from './AmbientCA.jsx';
import Defn, { Op } from './Defn.jsx';

// Same rules as the Concepts page's quick-pick list, one color each --
// reuses the site's established regime hues for visual continuity.
const SAMPLE_RULES = [
  { num: 4, color: 'oklch(0.55 0.12 195)' },
  { num: 184, color: 'oklch(0.58 0.13 150)' },
  { num: 30, color: 'oklch(0.58 0.13 300)' },
  { num: 110, color: 'oklch(0.58 0.13 240)' },
  { num: 54, color: 'oklch(0.6 0.14 75)' },
  { num: 90, color: 'oklch(0.56 0.15 22)' },
];

const pBody = { fontSize: '1rem', color: 'var(--ink-soft)', margin: '0 0 1.2rem', maxWidth: '68ch' };

export default function Home() {
  return (
    <>
      <Nav active="home" />

      <main style={{ maxWidth: 880, margin: '0 auto', padding: '2rem 1.25rem 4rem' }}>
        <section style={{ padding: '1.6rem 0 0.5rem' }}>
          <h1 style={{ fontFamily: "'Lora',serif", fontSize: 'clamp(1.9rem,5vw,2.6rem)', lineHeight: 1.25, margin: '0 0 0.6em', fontWeight: 600, letterSpacing: '-0.01em' }}>
            A New Lens on Cellular Automata
          </h1>

          <p style={pBody}>
            Some years ago I had an idea for a simple Boolean calculus specifically for cellular automata &mdash; so
            simple it's almost trivial. More details are available on the{' '}
            <a href="concepts.html" style={{ color: 'var(--accent)' }}>Concepts page</a>, but the entire thing can be
            defined here, mostly in terms of XOR.
          </p>

          <p style={pBody}>
            Normally you'd just say: the next state is <Op>&phi;(S)</Op>, full stop. Call
            that step <Op>E(S)</Op>, for <em>evolve</em> &mdash; and if all you want is the
            next state, that's the whole story, no calculus required. What follows arrives at that exact
            same <Op>&phi;(S)</Op> by a longer road, through a derivative and an integral.
            That's not a different answer &mdash; <Op>E(S)</Op> is provably identical to
            plain <Op>&phi;(S)</Op>, an isomorphism, not a new evolution rule. The point of
            the detour is what it exposes along the way: two internal moving parts, <Op>D</Op>{' '}
            and <Op>I</Op>, that turn out to be useful on their own.
          </p>

          <div style={{ margin: '1.4rem 0' }}>
            <Defn lines={[
              { parts: [{ t: 'R' }, { t: ' ∈ {0, 1, …, 255}' }], note: 'the rule' },
              { parts: [
                  { t: <>&phi;(S)<sub>i</sub></>, k: 'φ' },
                  { t: ' = ' },
                  { t: <>R<sub>4&middot;S(i&minus;1) + 2&middot;S(i) + S(i+1)</sub></>, k: 'R' },
                ], note: "one cell's next value" },
              { parts: [{ t: 'D' }, { t: '(S) = S ⊕ ' }, { t: 'φ' }, { t: '(S)' }], note: 'differentiate — what changed' },
              { parts: [{ t: 'I' }, { t: '(a, b) = a ⊕ b' }], note: 'integrate — fold a difference back in' },
              { parts: [{ t: 'E' }, { t: '(S) = ' }, { t: 'I' }, { t: '(S, ' }, { t: 'D' }, { t: '(S)) = ' }, { t: 'φ' }, { t: '(S)' }], note: 'evolve — derived, not assumed' },
            ]} />
          </div>
          <p style={{ ...pBody, fontSize: '0.9rem' }}>
            <Op>&phi;</Op>{' '}
            just reads <Op>R</Op>{' '}
            as an 8-entry lookup table, indexed by the 3-cell neighborhood &mdash; the same table the rule-diagram on
            the Concepts page lets you edit by hand. Anything <span style={{ fontWeight: 700 }}>bold with a dotted
            underline</span> here and on the Concepts page is clickable &mdash; tap it for its definition.
          </p>

          <StaticRuleGrid rules={SAMPLE_RULES} />

          <p style={{ ...pBody, marginTop: '1.8rem' }}>
            For the longest time I thought of this as just a sort of pedantic expansion of some trivial dynamics
            &mdash; I assumed it was an established way to look at CAs. When I dusted it off in November of 2025,
            though, I realized that at least a cursory exploration of the space didn't surface anyone else looking at
            CAs this way. Furthermore, this time I noticed some affordances through it that I'd never noticed before.
          </p>

          <p style={pBody}>
            This site exists to document and explore some of the implications. I'm not heavily invested in CA
            studies, I'm not making any claims that any of this is groundbreaking, but some of it is interesting
            enough that I wanted to create a coherent place to share it.
          </p>

          <p style={pBody}>
            What I have is a Boolean calculus and then a few instruments defined or inspired by it, and together
            they give me some interesting lenses through which to examine CA rules.
          </p>

          <p style={pBody}>
            On this site you'll find a <a href="concepts.html" style={{ color: 'var(--accent)' }}>Concepts page</a>,
            where I go into detail about the various concepts in play &mdash; the goal is to be intelligible even to
            someone who has never played with CAs before.
          </p>

          <p style={pBody}>
            You'll find a <a href="questions.html" style={{ color: 'var(--accent)' }}>Questions page</a>, where I
            explain the questions that arise for me and what the experiments have taught us so far.
          </p>

          <p style={pBody}>
            The <a href="research/index.html" style={{ color: 'var(--accent)' }}>Research section</a> keeps the ongoing
            work: experiments, corrections, and open questions, with their methods and evidence. As an idea becomes
            ready to explain, it finds its way into these main pages.
          </p>

          <p style={pBody}>
            And you'll find an <a href="explorer.html" style={{ color: 'var(--accent)' }}>Explorer page</a>, which
            lets you play with CAs in an interface designed to support the novel affordances that emerge from this
            calculus and the related instruments.
          </p>

          <div className="gc-cta" style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap', margin: '1.8em 0 0' }}>
            <a href="concepts.html" className="gc-mono" style={{ display: 'inline-block', fontWeight: 700, fontSize: '0.92rem', textDecoration: 'none', padding: '0.7rem 1.3rem', borderRadius: 7, border: '1px solid var(--accent)', background: 'var(--accent)', color: '#fff' }}>
              Read the concepts &rarr;
            </a>
            <a href="questions.html" className="gc-mono" style={{ display: 'inline-block', fontWeight: 700, fontSize: '0.92rem', textDecoration: 'none', padding: '0.7rem 1.3rem', borderRadius: 7, border: '1px solid var(--accent)', background: 'transparent', color: 'var(--accent)' }}>
              See the questions
            </a>
            <a href="explorer.html" className="gc-mono" style={{ display: 'inline-block', fontWeight: 700, fontSize: '0.92rem', textDecoration: 'none', padding: '0.7rem 1.3rem', borderRadius: 7, border: '1px solid var(--accent)', background: 'transparent', color: 'var(--accent)' }}>
              Try the explorer
            </a>
          </div>
        </section>
      </main>

      <footer className="gc-footer">
        <div className="gc-footer-inner">
          Source, library code, and full research notes live in the{' '}
          <a href="https://github.com/mbilokonsky/groovy-commutator">GitHub repository</a>.
        </div>
      </footer>
    </>
  );
}
