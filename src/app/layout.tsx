import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '胡雨丰 | AI 产品与系统设计师',
  description: '电子科技大学硕士，研究方向云计算/边缘计算。专注于 AI Agent、RAG 工作流的的产品设计与快速原型开发。',
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌊</text></svg>",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
