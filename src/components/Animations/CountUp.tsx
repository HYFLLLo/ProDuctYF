'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './CountUp.module.css';

interface CountUpProps {
  target: number;
  suffix?: string;
  duration?: number;
  className?: string;
  style?: React.CSSProperties;
}

export default function CountUp({
  target,
  suffix = '',
  duration = 2000,
  className = '',
  style,
}: CountUpProps) {
  const [value, setValue] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const startedRef = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !startedRef.current) {
          startedRef.current = true;
          const startTime = performance.now();

          const step = (now: number) => {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            setValue(Math.floor(eased * target));
            if (progress < 1) {
              requestAnimationFrame(step);
            } else {
              setValue(target);
            }
          };

          requestAnimationFrame(step);
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [target, duration]);

  return (
    <span ref={ref} className={`${styles.count} ${className}`} style={style}>
      {value}
      {suffix}
    </span>
  );
}
