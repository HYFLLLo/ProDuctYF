'use client';

import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import styles from './Hero.module.css';

const roles = [
  'AI 产品设计师',
  'RAG / Agent 架构师',
  '快速原型开发者',
  '云计算产品经理',
];

function GridBackground() {
  return (
    <div className={styles.gridBg} aria-hidden="true">
      <div className={styles.gridLines} />
      <div className={styles.glowOrb} />
    </div>
  );
}

export default function Hero() {
  const roleRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    let idx = 0;
    const el = roleRef.current;
    if (!el) return;

    const run = () => {
      el.classList.remove(styles.roleVisible);
      el.classList.add(styles.roleFade);
      setTimeout(() => {
        idx = (idx + 1) % roles.length;
        el.textContent = roles[idx];
        el.classList.remove(styles.roleFade);
        el.classList.add(styles.roleVisible);
        setTimeout(run, 2800);
      }, 400);
    };

    setTimeout(run, 1800);
  }, []);

  return (
    <section className={styles.hero} id="hero">
      <GridBackground />

      <div className={`container ${styles.content}`}>
        {/* Badge */}
        <motion.div
          className={styles.badge}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
        >
          <span className={styles.badgeDot} />
          <span>深圳 · 开放机会</span>
        </motion.div>

        {/* Main heading */}
        <motion.h1
          className={styles.heading}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          你好，我是
          <br />
          <span className={styles.name}>胡雨丰</span>
        </motion.h1>

        {/* Role */}
        <motion.div
          className={styles.role}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <span ref={roleRef} className={`${styles.roleText} ${styles.roleVisible}`}>
            {roles[0]}
          </span>
        </motion.div>

        {/* Description */}
        <motion.p
          className={styles.desc}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.95, ease: [0.16, 1, 0.3, 1] }}
        >
          电子科技大学硕士，专注云计算与服务网格。<br />
          擅长把 AI 原型做成真实产品，用 Agent 工作流解决实际问题。
        </motion.p>

        {/* CTAs */}
        <motion.div
          className={styles.ctas}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1.15, ease: [0.16, 1, 0.3, 1] }}
        >
          <a href="#projects" className={styles.btnPrimary}>
            <span>看我的项目</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
          <a href="#contact" className={styles.btnGhost}>
            联系我
          </a>
        </motion.div>

        {/* Tags */}
        <motion.div
          className={styles.tags}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2, duration: 0.6 }}
        >
          {['AI Agent', 'RAG', 'Next.js', 'TypeScript', 'Edge Computing', '服务网格'].map((t) => (
            <span key={t} className={styles.tag}>{t}</span>
          ))}
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className={styles.scrollHint}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2, duration: 0.6 }}
      >
        <div className={styles.scrollLine} />
        <span>向下滚动</span>
      </motion.div>
    </section>
  );
}
