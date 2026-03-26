'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import styles from './Contact.module.css';

const links = [
  {
    label: '邮箱',
    value: 'huyufeng227@163.com',
    href: 'mailto:huyufeng227@163.com',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="2" y="4" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="1.5"/>
        <path d="M2 7l8 5.5L18 7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
    color: '#b8ff57',
  },
  {
    label: '微信',
    value: 'HYF_0227',
    href: '#',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M7 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM13 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5"/>
        <path d="M4 17c0-2.21 2.69-4 6-4s6 1.79 6 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M7 10a5 5 0 0 0 6 0" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
    color: '#00e5a0',
  },
  {
    label: 'GitHub',
    value: 'HYFLLLo',
    href: 'https://github.com/HYFLLLo',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 2C5.58 2 2 5.58 2 10c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A5.98 5.98 0 0 0 18 10c0-4.42-3.58-8-8-8z" fill="currentColor"/>
      </svg>
    ),
    color: '#8888a0',
  },
  {
    label: 'Vercel',
    value: 'vercel.com/hyfs-projects',
    href: 'https://vercel.com/hyfs-projects',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <polygon points="10 2 18 16 2 16" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
        <line x1="10" y1="8" x2="10" y2="16" stroke="currentColor" strokeWidth="1.5"/>
      </svg>
    ),
    color: '#a78bfa',
  },
];

export default function Contact() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section className={styles.section} id="contact">
      <div className={styles.bgGlow} aria-hidden="true" />
      <div className="container">
        <motion.div
          ref={ref}
          className={styles.inner}
          initial={{ opacity: 0, y: 40 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="section-label">Contact</p>
          <h2 className={`section-title ${styles.heading}`}>
            一起做点<br />有意思的东西
          </h2>
          <p className={styles.sub}>
            无论是 AI 产品合作、原型开发还是行业交流，欢迎联系。
          </p>

          <div className={styles.links}>
            {links.map((link, i) => (
              <motion.a
                key={link.label}
                href={link.href}
                target={link.href.startsWith('http') ? '_blank' : undefined}
                rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                className={styles.link}
                initial={{ opacity: 0, y: 20 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.2 + i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              >
                <span className={styles.linkIcon} style={{ color: link.color }}>
                  {link.icon}
                </span>
                <span className={styles.linkInfo}>
                  <span className={styles.linkLabel}>{link.label}</span>
                  <span className={styles.linkValue}>{link.value}</span>
                </span>
                <svg className={styles.linkArrow} width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                  <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </motion.a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
