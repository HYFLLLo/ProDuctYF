'use client';

import { useRef, useState, useEffect } from 'react';
import { motion, useInView } from 'framer-motion';
import ProjectModal from './ProjectModal';
import HudTerminal from './HudTerminal';
import styles from './Projects.module.css';

const projects = [
  {
    id: 1,
    title: '外卖夜宵爆品预测',
    subtitle: 'AI Agent × 即时零售',
    tag: '商家GMV提升助手',
    description:
      '专攻即时零售夜间场景的 AI 爆品预测助手。基于事件理解、用户情绪分析、决策三层 Agent 架构，实现精准小时级爆品预测 + 动态定价策略。',
    highlights: [
      '事件理解 Agent 事件分类准确率 97%',
      '用户情绪分析 Agent 场景识别准确率 80%',
      '决策层 Agent 爆品预测准确率 68.8%',
      '商家推荐方案采纳率 30%',
    ],
    color: '#b8ff57',
    docUrl: 'https://my.feishu.cn/wiki/A7OFwzuuzi19RHki2bec1PMEnQX?from=from_copylink',
    githubUrl: 'https://github.com/HYFLLLo/Late-night-snack-prediction',
    featured: true,
    metric: '97%',
    metricLabel: '事件理解准确率',
    background: '即时零售夜间场景正爆发式增长。美团研究院数据显示，2023年夜间即时零售订单量同比增长42%，冷饮夜间占比35%（白天仅15%），啤酒洋酒贡献线上酒水订单六成，速食品类夜间占比45%。\n\n三大核心痛点制约商家经营：\n1. 缺货损失：夜间销售额平均流失 8%-12%，单店月均损失 4000-6000 元\n2. 滞销损耗：备货失当导致的食品过期损耗率是日间的 2 倍\n3. 预测困难：商家依赖经验备货，无法精准预判热点事件带来的需求爆发',
    solution: '构建三层 Agent 协同架构，核心突破是"静态动态数据分离"策略，避免每日重复分析历史订单，节省 80%+ TOKEN 消耗：\n\n事件理解 Agent：实时采集天气、赛事、社交媒体三类动态数据，通过轻量级 LLM 进行事件分类与热度计算。关键设计：静态映射表（月/季度更新）预先建立"事件-爆品"对应关系（如世界杯→啤酒/炸鸡），新事件直接匹配映射表，无需重复分析历史数据。置信度 <70% 时触发人工复核流程。\n\n用户场景分析 Agent：基于规则引擎 + ReAct 模式的双层推理。第一层规则引擎快速匹配候选场景（看球/加班/聚会/独饮/零食等），第二层 LLM 综合用户画像、地域特性、事件上下文进行验证推理，输出带置信度的最终场景标签。\n\n决策层 Agent——多维度爆品识别引擎：核心创新点。突破单一销量维度，整合五维度加权评分——热点事件 40%、用户偏好 25%、地域特色 20%、顶流热点 10%、趋势增长 5%。得分 ≥70 分纳入爆品清单，50-70 分进入候选池等待确认。同时支持美团（即时零售，24小时小时级预测）和淘宝（电商，5天日级预测）的差异化需求。',
    result: '离线测试验证核心指标达成：\n• 事件理解 Agent 分类准确率 97%，有效覆盖赛事/娱乐/天气/社会/其他五大类型\n• 用户场景分析 Agent 场景识别准确率 80%，支持看球/加班/聚会/独饮/零食/节日特供六大场景\n• 多维度爆品引擎预测准确率 68.8%，小时级粒度输出\n• 商家推荐方案采纳率 30%，验证商业可行性\n• 核心架构优势：静态动态数据分离策略节省 80%+ TOKEN，响应延迟降低 50 倍+',
  },
  {
    id: 2,
    title: '智能客服系统',
    subtitle: 'RAG + Agent + LLM',
    tag: '坐席提效系统',
    description:
      '面向企业的 IT 智能客服系统，融合知识库检索、大语言模型与 Agent 决策链。员工侧智能问答 + 坐席侧 AI 辅助，覆盖问-答-解决全流程。',
    highlights: [
      '任务完成准确率 > 90%（100 条复杂问题评测）',
      '平均响应时间 5s，95% 请求 5s 内完成',
      'AI 直接解决率 ≥ 70%',
    ],
    color: '#00e5a0',
    docUrl: 'https://my.feishu.cn/docx/ChTGdisyZomLwrxgExhcC5BKnR1',
    githubUrl: 'https://github.com/HYFLLLo/New-Assitant',
    metric: '>90%',
    metricLabel: '任务完成准确率',
    background: '企业IT部门每天处理大量重复性桌面运维问题——电脑蓝屏、网络连不上、软件装不上、密码忘了……真正需要人工处理的高优先级问题被淹没在工单海洋里。\n\n痛点一：知识碎片化——IT运维知识散落在各种文档、手册、聊天记录里，坐席靠经验回答，新员工培训成本高。\n\n痛点二：重复问题占用人力——IT坐席60%以上工作时间在回答重复问题（如密码重置、打印机驱动安装），人力严重浪费。\n\n痛点三：响应慢体验差——员工遇小问题只能排队等坐席，夜间值班人力不足，问题无人响应。\n\n痛点四：知识库更新滞后——新系统上线、新故障出现时知识库无法及时同步，服务质量不稳定。',
    solution: '以 RAG 为核心的三层协同架构：\n\n第一层——知识库管理：坐席上传IT运维文档（PDF/Word/Markdown），系统自动完成解析→分块→向量化→入库。文档以1000字符为单位切成chunk，通过Ollama本地部署的bge-m3模型生成稠密向量，存入ChromaDB向量数据库。\n\n第二层——AI问答引擎：员工提交问题时，问答引擎同时启动两路检索：向量相似度搜索 + BM25关键词检索，两路结果通过RRF（倒数排名融合）算法合并重排，输出Top-K相关文档片段作为上下文，拼接后发给MiniMax大模型生成回答，同时输出检索质量、答案结构、关键词覆盖三维度置信度评分。\n\n第三层——分流与工单流转：置信度>0.8直接返回答案；0.6-0.8返回答案并推荐提交人工；<0.6则隐藏AI答案，自动创建工单通知坐席。坐席处理时可查看AI提取的问题类型、设备信息等元数据，并借助AI生成的质检报告草稿快速回复，形成"AI首答→低置信度转人工→坐席处理→员工反馈"闭环。',
    result: 'AI模拟100条企业IT复杂问题评测中，任务完成准确率>90%；平均问答响应时间维持5s左右，95%请求在5s内完成。验证了RAG+Agent架构在企业IT客服场景的落地可行性，显著降低坐席重复劳动、提升员工体验。',
  },
  {
    id: 3,
    title: '个人工作助手',
    subtitle: '知识管理 + 报告生成',
    tag: '个人工作效率提升',
    description:
      '面向知识工作者的 AI 生产力工具，融合知识库管理、任务意图识别与多轮对话能力。自动解析多格式文档、智能拆解任务、生成结构化报告。',
    highlights: [
      '复杂报告生成时间从数小时压缩至 1 分钟以内',
      '报告结构完整性 90%，内容相关性 85%',
      '8 种预定义模板，多格式文档支持，私有知识库检索',
    ],
    color: '#00d4ff',
    docUrl: 'https://my.feishu.cn/docx/MkWnd95QooqxNOxZpo2cabPhn0f',
    githubUrl: 'https://github.com/HYFLLLo/Personal-Work-Assistant',
    metric: '<1min',
    metricLabel: '报告生成时间',
    background: '背景：职场人每天需要产出大量结构化文档——周报、月报、竞品分析、行业研究、项目汇报等。这些报告是沟通、汇报和决策的基础，但写作过程高度重复，价值却很低。真正需要人投入智力的判断和决策，只占整个过程的很小一部分。\n\n痛点\n职场人写一份报告平均耗时 2-3 小时，流程可拆解为三段：\n1. 资料搜集——耗时 1-2 小时 手动搜索、复制、粘贴、同步到本地文档。内容散、来源杂、整理费时，且每次写报告都要重来一遍。\n2. 内容整理——耗时 30 分钟 从搜集来的资料中筛选、归纳、提炼观点。信息过载与信息不足并存，往往花了时间却抓不住重点。\n3. 格式排版——耗时 20 分钟 按模板调整章节结构、字体字号、标题层级。这些操作机械重复，但 AI 时代本不需要人来做。',
    solution: '构建「知识库优先 + 用户确认机制 + 模板化生成」的三层工作流：\n第一层：意图识别与知识库检索\n用户输入需求后，先由意图识别节点判断任务类型（生成新报告 / 修改 / 追问 / 补充），同时并行检索本地知识库。通过相关性评估判断知识库内容是否充分——充足则直接使用，不足或无关则询问用户是否启用外部搜索。这一层确保本地有资料时响应快、不乱搜。\n\n第二层：外部搜索与验证\n用户确认后，Planner 节点将任务拆解为 3-5 个搜索步骤，Executor 调用 Exa Search API 批量获取信息，Verifier 节点验证搜索结果与用户需求的相关性——跑题则自动重试，最多 3 次。搜索结果全程通过 SSE 流式推送，用户实时看到进度。\n\n第三层：模板化报告生成\n通过的验证结果由 Report Generator 节点按照预设模板（周报、月报、竞品分析等 9 种）填充生成。每一次修改自动保存版本历史（最多 5 版），支持选中段落精准修改和指定位置补充，而非全篇重写。',
    result: '平时需要几个小时整理一个复杂的报告，时间压缩到 1 分钟以内；\n报告结构完整性达到 90%，内容相关性达到 85%。',
  },
  {
    id: 4,
    title: 'ECI容器资源画像',
    subtitle: '节省资源 × 智能调度',
    tag: '资源利用率优化',
    description: '通过分析容器历史资源使用数据，为 Kubernetes 容器自动生成合理的 Request 和 Limit 推荐值，帮助管理员在资源浪费 和 稳定性风险 之间找到最优平衡。',
    highlights: [
      '基于历史数据+冗余缓冲算法，让运维人员从"凭经验猜配置"变成"有数据依据的科学决策"，同时通过变配推荐机制实现资源的动态优化',
      '智能推荐Request，降低资源浪费',
    ],
    color: '#a78bfa',
    docUrl: '#',
    githubUrl: '#',
    metric: '>30%',
    metricLabel: '资源浪费降低',
    background: '在容器化应用管理中，资源规格的合理配置是平衡性能与成本的核心挑战。Request（容器声明的最小资源需求）和 Limit（容器可使用的最大资源上限）配置不当会带来严重问题：过高的资源规格导致大量资源浪费，过低的规格带来稳定性风险，多个高优先级任务同时竞争同一节点会造成性能瓶颈。\n\n核心痛点：\n• 资源浪费 — Request 配太高，低优先级任务占用大量闲置资源\n• 稳定性风险 — Request 配太低，应用在流量波动时可能崩溃\n• 配置困难 — 管理员凭经验填写，难以科学确定合理值',
    solution: '容器资源画像 + 变配推荐机制\n\n核心公式：\n目标资源规格：Target = Recommend × (1 + Buffer)\n偏离程度：Degree = 1 - (原始Request ÷ Target)\n\n功能层级：\n• 应用层资源画像 — 在 DevOps 云渡平台配额页面开启，设置 CPU/内存资源消耗冗余比例（30%/50%/70%），根据推荐值进行资源变配\n• ECI 实例层资源画像 — 在应用详情页开启（前提是应用层画像已开启），支持按实例状态提供差异化画像\n\n变配推荐规则：\n• 升配：推荐值 > 当前配置 → 必须升配\n• 降配：推荐值 < 当前配置 且 |Degree| > 10% → 可降配\n• 保持：|Degree| ≤ 10% → 建议保持当前配置',
    result: '通过资源画像分析历史数据，生成 Request 推荐值，帮助管理员：\n• 降低资源浪费 — 推荐合理 Request，减少低优先级任务的资源闲置\n• 提升资源利用率 — 科学配置使集群资源更高效利用\n• 保障稳定性 — 预留安全缓冲，应对流量波动和突发峰值',
  },
  {
    id: 5,
    title: '存储产品功能建设',
    subtitle: '需求设计 × POC验证',
    tag: 'NAS产品设计',
    description: '负责马上云 NAS 文件存储产品的需求设计与评审，主导回收站、目录配额等关键模块的功能边界与规则梳理，同时承担云厂商 POC 用例编写与验证工作。',
    highlights: [
      '主导回收站、目录配额模块需求设计与评审，将 NAS 能力拆解为可执行的 POC 用例，对齐用例口径与验证结论，支撑采购决策',
    ],
    color: '#fb923c',
    docUrl: '#',
    githubUrl: '#',
    metric: 'POC',
    metricLabel: '用例验证完成',
    background: '马上云 NAS 文件存储是企业级云存储的核心产品，文件存储的容量管理、访问控制、数据安全是产品能力的关键组成部分。\n\n核心痛点：\n• 存储空间滥用 — 缺乏配额管控，用户可能无限制占用存储资源\n• 数据误删风险 — 缺乏回收站机制，删除后无法恢复\n• 能力边界模糊 — 云厂商 NAS 能力差异大，难以横向对比选型',
    solution: '模块一：回收站机制设计\n• 定义删除规则：普通删除 vs 永久删除的差异\n• 设计保留策略：基于时间/容量阈值的自动清理机制\n• 明确恢复流程：恢复权限、恢复路径、时间窗口\n\n模块二：目录配额管控\n• 配额粒度：目录级配额 vs 用户级配额\n• 配额告警：阈值提醒、强制限制两种模式\n• 配额继承：父子目录配额关系处理\n\n模块三：POC 用例编写\n• 能力拆解：将 NAS 功能拆解为可验证的 POC 测试用例\n• 用例口径对齐：与云厂商对接，确保测试结论可对比\n• 验证结论支撑：输出结构化 POC 报告，支撑采购决策',
    result: '• 完成 NAS 关键模块（回收站、目录配额）需求设计与评审交付，形成可评审、可落地的产品方案\n• 将 NAS 能力拆解为可执行的 POC 用例，沉淀 POC 验证用例与测试支持过程\n• 使云厂商能力边界更清晰、可复盘，支撑后续采购决策',
  },
];

