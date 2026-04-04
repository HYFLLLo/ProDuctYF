'use client';

import Nav from '@/components/Nav/Nav';
import Hero from '@/components/Hero/Hero';
import Projects from '@/components/Projects/Projects';
import Timeline from '@/components/Timeline/Timeline';
import Contact from '@/components/Contact/Contact';
import Footer from '@/components/Footer/Footer';
import WaveDivider from '@/components/WaveDivider/WaveDivider';
import { useState } from 'react';

export default function Home() {
  const [wechatShining, setWechatShining] = useState(false);

  return (
    <>
      <Nav onWechatShine={() => setWechatShining(true)} />
      <main>
        <Hero />
        <WaveDivider />
        <Projects />
        <WaveDivider flip />
        <Timeline />
        <WaveDivider />
        <Contact wechatShining={wechatShining} onShiningDone={() => setWechatShining(false)} />
      </main>
      <Footer />
    </>
  );
}
