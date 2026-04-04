'use client';

import { useEffect, useState } from 'react';
import styles from './Typewriter.module.css';

interface TypewriterProps {
  text: string;
  speed?: number;
  startDelay?: number;
  className?: string;
  style?: React.CSSProperties;
  cursorClassName?: string;
}

export default function Typewriter({
  text,
  speed = 80,
  startDelay = 0,
  className = '',
  style,
}: TypewriterProps) {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);
  const startedRef = { current: false };

  useEffect(() => {
    setDisplayed('');
    setDone(false);
    startedRef.current = false;

    let timeoutId: ReturnType<typeof setTimeout>;
    let intervalId: ReturnType<typeof setInterval>;
    let i = 0;

    const startTyping = () => {
      startedRef.current = true;
      i = 0;
      intervalId = setInterval(() => {
        i++;
        setDisplayed(text.slice(0, i));
        if (i >= text.length) {
          clearInterval(intervalId);
          setDone(true);
        }
      }, speed);
    };

    timeoutId = setTimeout(startTyping, startDelay);

    return () => {
      clearTimeout(timeoutId);
      clearInterval(intervalId);
    };
  }, [text, speed, startDelay]);

  return (
    <span className={`${styles.wrapper} ${className}`} style={style}>
      <span>{displayed}</span>
      <span
        className={`${styles.cursor} ${done ? styles.cursorDone : ''}`}
        aria-hidden="true"
      >
        |
      </span>
    </span>
  );
}
