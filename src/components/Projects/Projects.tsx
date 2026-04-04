'use client';

import { useRef, useState, useEffect } from 'react';
import { motion, useInView } from 'framer-motion';
import ProjectModal from './ProjectModal';
import styles from './Projects.module.css';

const projects = [
  {
    id: 1,
    title: '外卖夜宵爆品预测',
    subtitle: 'AI Agent × 即时零售',
    tag: '商家GMV提升助手',
    description:
      '专攻即时零售夜间场景的 AI 爆品预测助手。基于事件理解、用户情绪分析、决策三层 Agent 架构，实现精准小时级爆品预测 + 动态定价策略。',
    highlights: [
      '事件理解 Agent 分类准确率 97%',
      '决策层 Agent 预测准确率 68.8%',
      'Claude Code 快速原型验证全流程',
    ],
    color: '#b8ff57',
    docUrl: 'https://my.feishu.cn/wiki/A7OFwzuuzi19RHki2bec1PMEnQX?from=from_copylink',
    githubUrl: 'https://github.com/HYFLLLo/Late-night-snack-prediction',
    featured: true,
    metric: '97%',
    metricLabel: '事件理解准确率',
    background: '',
    solution: '',
    result: '',
  },
  {
    id: 2,
    title: '智能客服系统',
    subtitle: 'RAG + Agent + LLM',
    tag: '坐席提效系统',
    description:
      '面向企业的 IT 智能客服系统，融合知识库检索、大语言模型与 Agent 决策链。员工侧智能问答 + 坐席侧 AI 辅助，覆盖问-答-解决全流程。',
    highlights: [
      '任务完成准确率 > 90%（100 条复杂问题评测）',
      '平均响应时间 5s，95% 请求 5s 内完成',
      'AI 直接解决率 ≥ 70%，满意度 4.5/5',
    ],
    color: '#00e5a0',
    docUrl: 'https://my.feishu.cn/docx/ChTGdisyZomLwrxgExhcC5BKnR1',
    githubUrl: 'https://github.com/HYFLLLo/IT-Intelligent-Customer-Service-System',
    metric: '>90%',
    metricLabel: '任务完成准确率',
    background: '',
    solution: '',
    result: '',
  },
  {
    id: 3,
    title: '个人工作助手',
    subtitle: '知识管理 + 报告生成',
    tag: '个人工作效率提升',
    description:
      '面向知识工作者的 AI 生产力工具，融合知识库管理、任务意图识别与多轮对话能力。自动解析多格式文档、智能拆解任务、生成结构化报告。',
    highlights: [
      '复杂报告生成时间从数小时压缩至 1 分钟以内',
      '报告结构完整性 90%，内容相关性 85%',
      '8 种预定义模板，多格式文档支持，私有知识库检索',
    ],
    color: '#00d4ff',
    docUrl: 'https://my.feishu.cn/docx/MkWnd95QooqxNOxZpo2cabPhn0f',
    githubUrl: 'https://github.com/HYFLLLo/Personal-Work-Assistant',
    metric: '<1min',
    metricLabel: '报告生成时间',
    background: '',
    solution: '',
    result: '',
  },
  {
    id: 4,
    title: '项目四',
    subtitle: '待填充',
    tag: '',
    description: '项目内容待填充，敬请期待…',
    highlights: [],
    color: '#888',
    docUrl: '#',
    githubUrl: '#',
    metric: '—',
    metricLabel: '待上线',
    background: '',
    solution: '',
    result: '',
  },
  {
    id: 5,
    title: '项目五',
    subtitle: '待填充',
    tag: '',
    description: '项目内容待填充，敬请期待…',
    highlights: [],
    color: '#888',
    docUrl: '#',
    githubUrl: '#',
    metric: '—',
    metricLabel: '待上线',
    background: '',
    solution: '',
    result: '',
  },
  {
    id: 6,
    title: '项目六',
    subtitle: '待填充',
    tag: '',
    description: '项目内容待填充，敬请期待…',
    highlights: [],
    color: '#888',
    docUrl: '#',
    githubUrl: '#',
    metric: '—',
    metricLabel: '待上线',
    background: '',
    solution: '',
    result: '',
  },
];

function ProjectCard({ project }: { project: typeof projects[0] }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <motion.article
      ref={ref}
      className={`${styles.card} ${project.featured ? styles.featuredCard : ''}`}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      whileHover={{ scale: 1.035, y: -6 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* top accent line */}
      <div className={styles.accentLine} style={{ background: project.color }} />

      <div className={styles.inner}>
        {/* Header */}
        <div className={styles.cardHeader}>
          {project.featured && (
            <span className={styles.featuredBadge}>★ 重点推荐</span>
          )}
          <div className={styles.meta}>
            <span
              className={styles.tagChip}
              style={{
                color: project.color,
                borderColor: `${project.color}40`,
                background: `${project.color}10`,
              }}
            >
              {project.tag}
            </span>
          </div>
          <h3 className={styles.title}>{project.title}</h3>
          <p className={styles.subtitle}>{project.subtitle}</p>
        </div>

        {/* Description */}
        <p className={styles.description}>{project.description}</p>

        {/* Highlights */}
        <ul className={styles.highlights}>
          {project.highlights.map((h) => (
            <li key={h} className={styles.highlight}>
              <span className={styles.bullet} style={{ background: project.color }} />
              {h}
            </li>
          ))}
        </ul>

        {/* Footer */}
        <div className={styles.footer}>
          <div className={styles.metricBlock}>
            <span className={styles.metric} style={{ color: project.color }}>{project.metric}</span>
            <span className={styles.metricLabel}>{project.metricLabel}</span>
          </div>

          <div className={styles.linkGroup}>
            <a
              href={project.githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.githubLink}
              style={{ '--accent': project.color } as React.CSSProperties}
            >
              <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M10 2C5.58 2 2 5.58 2 10c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A5.98 5.98 0 0 0 18 10c0-4.42-3.58-8-8-8z" fill="currentColor"/>
              </svg>
              GitHub
            </a>

            <a
              href={project.docUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.docLink}
              style={{ '--accent': project.color } as React.CSSProperties}
            >
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M9 2H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V6L9 2Z" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round"/>
                <path d="M9 2v4h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              需求文档
            </a>
          </div>

          <button
            className={styles.detailBtn}
            onClick={() => window.dispatchEvent(new CustomEvent('openProjectModal', { detail: project }))}
          >
            查看详情
          </button>
        </div>
      </div>
    </motion.article>
  );
}

export default function Projects() {
  const [selectedProject, setSelectedProject] = useState<(typeof projects)[0] | null>(null);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  useEffect(() => {
    const handler = (e: Event) => setSelectedProject((e as CustomEvent<(typeof projects)[0]>).detail);
    window.addEventListener('openProjectModal', handler);
    return () => window.removeEventListener('openProjectModal', handler);
  }, []);

  return (
    <section className={styles.section} id="projects">
      <div className="container">
        {/* Section 1: AI 项目 */}
        <motion.div
          ref={ref}
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="section-label">Projects</p>
          <h2 className="section-title}>我的 AI 项目</h2>
        </motion.div>

        <div className={styles.grid}>
          {projects.slice(0, 3).map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>

        {/* Section 2: 工作成果 */}
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          style={{ marginTop: '4rem' }}
        >
          <p className="section-label">Work</p>
          <h2 className="section-title}>我的工作成果</h2>
        </motion.div>

        <div className={styles.grid}>
          {projects.slice(3, 6).map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>
      </div>

      <ProjectModal
        project={selectedProject}
        onClose={() => setSelectedProject(null)}
      />
    </section>
  );
}
