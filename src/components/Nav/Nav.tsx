'use client';

import { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import styles from './Nav.module.css';

const navLinks = [
  { label: '项目&工作成果', href: '#projects' },
  { label: '经历', href: '#experience' },
];

interface NavProps {
  onWechatShine?: () => void;
}

// 文字解码特效 Hook
function useTextDecode(text: string, interval: number = 5000) {
  const [displayText, setDisplayText] = useState('');
  const frameRef = useRef<number | null>(null);
  const startTimeRef = useRef<number>(0);

  useEffect(() => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    
    const animate = (timestamp: number) => {
      if (!startTimeRef.current) startTimeRef.current = timestamp;
      const elapsed = timestamp - startTimeRef.current;
      
      // 解码时间 1.5 秒，然后保持正确文字
      const decodeDuration = 1500;
      const holdDuration = interval - decodeDuration;
      
      if (elapsed < decodeDuration) {
        // 解码中
        const progress = elapsed / decodeDuration;
        let result = '';
        for (let i = 0; i < text.length; i++) {
          const charProgress = Math.min(1, (progress * text.length - i * 0.3));
          if (charProgress >= 1 || text[i] === ' ' || text[i] === '，' || text[i] === '。' || text[i] === '|' || text[i] === '：') {
            result += text[i];
          } else {
            const randomIndex = Math.floor(Math.random() * chars.length);
            result += chars[randomIndex];
          }
        }
        setDisplayText(result);
        frameRef.current = requestAnimationFrame(animate);
      } else {
        // 保持正确文字
        setDisplayText(text);
        frameRef.current = requestAnimationFrame(animate);
      }
    };

    // 启动循环
    const startLoop = () => {
      startTimeRef.current = 0;
      frameRef.current = requestAnimationFrame(animate);
    };

    startLoop();
    const loopInterval = setInterval(startLoop, interval);

    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
      clearInterval(loopInterval);
    };
  }, [text, interval]);

  return displayText;
}

export default function Nav({ onWechatShine }: NavProps) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const taglineText = 'Hello，我是Yven，也是YuFeng.Hu';
  const decodedText = useTextDecode(taglineText, 5000);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className={`${styles.nav} ${scrolled ? styles.scrolled : ''}`}>
      <div className={styles.inner}>
        <a href="#" className={styles.logo}>
          <span className={styles.logoMark}>Y</span>
          <span className={styles.logoDot} />
        </a>

        <motion.span
          className={styles.tagline}
          initial={{ clipPath: 'inset(0 100% 0 0)' }}
          animate={{ clipPath: 'inset(0 0% 0 0)' }}
          transition={{ duration: 1.4, ease: [0.16, 1, 0.3, 1], delay: 0.5 }}
        >
          {decodedText}
        </motion.span>

        <ul className={`${styles.links} ${menuOpen ? styles.open : ''}`}>
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className={styles.link}
                onClick={() => setMenuOpen(false)}
              >
                {link.label}
              </a>
            </li>
          ))}
          <li>
            <a href="#contact" className={styles.cta} onClick={() => { setMenuOpen(false); onWechatShine?.(); }}>
              聊聊
            </a>
          </li>
        </ul>

        <button
          className={`${styles.burger} ${menuOpen ? styles.burgerOpen : ''}`}
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="菜单"
        >
          <span />
          <span />
        </button>
      </div>
    </nav>
  );
}