function ProjectCard({ project }: { project: typeof projects[0] }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <motion.article
      ref={ref}
      className={`${styles.card} ${project.featured ? styles.featuredCard : ''}`}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      whileHover={{ scale: 1.035, y: -6 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* top accent line */}
      <div className={styles.accentLine} style={{ background: project.color }} />

      <div className={styles.inner}>
        {/* Header */}
        <div className={styles.cardHeader}>
          {project.featured && (
            <span className={styles.featuredBadge}>★ 重点推荐</span>
          )}
          <div className={styles.meta}>
            <span
              className={styles.tagChip}
              style={{
                color: project.color,
                borderColor: `${project.color}40`,
                background: `${project.color}10`,
              }}
            >
              {project.tag}
            </span>
          </div>
          <h3 className={styles.title}>{project.title}</h3>
          <p className={styles.subtitle}>{project.subtitle}</p>
        </div>

        {/* Description */}
        <p className={styles.description}>{project.description}</p>

        {/* Highlights */}
        <ul className={styles.highlights}>
          {project.highlights.map((h) => (
            <li key={h} className={styles.highlight}>
              <span className={styles.bullet} style={{ background: project.color }} />
              {h}
            </li>
          ))}
        </ul>

        {/* Footer */}
        <div className={styles.footer}>
          {project.metric !== '—' && (
            <div className={styles.metricBlock}>
              <span className={styles.metric} style={{ color: project.color }}>{project.metric}</span>
              <span className={styles.metricLabel}>{project.metricLabel}</span>
            </div>
          )}

          <div className={styles.linkGroup}>
            {project.githubUrl !== '#' && (
              <a
                href={project.githubUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.githubLink}
                style={{ '--accent': project.color } as React.CSSProperties}
              >
                <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                  <path d="M10 2C5.58 2 2 5.58 2 10c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A5.98 5.98 0 0 0 18 10c0-4.42-3.58-8-8-8z" fill="currentColor"/>
                </svg>
                GitHub
              </a>
            )}

            {project.docUrl !== '#' && (
              <a
                href={project.docUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.docLink}
                style={{ '--accent': project.color } as React.CSSProperties}
              >
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                  <path d="M9 2H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V6L9 2Z" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round"/>
                  <path d="M9 2v4h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                需求文档
              </a>
            )}
          </div>

          <button
            className={styles.detailBtn}
            onClick={() => window.dispatchEvent(new CustomEvent('openProjectModal', { detail: project }))}
          >
            查看详情
          </button>
        </div>
      </div>
    </motion.article>
  );
}

