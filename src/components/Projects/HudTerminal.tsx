'use client';

import { useState, useEffect, useRef } from 'react';
import styles from './HudTerminal.module.css';

const CODE_LINES = [
  '> init.portfolio()',
  '> scan.modules: [ECI, NAS, RAG, AGENT]',
  '> ECI_resource.profile()',
  '>   闲置率: 23% (目标: <15%)',
  '> NAS_design.spec()',
  '>   回收站 + 目录配额 — OK',
  '> POC_validate.cases()',
  '>   12/12 PASSED',
  '> agent.workflow()',
  '>   status: DEPLOYED',
  '> _',
];

const ASCII_ART = [
  '    ╔═══╗╔═══╗    ╭─────╮',
  '    ╚═══╝╚═══╝    │░░░░░│',
  '   ╔═══════════╗   ╰──┬──╯',
  '   ░░░░░░░░░░░░░      │',
  '     ▓▓▓▓▓▓▓▓▓▓    ──┴─',
];

export default function HudTerminal() {
  const [visibleLines, setVisibleLines] = useState(0);
  const [cursorVisible, setCursorVisible] = useState(true);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const cursorIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Typewriter: advance one line every 450ms
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setVisibleLines((prev) => {
        if (prev >= CODE_LINES.length) {
          // Reset after holding at the end
          setTimeout(() => setVisibleLines(0), 1200);
          return prev;
        }
        return prev + 1;
      });
    }, 450);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  // Blink cursor
  useEffect(() => {
    cursorIntervalRef.current = setInterval(() => {
      setCursorVisible((prev) => !prev);
    }, 500);
    return () => {
      if (cursorIntervalRef.current) clearInterval(cursorIntervalRef.current);
    };
  }, []);

  return (
    <div className={styles.terminal}>
      {/* Terminal title bar */}
      <div className={styles.titleBar}>
        <span className={styles.dot} style={{ background: '#ff3366' }} />
        <span className={styles.dot} style={{ background: '#ffcc00' }} />
        <span className={styles.dot} style={{ background: '#00ff88' }} />
        <span className={styles.titleText}>Yven.Portfolio — sys.log</span>
        <span className={styles.liveIndicator}>
          <span className={styles.liveDot} />
          LIVE
        </span>
      </div>

      {/* Content area */}
      <div className={styles.content}>
        {/* ASCII art */}
        <pre className={styles.ascii} aria-hidden="true">
          {ASCII_ART.join('\n')}
        </pre>

        {/* Code lines */}
        <div className={styles.codeArea}>
          {CODE_LINES.slice(0, visibleLines).map((line, i) => (
            <div
              key={i}
              className={styles.codeLine}
              style={{ animationDelay: `${i * 0.05}s` }}
            >
              <span className={styles.lineText}>{line}</span>
            </div>
          ))}
          {/* Cursor line — shown when not at the end */}
          {visibleLines < CODE_LINES.length && (
            <div className={styles.codeLine}>
              <span
                className={styles.cursor}
                style={{ opacity: cursorVisible ? 1 : 0 }}
              >
                █
              </span>
            </div>
          )}
          {/* Persistent blinking cursor at end state */}
          {visibleLines >= CODE_LINES.length && (
            <div className={styles.codeLine}>
              <span
                className={styles.cursor}
                style={{ opacity: cursorVisible ? 1 : 0 }}
              >
                █
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Bottom accent */}
      <div className={styles.bottomBar}>
        <span className={styles.bottomText}>PID: 0xYVEN · UPTIME: 24/7</span>
        <span className={styles.bottomText}>v2.0.26</span>
      </div>
    </div>
  );
}
