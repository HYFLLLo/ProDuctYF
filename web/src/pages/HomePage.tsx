import { Link } from 'react-router-dom'

const featureCards = [
  {
    id: 'STATUS_01',
    title: 'INTERFACE_DYN',
    body: 'Dynamic UI modules built for high-stress environments. Low latency, high response.',
  },
  {
    id: 'STATUS_02',
    title: 'NEURAL_PASS',
    body: 'Biometric authentication protocols integrated at the kernel level for absolute security.',
  },
  {
    id: 'STATUS_03',
    title: 'VOID_ARCH',
    body: 'Minimalist architectural structures designed to persist in the digital void.',
  },
]

export function HomePage() {
  return (
    <div className="page page--home">
      <div className="home-decor home-decor--tl" aria-hidden>
        <p>LOC_DATA: 34.0522° N, 118.2437° W</p>
        <p>ENCRYPTION: AES_256_GCM</p>
        <p>SYNC_STATUS: VERIFIED</p>
        <div className="glitch-line glitch-line--sm" />
      </div>
      <div className="home-decor home-decor--br" aria-hidden>
        <p>MEM_UTIL: 42% [||||------]</p>
        <p>UPLINK_STRENGTH: 98.4dB</p>
        <p>PORT: 8080/UDP</p>
        <div className="glitch-line glitch-line--md" />
      </div>

      <div className="home-hero">
        <div className="home-logo-wrap">
          <div className="home-logo-glow" />
          <h1 className="home-y hologram-y">Y</h1>
          <div className="home-ref label-mono">REF_ID: YVEN_01</div>
        </div>

        <div className="home-intro">
          <div className="home-greeting">
            <span className="label-mono home-greeting__tag">INITIALIZING_GREETING</span>
            <p className="headline-lg home-greeting__line">
              Hello! Welcome to Yven&apos;s web
            </p>
          </div>
          <p className="body-text home-lead">
            Exploring the intersection of high-fidelity aesthetics and clandestine functionality. Designing the digital
            infrastructure for the next generation of neural interfaces.
          </p>
        </div>

        <div className="home-cta">
          <Link to="/contact" className="chamfer-btn label-mono">
            Contact me
          </Link>
          <a className="ghost-link label-mono" href="https://github.com" target="_blank" rel="noreferrer">
            <span className="ghost-link__dot" />
            View Repository
          </a>
        </div>
      </div>

      <div className="home-grid">
        {featureCards.map((card) => (
          <article key={card.id} className="neo-card">
            <div className="neo-card__corner" />
            <span className="label-mono neo-card__id">{card.id}</span>
            <h3 className="headline-md neo-card__title">{card.title}</h3>
            <p className="body-text neo-card__body">{card.body}</p>
          </article>
        ))}
      </div>
    </div>
  )
}
