'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import Image from 'next/image';
import styles from './Projects.module.css';

const projects = [
  {
    id: 1,
    title: '外卖夜宵爆品预测',
    subtitle: 'AI Agent × 即时零售',
    tag: 'AI 产品原型',
    description:
      '为中小便利店与闪电仓商家打造的夜间场景 AI 爆品预测助手。基于事件理解、用户情绪分析、决策三层 Agent 架构，实现精准小时级爆品预测 + 动态定价策略。',
    highlights: [
      '事件理解 Agent 分类准确率 97%',
      '决策层 Agent 预测准确率 68.8%',
      'Claude Code 快速原型验证全流程',
    ],
    tech: ['Claude Code', 'Agent SOP', 'RAG', 'ReAct', '混合检索'],
    color: '#b8ff57',
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    img: null as string | null,
    metric: '97%',
    metricLabel: '事件理解准确率',
  },
  {
    id: 2,
    title: '智能客服系统',
    subtitle: 'RAG + Agent + LLM',
    tag: '企业 AI 产品',
    description:
      '面向企业的 IT 智能客服系统，融合知识库检索、大语言模型与 Agent 决策链。员工侧智能问答 + 坐席侧 AI 辅助处理，覆盖问-答-解决全流程。',
    highlights: [
      '任务完成准确率 > 90%（100 条复杂问题评测）',
      '平均响应时间 5s，支持 95% 请求 5s 内完成',
      'AI 直接解决率 ≥ 70%，满意度 4.5/5',
    ],
    tech: ['LLM', '向量检索', 'ReAct', '思维链', '知识库管理'],
    color: '#00e5a0',
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    img: null as string | null,
    metric: '>90%',
    metricLabel: '任务完成准确率',
  },
];

function ProjectCard({ project, index }: { project: typeof projects[0]; index: number }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <motion.article
      ref={ref}
      className={styles.card}
      initial={{ opacity: 0, y: 60 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.7, delay: index * 0.15, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Left: info */}
      <div className={styles.info}>
        <div className={styles.meta}>
          <span className={styles.tag} style={{ color: project.color, borderColor: `${project.color}40`, background: `${project.color}10` }}>
            {project.tag}
          </span>
          <span className={styles.index}>0{project.id}</span>
        </div>

        <h3 className={styles.title}>{project.title}</h3>
        <p className={styles.subtitle}>{project.subtitle}</p>
        <p className={styles.description}>{project.description}</p>

        <ul className={styles.highlights}>
          {project.highlights.map((h) => (
            <li key={h} className={styles.highlight}>
              <span className={styles.bullet} style={{ background: project.color }} />
              {h}
            </li>
          ))}
        </ul>

        <div className={styles.techRow}>
          {project.tech.map((t) => (
            <span key={t} className={styles.tech}>{t}</span>
          ))}
        </div>

        <div className={styles.metricBlock}>
          <span className={styles.metric} style={{ color: project.color }}>{project.metric}</span>
          <span className={styles.metricLabel}>{project.metricLabel}</span>
        </div>
      </div>

      {/* Right: visual */}
      <div className={styles.visual}>
        <div className={styles.visualInner} style={{ '--accent': project.color } as React.CSSProperties}>
          {/* Abstract tech diagram placeholder */}
          <div className={styles.diagram}>
            <div className={styles.diagramGrid}>
              {Array.from({ length: 16 }).map((_, i) => (
                <div key={i} className={styles.diagramCell} />
              ))}
            </div>
            <div className={styles.diagramContent}>
              <div className={styles.diagramNode} style={{ '--i': 0, '--accent': project.color } as React.CSSProperties}>
                <span>事件理解</span>
              </div>
              <div className={styles.diagramNode} style={{ '--i': 1, '--accent': project.color } as React.CSSProperties}>
                <span>情绪分析</span>
              </div>
              <div className={styles.diagramNode} style={{ '--i': 2, '--accent': project.color } as React.CSSProperties}>
                <span>决策Agent</span>
              </div>
              <div className={styles.diagramConns}>
                <svg viewBox="0 0 200 80" fill="none" className={styles.connSvg}>
                  <path d="M 40 20 Q 70 20 100 40" stroke="currentColor" strokeWidth="1" strokeDasharray="3 3"/>
                  <path d="M 140 20 Q 170 20 160 40" stroke="currentColor" strokeWidth="1" strokeDasharray="3 3"/>
                  <path d="M 100 60 L 100 40" stroke="currentColor" strokeWidth="1" strokeDasharray="3 3"/>
                </svg>
              </div>
            </div>
          </div>

          <div className={styles.visualLabel} style={{ color: project.color }}>
            <span>{project.title}</span>
          </div>
        </div>
      </div>
    </motion.article>
  );
}

export default function Projects() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section className={styles.section} id="projects">
      <div className="container">
        <motion.div
          ref={ref}
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="section-label">Projects</p>
          <h2 className="section-title">真实落地的 AI 项目</h2>
          <p className={styles.sub}>
            不只是 Demo，是从需求到原型到评测验证的完整闭环
          </p>
        </motion.div>

        <div className={styles.grid}>
          {projects.map((p, i) => (
            <ProjectCard key={p.id} project={p} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
