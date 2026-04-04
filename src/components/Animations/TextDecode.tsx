'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './TextDecode.module.css';

interface TextDecodeProps {
  text: string;
  className?: string;
  style?: React.CSSProperties;
}

const SCRAMBLE_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

export default function TextDecode({ text, className = '', style }: TextDecodeProps) {
  const [display, setDisplay] = useState('');
  const startedRef = useRef(false);
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !startedRef.current) {
          startedRef.current = true;
          const totalFrames = 45;
          let frame = 0;

          const animate = () => {
            frame++;
            const progress = frame / totalFrames;
            const revealedCount = Math.floor(progress * text.length);

            let result = '';
            for (let i = 0; i < text.length; i++) {
              if (i < revealedCount) {
                result += text[i];
              } else {
                result += SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
              }
            }
            setDisplay(result);
            if (frame < totalFrames) {
              requestAnimationFrame(animate);
            } else {
              setDisplay(text);
            }
          };

          requestAnimationFrame(animate);
        }
      },
      { threshold: 0.15 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [text]);

  return (
    <span ref={ref} className={`${styles.decode} ${className}`} style={style}>
      {display}
    </span>
  );
}
