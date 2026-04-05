'use client';

import { useState, useEffect } from 'react';
import styles from './SectionNav.module.css';

const sections = [
  { id: 'hero', label: '首页' },
  { id: 'projects', label: '项目&工作成果' },
  { id: 'experience', label: '经历' },
  { id: 'contact', label: '联系' },
];

export default function SectionNav() {
  const [activeSection, setActiveSection] = useState('hero');

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { threshold: 0.3 }
    );

    sections.forEach(({ id }) => {
      const element = document.getElementById(id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, []);

  const handleClick = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className={styles.nav} aria-label="页面导航">
      <div className={styles.track}>
        {sections.map((section, index) => (
          <div key={section.id} className={styles.item}>
            {/* 连接线 */}
            {index > 0 && <div className={styles.line} />}
            {/* 圆点 */}
            <button
              className={`${styles.dot} ${activeSection === section.id ? styles.active : ''}`}
              onClick={() => handleClick(section.id)}
              aria-label={`跳转到${section.label}`}
              aria-current={activeSection === section.id ? 'true' : undefined}
            >
              <span className={styles.dotInner} />
              <span className={styles.label}>{section.label}</span>
            </button>
          </div>
        ))}
      </div>
    </nav>
  );
}
