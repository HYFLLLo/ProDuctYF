'use client';

import styles from './WaveDivider.module.css';

interface WaveDividerProps {
  topSection?: string; // css color of section above
  bottomSection?: string; // css color of section below
  flip?: boolean; // flip vertically
  className?: string;
}

export default function WaveDivider({
  flip = false,
  className = '',
}: WaveDividerProps) {
  return (
    <div className={`${styles.wrapper} ${flip ? styles.flip : ''} ${className}`}>
      <svg
        className={styles.wave}
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <path
          className={styles.path}
          d="M0,40 C180,80 360,0 540,40 C720,80 900,0 1080,40 C1260,80 1380,20 1440,40 L1440,80 L0,80 Z"
          fill="currentColor"
        />
        <path
          className={`${styles.path} ${styles.path2}`}
          d="M0,50 C200,10 400,70 600,30 C800,-10 1000,60 1200,30 C1320,12 1400,40 1440,50 L1440,80 L0,80 Z"
          fill="currentColor"
          opacity="0.4"
        />
      </svg>
    </div>
  );
}
