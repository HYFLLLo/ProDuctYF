import Nav from '@/components/Nav/Nav';
import Hero from '@/components/Hero/Hero';
import Projects from '@/components/Projects/Projects';
import Timeline from '@/components/Timeline/Timeline';
import Contact from '@/components/Contact/Contact';
import Footer from '@/components/Footer/Footer';

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Projects />
        <Timeline />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
