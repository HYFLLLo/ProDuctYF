import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './ProjectModal.module.css';

interface ProjectModalProps {
  project: {
    title: string;
    subtitle: string;
    tag: string;
    description: string;
    highlights: string[];
    color: string;
    metric: string;
    metricLabel: string;
    docUrl: string;
    githubUrl: string;
    background?: string;
    solution?: string;
    result?: string;
  } | null;
  onClose: () => void;
}

export default function ProjectModal({ project, onClose }: ProjectModalProps) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    
    // 打开模态框时禁止背景滚动
    if (project) {
      document.body.style.overflow = 'hidden';
    }
    
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [onClose, project]);

  return (
    <AnimatePresence>
      {project && (
        <>
          {/* Backdrop */}
          <motion.div
            className={styles.backdrop}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            className={styles.modal}
            initial={{ opacity: 0, scale: 0.92, y: 20, x: '-50%' }}
            animate={{ opacity: 1, scale: 1, y: '-50%', x: '-50%' }}
            exit={{ opacity: 0, scale: 0.95, y: 10, x: '-50%' }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            role="dialog"
            aria-modal="true"
          >
            {/* Close */}
            <button className={styles.closeBtn} onClick={onClose} aria-label="关闭">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>

            {/* Title only */}
            <div className={styles.header}>
              <h2 className={styles.title}>{project.title}</h2>
            </div>

            {/* Three sections */}
            <div className={styles.body}>
              <div className={styles.section}>
                <div className={styles.sectionHead}>
                  <span className={styles.sectionNum}>01</span>
                  <span className={styles.sectionTitle}>背景与痛点</span>
                </div>
                <p className={styles.sectionText}>
                  {project.background || '点击填写…'}
                </p>
              </div>

              <div className={styles.section}>
                <div className={styles.sectionHead}>
                  <span className={styles.sectionNum}>02</span>
                  <span className={styles.sectionTitle}>解决方案</span>
                </div>
                <p className={styles.sectionText}>
                  {project.solution || '点击填写…'}
                </p>
              </div>

              <div className={styles.section}>
                <div className={styles.sectionHead}>
                  <span className={styles.sectionNum}>03</span>
                  <span className={styles.sectionTitle}>最终结果</span>
                </div>
                <p className={styles.sectionText}>
                  {project.result || '点击填写…'}
                </p>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
