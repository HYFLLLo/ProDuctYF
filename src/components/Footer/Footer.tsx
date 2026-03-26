'use client';

import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className="container">
        <div className={styles.inner}>
          <span className={styles.name}>胡雨丰</span>
          <span className={styles.copy}>
            © {new Date().getFullYear()} · 用 Next.js + Framer Motion 构建
          </span>
        </div>
      </div>
    </footer>
  );
}
