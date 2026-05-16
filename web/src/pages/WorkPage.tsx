type Project = {
  ref: string
  title: string
  description: string
  tags: string[]
  icon: string
}

const projects: Project[] = [
  {
    ref: 'REF_001',
    title: 'NEURAL_LINK',
    description:
      'Biometric synchronization interface designed for low-latency neural feedback loops. Optimized for sub-ms response times.',
    tags: ['C++', 'Neural', 'Encrypted'],
    icon: 'data_object',
  },
  {
    ref: 'REF_002',
    title: 'VOID_SEC',
    description:
      'Zero-trust infrastructure framework for decentralized data clusters. Implements advanced spectral encryption protocols.',
    tags: ['Rust', 'Protocol'],
    icon: 'security',
  },
  {
    ref: 'REF_003',
    title: 'GRID_MAPPING',
    description:
      'Real-time visualization engine for metropolitan data grids. Processes over 1M dynamic nodes per second.',
    tags: ['WebGL', 'Live'],
    icon: 'hub',
  },
  {
    ref: 'REF_004',
    title: 'CORE_PROCESS',
    description:
      'Kernel-level optimization suite for multi-threaded synthetic intelligence processing. Reduced overhead by 40%.',
    tags: ['Kernel', 'AI'],
    icon: 'memory',
  },
  {
    ref: 'REF_005',
    title: 'SKY_NET_UI',
    description:
      'Orbital telemetry dashboard for satellite fleet monitoring and orbital adjustment calculations.',
    tags: ['React', 'Space'],
    icon: 'satellite_alt',
  },
  {
    ref: 'REF_006',
    title: 'GHOST_DRIVE',
    description:
      'Silent data exfiltration toolset designed for deep-layer network audits and security stress testing.',
    tags: ['Stealth', 'Python'],
    icon: 'waves',
  },
]

export function WorkPage() {
  return (
    <div className="page page--work">
      <section className="work-hero">
        <div className="work-hero__title-row">
          <span className="work-hero__bar" />
          <h1 className="headline-xl text-primary-neon work-hero__title work-hero__title--desktop">PROJECT_ARCHIVE</h1>
          <h1 className="headline-md text-primary-neon work-hero__title work-hero__title--mobile">ARCHIVE</h1>
        </div>
        <p className="label-mono work-hero__lead muted">
          A collection of neural interfaces, data architectures, and tactical UI modules developed within the YVEN
          ecosystem. Filtered by performance and stability.
        </p>
      </section>

      <div className="work-project-grid">
        {projects.map((p) => (
          <article key={p.ref} className="glass-panel work-card">
            <div className="work-card__top">
              <span className="label-mono work-card__ref">{p.ref}</span>
              <span className="material-symbols-outlined work-card__icon" aria-hidden>
                {p.icon}
              </span>
            </div>
            <h3 className="headline-md text-primary-neon work-card__title">{p.title}</h3>
            <p className="body-text muted work-card__desc">{p.description}</p>
            <div className="work-card__tags">
              {p.tags.map((t) => (
                <span key={t} className="tag label-mono">
                  {t}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>

      <section className="work-specs">
        <div className="label-mono work-specs__ribbon">TECH_SPECS_V.01</div>
        <div className="work-specs__grid">
          <div>
            <span className="label-mono muted work-specs__k">Uptime</span>
            <span className="headline-md text-primary-neon">99.99%</span>
          </div>
          <div>
            <span className="label-mono muted work-specs__k">Projects</span>
            <span className="headline-md text-primary-neon">256+</span>
          </div>
          <div>
            <span className="label-mono muted work-specs__k">Integrity</span>
            <span className="headline-md text-primary-neon">MAX</span>
          </div>
          <div>
            <span className="label-mono muted work-specs__k">Signal</span>
            <span className="headline-md text-primary-neon">STABLE</span>
          </div>
        </div>
      </section>
    </div>
  )
}
