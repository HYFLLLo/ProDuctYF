'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import styles from './Nav.module.css';

const navLinks = [
  { label: '项目&工作成果', href: '#projects' },
  { label: '经历', href: '#experience' },
];

interface NavProps {
  onWechatShine?: () => void;
}

export default function Nav({ onWechatShine }: NavProps) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className={`${styles.nav} ${scrolled ? styles.scrolled : ''}`}>
      <div className={styles.inner}>
        <a href="#" className={styles.logo}>
          <span className={styles.logoMark}>Y</span>
          <span className={styles.logoDot} />
        </a>

        <motion.span
          className={styles.tagline}
          initial={{ clipPath: 'inset(0 100% 0 0)' }}
          animate={{ clipPath: 'inset(0 0% 0 0)' }}
          transition={{ duration: 1.4, ease: [0.16, 1, 0.3, 1], delay: 0.5 }}
        >
          Hello，我是Yven，也是YuFeng.Hu
        </motion.span>

        <ul className={`${styles.links} ${menuOpen ? styles.open : ''}`}>
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className={styles.link}
                onClick={() => setMenuOpen(false)}
              >
                {link.label}
              </a>
            </li>
          ))}
          <li>
            <a href="#contact" className={styles.cta} onClick={() => { setMenuOpen(false); onWechatShine?.(); }}>
              聊聊
            </a>
          </li>
        </ul>

        <button
          className={`${styles.burger} ${menuOpen ? styles.burgerOpen : ''}`}
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="菜单"
        >
          <span />
          <span />
        </button>
      </div>
    </nav>
  );
}
