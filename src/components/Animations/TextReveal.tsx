import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import styles from './TextReveal.module.css';

interface TextRevealProps {
  text: string;
  className?: string;
  startDelay?: number;
  duration?: number;
}

export default function TextReveal({
  text,
  className = '',
  startDelay = 0,
  duration = 1.2,
}: TextRevealProps) {
  return (
    <motion.div
      className={`${styles.wrapper} ${className}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3, delay: startDelay }}
    >
      <div className={styles.clipContainer}>
        <motion.span
          className={styles.text}
          initial={{ clipPath: 'inset(0 100% 0 0)' }}
          animate={{ clipPath: 'inset(0 0% 0 0)' }}
          transition={{
            duration,
            ease: [0.16, 1, 0.3, 1],
            delay: startDelay + 0.3,
          }}
        >
          {text}
        </motion.span>
      </div>
    </motion.div>
  );
}
