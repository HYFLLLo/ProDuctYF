'use client';

import { useEffect, useRef, useState } from 'react';

export function useCountUp(target: number, duration = 2000) {
  const [value, setValue] = useState(0);
  const ref = useRef<HTMLElement | null>(null);
  const startedRef = useRef(false);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !startedRef.current) {
          startedRef.current = true;
          const startTime = performance.now();

          const step = (now: number) => {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            setValue(Math.floor(eased * target));
            if (progress < 1) requestAnimationFrame(step);
          };

          requestAnimationFrame(step);
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [target, duration]);

  return { value, ref };
}

export function useTypewriter(text: string, speed = 80, startDelay = 0) {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);
  const startedRef = useRef(false);

  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;
    setDisplayed('');
    setDone(false);

    let i = 0;
    const timeout = setTimeout(() => {
      const interval = setInterval(() => {
        i++;
        setDisplayed(text.slice(0, i));
        if (i >= text.length) {
          clearInterval(interval);
          setDone(true);
        }
      }, speed);
      return () => clearInterval(interval);
    }, startDelay);

    return () => clearTimeout(timeout);
  }, [text, speed, startDelay]);

  return { displayed, done };
}

export function useTextDecode(text: string) {
  const [decoded, setDecoded] = useState('');
  const [active, setActive] = useState(false);
  const startedRef = useRef(false);
  const ref = useRef<HTMLElement | null>(null);

  const CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !startedRef.current) {
          startedRef.current = true;
          setActive(true);
          let frame: number;
          const totalFrames = 40;
          let frameCount = 0;

          const animate = () => {
            frameCount++;
            const progress = frameCount / totalFrames;
            const revealedCount = Math.floor(progress * text.length);

            let result = '';
            for (let i = 0; i < text.length; i++) {
              if (i < revealedCount) {
                result += text[i];
              } else {
                result += CHARS[Math.floor(Math.random() * CHARS.length)];
              }
            }
            setDecoded(result);
            if (frameCount < totalFrames) {
              frame = requestAnimationFrame(animate);
            } else {
              setDecoded(text);
            }
          };

          frame = requestAnimationFrame(animate);
          return () => cancelAnimationFrame(frame);
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [text]);

  return { decoded, ref };
}
