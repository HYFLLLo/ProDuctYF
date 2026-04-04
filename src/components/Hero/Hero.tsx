'use client';

import { motion } from 'framer-motion';
import { Typewriter, TextDecode } from '@/components/Animations';
import styles from './Hero.module.css';

const descriptions = [
  '具备 Vibe coding 的快速原型能力：已经熟练使用 Trae、Claude Code、Cursor 等工具沉淀高效工作流，用于 Demo 或原型的快速开发与方案验证，提升研发效率；',
  '具备系统架构理解力和 AI 原生思维，能够清晰设计 Agent 工作流，推动智能化方案落地；',
  '善于将"成本/效率类问题"拆解为可落地的规则与机制：在容器 ECI 资源闲置率较高的背景下，规划资源画像分层架构与风险冗余机制，有效提升资源利用率与成本效率。',
  '熟悉大模型、对话交互、提示词、RAG、多模态等基础概念与落地逻辑；',
  '持续关注海内外 AI 动态，对最新的 Agent 生态有一定了解。',
];

function AuroraBackground() {
  return (
    <div className={styles.aurora} aria-hidden="true">
      <div
        className={`${styles.auroraBlob} ${styles.auroraBlob1}`}
        style={{
          '--dx1': '80px', '--dy1': '-50px', '--ds1': '1.15',
          '--dx2': '-60px', '--dy2': '60px', '--ds2': '0.9',
          '--dx3': '40px', '--dy3': '-30px', '--ds3': '1.05',
          '--duration': '14s', '--delay': '0s',
        } as React.CSSProperties}
      />
      <div
        className={`${styles.auroraBlob} ${styles.auroraBlob2}`}
        style={{
          '--dx1': '-70px', '--dy1': '40px', '--ds1': '1.1',
          '--dx2': '50px', '--dy2': '-60px', '--ds2': '0.95',
          '--dx3': '-30px', '--dy3': '50px', '--ds3': '1.08',
          '--duration': '18s', '--delay': '-5s',
        } as React.CSSProperties}
      />
      <div
        className={`${styles.auroraBlob} ${styles.auroraBlob3}`}
        style={{
          '--dx1': '60px', '--dy1': '30px', '--ds1': '1.2',
          '--dx2': '-80px', '--dy2': '-40px', '--ds2': '0.88',
          '--dx3': '50px', '--dy3': '20px', '--ds3': '1.12',
          '--duration': '22s', '--delay': '-10s',
        } as React.CSSProperties}
      />
    </div>
  );
}

function GridBackground() {
  return (
    <div className={styles.gridBg} aria-hidden="true">
      <div className={styles.gridLines} />
      <div className={styles.glowOrb} />
    </div>
  );
}

export default function Hero() {

  return (
    <section className={styles.hero} id="hero">
      <AuroraBackground />
      <GridBackground />

      <div className={`container ${styles.content}`}>
        {/* Main heading */}
        <motion.h1
          className={styles.heading}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          <Typewriter text="咖啡因转化中…☕→💻" speed={100} startDelay={400} />
        </motion.h1>

        {/* Role */}
        <motion.div
          className={styles.role}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <span className={styles.roleText}>具备的能力/素质</span>
        </motion.div>

        {/* Description list */}
        <motion.div
          className={styles.descList}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.95, ease: [0.16, 1, 0.3, 1] }}
        >
          {descriptions.map((desc, i) => (
            <p key={i} className={styles.descItem}>
              <span className={styles.descNum}>{i + 1}.</span>
              <TextDecode
                text={desc}
                style={{ animationDelay: `${i * 0.15}s` }}
              />
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
          transition={{ delay: 1.5, duration: 0.6 }}
        >
          {['AI Agent', 'RAG', 'Next.js', 'TypeScript', 'Edge Computing', 'Python', 'PyTorch'].map((t) => (
            <span key={t} className={styles.tag}>{t}</span>
          ))}
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
        <span>向下滚动</span>
      </motion.div>
    </section>
  );
}
