'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Typewriter, TextDecode } from '@/components/Animations';
import styles from './Hero.module.css';

const descriptions = [
  '具备 Vibe Coding 快速原型开发经验：使用 Trae、Claude Code、Cursor 等工具建立实用工作流，支持 Demo 与原型的快速开发及方案验证，辅助提升研发效率。',
  '具备系统架构基础认知与 AI 原生思维，可参与 Agent 工作流的设计与优化，配合团队推进智能化方案落地。',
  '能将成本与效率相关问题拆解为具体规则与机制：在容器 ECI 资源闲置率较高的场景中，参与设计资源画像分层架构与风险冗余机制，相关实践对资源利用率与成本效率有所改善。',
  '了解大模型、对话交互、提示词设计、RAG、多模态等技术的基本概念与常见应用方式。',
  '持续关注国内外 AI 领域动态，对 Agent 技术生态保持学习与跟进。',
];

function GridBackground() {
  return (
    <div className={styles.gridBg} aria-hidden="true">
      <div className={styles.gridLines} />
      <div className={styles.glowOrb} />
      <div className={styles.glowOrbSecondary} />
      {/* Corner accents */}
      <div className={`${styles.cornerAccent} ${styles['cornerAccent--tl']}`} />
      <div className={`${styles.cornerAccent} ${styles['cornerAccent--tr']}`} />
      <div className={`${styles.cornerAccent} ${styles['cornerAccent--bl']}`} />
      <div className={`${styles.cornerAccent} ${styles['cornerAccent--br']}`} />
      {/* Top HUD bar */}
      <div className={styles.hudBar} />
    </div>
  );
}

export default function Hero() {
  return (
    <section className={styles.hero} id="hero">
      <GridBackground />

      <div className={`container ${styles.content}`}>
        {/* Main heading with glitch effect */}
        <motion.div
          className={styles.headingWrapper}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          <h1
            className={styles.heading}
            data-text="咖啡因转化中…☕→💻"
          >
            <Typewriter text="咖啡因转化中…☕→💻" speed={100} startDelay={400} />
          </h1>
        </motion.div>

        {/* Role badge */}
        <motion.div
          className={styles.role}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className={styles.roleBar}>
            <span className={styles.roleIndicator} />
            <span className={styles.roleText}>具备的能力 / 素质</span>
          </div>
        </motion.div>

        {/* Description list — terminal card style */}
        <motion.div
          className={styles.descList}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.95, ease: [0.16, 1, 0.3, 1] }}
        >
          {descriptions.map((desc, i) => (
            <p key={i} className={styles.descItem}>
              <span className={styles.descNum}>{String(i + 1).padStart(2, '0')}.</span>
              <span className={styles.descText}>
                <TextDecode
                  text={desc}
                  style={{ animationDelay: `${i * 0.15}s` }}
                />
              </span>
            </p>
          ))}
        </motion.div>

        {/* CTAs */}
        <motion.div
          className={styles.ctas}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1.15, ease: [0.16, 1, 0.3, 1] }}
        >
          <a href="#projects" className={styles.btnPrimary}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M2 8h12M10 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            看我的项目
          </a>
          <a href="#contact" className={styles.btnGhost}>
            联系我
          </a>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className={styles.scrollHint}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.2, duration: 0.6 }}
      >
        <div className={styles.scrollLine} />
        <span>SCROLL</span>
      </motion.div>
    </section>
  );
}
