const nodes = [
  {
    id: 'NODE_01',
    label: 'WeChat',
    icon: 'chat_bubble',
    hint: 'ESTABLISH LINK',
    href: '#wechat',
  },
  {
    id: 'NODE_02',
    label: 'GitHub',
    icon: 'terminal',
    hint: 'SOURCE_ACCESS',
    href: 'https://github.com',
  },
  {
    id: 'NODE_03',
    label: 'RED',
    icon: 'share_reviews',
    hint: 'LIFESTYLE_FEED',
    href: '#red',
  },
] as const

export function ContactPage() {
  return (
    <div className="page page--contact">
      <div className="contact-meta label-mono">
        <div className="contact-meta__left">
          <span className="contact-meta__dot" />
          <span>Status: Secure_Protocol_Active</span>
        </div>
        <span>Target: YVEN_OS</span>
      </div>

      <section className="contact-section">
        <div className="contact-avatar" aria-hidden>
          <div className="contact-avatar__halo" />
          <div className="contact-avatar__ring" />
          <div className="contact-avatar__core">
            <span className="material-symbols-outlined contact-avatar__print">fingerprint</span>
            <div className="label-mono contact-avatar__tag">REF_USR_001</div>
          </div>
        </div>

        <div className="contact-brand copy-block">
          <h1 className="headline-xl text-primary-neon contact-brand__title">NEURAL_LINK</h1>
          <p className="body-text muted">
            Initiating secure handshake. Select a communication node below to establish a direct uplink with Yven&apos;s
            neural archive.
          </p>
        </div>

        <div className="contact-nodes">
          {nodes.map((n) => (
            <a
              key={n.id}
              href={n.href}
              className="contact-node"
              {...(n.href.startsWith('http') ? { target: '_blank', rel: 'noreferrer' } : {})}
            >
              <span className="label-mono contact-node__id">{n.id}</span>
              <span className="material-symbols-outlined contact-node__icon">{n.icon}</span>
              <span className="label-mono contact-node__label">{n.label}</span>
              <div className="contact-node__line" />
              <span className="label-mono contact-node__hint">{n.hint}</span>
            </a>
          ))}
        </div>

        <div className="contact-form">
          <label className="label-mono contact-form__label" htmlFor="contact-msg">
            Transmit Message
          </label>
          <div className="contact-form__field">
            <input
              id="contact-msg"
              className="contact-form__input label-mono"
              placeholder="SECURE_CHANNEL@YVEN.LOG"
              type="email"
              autoComplete="email"
            />
            <button type="button" className="contact-form__send" aria-label="发送">
              <span className="material-symbols-outlined">send</span>
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}
