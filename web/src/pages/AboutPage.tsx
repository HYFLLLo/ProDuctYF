const primaryStack = ['TypeScript / React', 'Node.js / Rust', 'PostgreSQL / Redis']
const cyberToolkit = ['AWS / Terraform', 'WebGL / Three.js', 'Docker / K8s']

const timeline = [
  {
    range: '2022 — PRESENT',
    org: 'Neural Nexus',
    role: 'SENIOR ARCHITECT',
    desc: 'Spearheading the development of next-gen interactive visualization engines for decentralized finance protocols.',
  },
  {
    range: '2019 — 2022',
    org: 'Cortex Labs',
    role: 'FRONT-END LEAD',
    desc: 'Managed a core team of 12 developers to rebuild a high-traffic SaaS platform with micro-frontend architecture.',
  },
  {
    range: '2017 — 2019',
    org: 'Void Digital',
    role: 'INTERACTIVE DEV',
    desc: 'Creative coding and GLSL shader development for award-winning digital installations and fashion brands.',
  },
]

function BulletList({ items }: { items: string[] }) {
  return (
    <ul className="about-list">
      {items.map((item) => (
        <li key={item}>
          <span className="about-list__bullet" />
          {item}
        </li>
      ))}
    </ul>
  )
}

export function AboutPage() {
  return (
    <div className="page page--about">
      <div className="about-glow about-glow--tl" aria-hidden />
      <div className="about-glow about-glow--br" aria-hidden />

      <div className="about-grid">
        <div className="about-bio glass-panel">
          <div className="label-mono about-bio__ref">REF_ID: //YVEN_BIO_01</div>
          <div className="about-bio__inner">
            <h1 className="headline-xl about-bio__title">
              Synthesizing <br />
              <span className="text-secondary">Digital Architectures</span>
            </h1>
            <div className="chip-row">
              <span className="chip chip--secondary">Lead Engineer</span>
              <span className="chip chip--primary">Full-Stack Meta</span>
              <span className="chip chip--muted">Tokyo // Virtual</span>
            </div>
            <div className="about-copy">
              <p className="body-text">
                Operating at the intersection of high-fidelity aesthetics and performant infrastructure. Yven specializes
                in the construction of immersive neural interfaces and distributed systems that challenge the
                boundaries of contemporary web standards.
              </p>
              <p className="body-text muted">
                With over a decade of experience in the shadows of the tech industry, I transform complex data flows
                into intuitive, luminous experiences. My philosophy is simple: high tech, low life, zero friction.
              </p>
            </div>
            <div className="about-skills">
              <div>
                <span className="label-mono about-skills__label">Primary_Stack</span>
                <BulletList items={primaryStack} />
              </div>
              <div>
                <span className="label-mono about-skills__label">Cyber_Toolkit</span>
                <BulletList items={cyberToolkit} />
              </div>
            </div>
            <div className="about-cta">
              <button type="button" className="manifest-btn label-mono">
                [ Download_Manifesto ]
                <span className="manifest-btn__corner manifest-btn__corner--tr" />
                <span className="manifest-btn__corner manifest-btn__corner--bl" />
              </button>
            </div>
          </div>
        </div>

        <div className="about-side">
          <div className="glass-panel neo-stroke code-panel">
            <div className="code-panel__bar">
              <span className="label-mono code-panel__title">
                <span className="material-symbols-outlined code-panel__icon" aria-hidden>
                  code
                </span>
                kernel_init.sys
              </span>
              <div className="code-panel__dots" aria-hidden>
                <span />
                <span />
                <span />
              </div>
            </div>
            <pre className="code-panel__pre label-mono">
              <code>
                {`import { NeuralCore } from '@yven/v2';

const kernel = new NeuralCore({
  identity: 'Yven_Unit_88',
  latency: '0.002ms',
  protocols: ['clean-ui', 'dark-mode']
});

await kernel.initialize();
// Check status...
if (kernel.isOnline()) {
  console.log('[SUCCESS] Connection established.');
}`}
              </code>
            </pre>
          </div>

          <div className="metrics-row">
            <div className="glass-panel neo-stroke metric-card">
              <span className="label-mono metric-card__label">System_Load</span>
              <div className="metric-card__value text-primary-neon">
                82.4<span className="metric-card__unit">%</span>
              </div>
              <div className="metric-card__bar">
                <div className="metric-card__fill metric-card__fill--cyan" style={{ width: '82.4%' }} />
              </div>
            </div>
            <div className="glass-panel neo-stroke metric-card">
              <span className="label-mono metric-card__label">Uptime_Sequence</span>
              <div className="metric-card__value text-secondary">
                99.9<span className="metric-card__unit">%</span>
              </div>
              <div className="metric-card__bar">
                <div className="metric-card__fill metric-card__fill--purple" style={{ width: '99.9%' }} />
              </div>
            </div>
          </div>

          <div className="glass-panel neo-stroke hex-viz">
            <div className="hex-viz__bg" aria-hidden>
              <span className="material-symbols-outlined">grid_view</span>
            </div>
            <div className="hex-viz__rings">
              <div className="hex-ring hex-ring--outer">
                <div className="hex-ring hex-ring--mid">
                  <div className="hex-ring hex-ring--inner">
                    <div className="hex-core" />
                  </div>
                </div>
              </div>
              <span className="label-mono hex-viz__axis hex-viz__axis--t">AXIS_Y</span>
              <span className="label-mono hex-viz__axis hex-viz__axis--b">AXIS_Δ</span>
              <span className="label-mono hex-viz__axis hex-viz__axis--l">AXIS_X</span>
              <span className="label-mono hex-viz__axis hex-viz__axis--r">AXIS_Σ</span>
            </div>
            <div className="label-mono hex-viz__caption">HEX_METRIC_VISUALIZER // V0.9</div>
          </div>
        </div>
      </div>

      <section className="about-log">
        <div className="about-log__head">
          <h2 className="headline-md text-primary-neon uppercase">Log_History</h2>
          <div className="about-log__rule" />
        </div>
        <div className="about-log__grid">
          {timeline.map((item) => (
            <article key={item.org} className="glass-panel neo-stroke log-card">
              <span className="label-mono log-card__range text-secondary">{item.range}</span>
              <h3 className="headline-sm log-card__org">{item.org}</h3>
              <p className="label-mono log-card__role text-primary-neon">{item.role}</p>
              <p className="body-text muted log-card__desc">{item.desc}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