export default function Projects() {
  const [selectedProject, setSelectedProject] = useState<(typeof projects)[0] | null>(null);
  const [mousePos, setMousePos] = useState({ x: -1000, y: -1000 });
  const [isHovering, setIsHovering] = useState(false);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  useEffect(() => {
    const handler = (e: Event) => setSelectedProject((e as CustomEvent<(typeof projects)[0]>).detail);
    window.addEventListener('openProjectModal', handler);
    return () => window.removeEventListener('openProjectModal', handler);
  }, []);

  const handleMouseMove = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <section
      className={styles.section}
      id="projects"
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      {/* 鼠标跟随光晕 */}
      <div
        className={`${styles.mouseGlow} ${isHovering ? styles.mouseGlowVisible : ''}`}
        style={{ left: mousePos.x, top: mousePos.y }}
      />
      {/* 网格背景 */}
      <div className={styles.sectionBg} aria-hidden="true">
        <div className={styles.gridLines} />
        <div className={styles.glowOrb} />
      </div>
      <div className="container">
        {/* Section 1: AI 项目 */}
        <motion.div
          ref={ref}
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="section-label">Projects</p>
          <div className={styles.titleRow}>
            <h2 className="section-title">我的 AI 项目</h2>
            <a
              href="https://my.feishu.cn/docx/TKWXddETCopk8ExkvD8cLKZGnXd?from=from_copylink"
              target="_blank"
              rel="noopener noreferrer"
              className={styles.demoBtn}
            >
              <span className={styles.btnIcon} aria-hidden="true">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <polyline points="2,2 8,7 2,12" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
              <span>PLAY DEMO</span>
            </a>
          </div>
        </motion.div>

        <div className={styles.grid}>
          {projects.slice(0, 3).map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>

        {/* Section 2: 工作成果 */}
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          style={{ marginTop: '4rem' }}
        >
          <p className="section-label">Work</p>
          <div className={styles.titleRow}>
            <h2 className="section-title">我的工作成果</h2>
          </div>
        </motion.div>

        <div className={styles.workGrid}>
          {projects.slice(3, 6).map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
          {/* Animated terminal HUD panel — keeps 3-col grid rhythm */}
          <HudTerminal />
        </div>
      </div>

      <ProjectModal
        project={selectedProject}
        onClose={() => setSelectedProject(null)}
      />
    </section>
  );
}
