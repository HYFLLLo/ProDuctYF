'use client';

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
