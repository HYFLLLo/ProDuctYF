'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import styles from './Timeline.module.css';

const experiences = [
  {
    period: '2025.07 — 2026.02',
    company: '马上消费金融股份有限公司',
    role: '产品经理 · B端 · 云计算方向（NAS/容器）',
    type: 'work',
    points: [
      '负责马上云 NAS 文件存储产品需求设计与评审，主导回收站、目录配额模块',
      '设计容器资源画像分层架构（应用层/实例层），引入风险冗余机制',
      'ECI 实例资源闲置率从 >60% 降至平均 23%，目标提升利用率 30%',
    ],
    tags: ['NAS', 'ECI', '产品设计', '资源治理', 'POC'],
    accent: '#b8ff57',
  },
  {
    period: '2022.09 — 2025.06',
    company: '电子科技大学（985）',
    role: '硕士 · 交通运输 · 研究方向：云计算/边缘计算',
    type: 'edu',
    points: [
      '研究方向：云计算、边缘计算、服务网格',
      '实习：中国移动"梧桐·鸿鹄"2024 研学夏令营（2024.6-2024.9）',
      '研究职责：负责研究无服务器函数在多云环境的交互研究',
      '成果：发表论文《Research on Intelligent Scheduling of Multi-Cloud Serverless Functions...》',
    ],
    tags: ['云计算', '边缘计算', '服务网格'],
    accent: '#00e5a0',
  },
  {
    period: '2018.09 — 2022.06',
    company: '福州大学（211）',
    role: '本科 · 自动化',
    type: 'edu',
    points: [
      '自动化专业本科，打下扎实的系统控制与编程基础',
      '本科期间积累系统思维与工程实践能力',
    ],
    tags: ['自动化', '系统工程'],
    accent: '#00d4ff',
  },
];

export default function Timeline() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section className={styles.section} id="experience">
      <div className="container">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="section-label">Experience</p>
          <h2 className="section-title">经历与背景</h2>
        </motion.div>

        <div className={styles.timeline}>
          {experiences.map((exp, i) => {
            const itemRef = useRef(null);
            const itemInView = useInView(itemRef, { once: true, margin: '-50px' });

            return (
              <motion.div
                key={exp.company + exp.period}
                ref={itemRef}
                className={styles.item}
                initial={{ opacity: 0, x: -30 }}
                animate={itemInView ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.6, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              >
                {/* Line */}
                <div className={styles.line}>
                  <div
                    className={styles.dot}
                    style={{ background: exp.accent, boxShadow: `0 0 16px ${exp.accent}60` }}
                  />
                  {i < experiences.length - 1 && (
                    <div className={styles.connector} style={{ background: `linear-gradient(to bottom, ${exp.accent}30, transparent)` }} />
                  )}
                </div>

                {/* Content */}
                <div className={styles.content}>
                  <div className={styles.periodRow}>
                    <span className={styles.period}>{exp.period}</span>
                    <span
                      className={styles.typeTag}
                      style={{ color: exp.accent, background: `${exp.accent}12`, borderColor: `${exp.accent}30` }}
                    >
                      {exp.type === 'work' ? '工作' : '教育'}
                    </span>
                  </div>

                  <h3 className={styles.company}>{exp.company}</h3>
                  <p className={styles.role}>{exp.role}</p>

                  <ul className={styles.points}>
                    {exp.points.map((p) => (
                      <li key={p} className={styles.point}>
                        <span className={styles.pointBullet} style={{ background: exp.accent }} />
                        {p}
                      </li>
                    ))}
                  </ul>

                  <div className={styles.tagRow}>
                    {exp.tags.map((t) => (
                      <span key={t} className={styles.tag}>{t}</span>
                    ))}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
