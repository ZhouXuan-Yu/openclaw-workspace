import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, Sequence, Img, staticFile } from "remotion";

const IKB = "#002FA7";
const PAPER = "#fafaf8";
const GREY2 = "#d4d4d2";
const GREY3 = "#737373";
const ORANGE = "#FF6B35";
const FONT_SANS = `"Inter","Noto Sans SC",sans-serif`;
const FONT_MONO = `"IBM Plex Mono",monospace`;
const popIn = (frame, delay, d = 12) => spring({ fps: 30, frame: frame - (delay || 0), config: { damping: d } });
const sf = (frame, index, base, stg = 5) => interpolate(frame, [base + index * stg, base + index * stg + 15], [0, 1], { extrapolateRight: "clamp" });
const SCENE_DUR = 206;

// ---- 字幕系统 ----
const subtitleLines = [
  { start: 0, end: 95, text: "2026年，AI Agent 岗位爆发" },
  { start: 95, end: 179, text: "私企 vs 国企，怎么选？" },
  { start: 179, end: 261, text: "私企重项目，国企重学历" },
  { start: 261, end: 352, text: "技术栈和薪资模型完全不同" },
  { start: 352, end: 439, text: "薪资对比：私企天花板更高" },
  { start: 439, end: 609, text: "但国企公积金加保险，实际差距只有20%到30%" },
  { start: 609, end: 714, text: "私企：本科够用，项目经历大于学历" },
  { start: 714, end: 830, text: "国企：硕博起步，证书加考试加政审" },
  { start: 830, end: 940, text: "私企 Agent 岗位增长 215%" },
  { start: 940, end: 1037, text: "国企从零起步，2026春招爆发" },
  { start: 1037, end: 1126, text: "最佳入场窗口：2026年底前" },
  { start: 1126, end: 1231, text: "Python + LangChain + MCP = 你的优势" },
];

const SubtitleBar = ({ frame }) => {
  const lines = subtitleLines.filter(l => frame >= l.start && frame < l.end);
  if (lines.length === 0) return null;
  const active = lines[0];
  const localFrame = frame - active.start;
  const dur = active.end - active.start;
  const fadeIn = interpolate(localFrame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const fadeOut = interpolate(localFrame, [dur - 10, dur], [1, 0], { extrapolateRight: "clamp" });
  const opacity = Math.min(fadeIn, fadeOut);
  // 逐字高亮
  const chars = [...active.text];
  const revealCount = Math.floor(interpolate(localFrame, [0, dur * 0.6], [0, chars.length], { extrapolateRight: "clamp" }));
  return (
    <div style={{
      position: "absolute", bottom: 120, left: 0, right: 0,
      display: "flex", justifyContent: "center", alignItems: "center",
      opacity, padding: "0 64px",
    }}>
      <div style={{
        background: "rgba(0,0,0,0.72)", borderRadius: 12,
        padding: "18px 36px", maxWidth: "92%",
        display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 0,
      }}>
        {chars.map((c, i) => (
          <span key={i} style={{
            fontSize: 32, fontWeight: 600, fontFamily: FONT_SANS,
            color: i < revealCount ? "#ffffff" : "rgba(255,255,255,0.15)",
            letterSpacing: "0.02em",
            transition: "none",
          }}>{c === " " ? "\u00A0" : c}</span>
        ))}
      </div>
    </div>
  );
};
// ---- 字幕系统 END ----

const Scene1Cover = () => {
  const f = useCurrentFrame();
  const bgOp = interpolate(f, [0, 30], [0, 0.25], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, opacity: bgOp }}>
        <Img src={staticFile("bg-01.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
      <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: 8, background: `linear-gradient(90deg,${IKB},${ORANGE})` }} />
      <div style={{ padding: "96px 88px", display: "flex", flexDirection: "column", justifyContent: "center", height: "100%" }}>
        <div style={{ fontSize: 22, color: IKB, fontWeight: 600, letterSpacing: "0.08em", fontFamily: FONT_MONO, opacity: interpolate(f, [0, 20], [0, 1], { extrapolateRight: "clamp" }), marginBottom: 12 }}>2026 PwC / LinkedIn Data</div>
        <h1 style={{ fontFamily: FONT_MONO, fontSize: 78, fontWeight: 700, color: IKB, lineHeight: 1.12, marginBottom: 12, letterSpacing: "-0.03em", transform: `translateY(${interpolate(f, [10, 40], [80, 0], { extrapolateRight: "clamp" })}px)` }}>AI Agent Jobs<br />Private vs SOE<br />Which One?</h1>
        <div style={{ opacity: interpolate(f, [35, 55], [0, 1], { extrapolateRight: "clamp" }) }}><p style={{ fontSize: 28, color: GREY3, lineHeight: 1.5, fontFamily: FONT_SANS }}>50+ Real JD Deep Analysis</p></div>
        <div style={{ display: "flex", gap: 24, marginTop: 48 }}>
          <div style={{ background: IKB, color: "#fff", padding: "16px 36px", fontSize: 22, fontWeight: 600, borderRadius: 4, fontFamily: FONT_SANS, transform: `scale(${popIn(f, 60)})` }}>Private: Python 100%</div>
          <div style={{ background: ORANGE, color: "#fff", padding: "16px 36px", fontSize: 22, fontWeight: 600, borderRadius: 4, fontFamily: FONT_SANS, transform: `scale(${popIn(f, 70)})` }}>SOE: Java + Certs</div>
        </div>
      </div>
      <div style={{ position: "absolute", right: 64, bottom: 32, fontSize: 100, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>01</div>
    </AbsoluteFill>
  );
};

const Scene2Comparison = () => {
  const f = useCurrentFrame();
  const rows = [["Education", "Bachelor 65%", "Master 60%+"], ["Age Limit", "None", "29/35 cap"], ["Language", "Python 100%", "Java+Python"], ["Framework", "LangChain 80%", "Dify+Local LLM"], ["Pay Model", "Monthly+Options", "Annual+13mo"], ["Hiring", "Projects > Degree", "Certs > Degree"]];
  return (
    <AbsoluteFill>
      <Img src={staticFile("bg-02.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.15 }} />
      <div style={{ padding: "64px 72px" }}>
        <h2 style={{ fontFamily: FONT_MONO, fontSize: 56, color: IKB, marginBottom: 8, opacity: sf(f, 0, 0, 0), fontWeight: 700 }}>Core Differences</h2>
        <div style={{ display: "flex", gap: 32, marginTop: 24 }}>
          <div style={{ flex: 1, background: "rgba(255,255,255,0.92)", borderRadius: 8, padding: 28, boxShadow: "0 2px 16px rgba(0,0,0,0.06)" }}>
            <h3 style={{ fontSize: 28, fontWeight: 700, color: IKB, marginBottom: 16, fontFamily: FONT_MONO }}>Private</h3>
            {rows.map((r, i) => (<div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px solid ${GREY2}`, fontSize: 20, fontFamily: FONT_SANS, opacity: sf(f, i, 10) }}><span style={{ color: GREY3 }}>{r[0]}</span><span style={{ fontWeight: 600, color: IKB }}>{r[1]}</span></div>))}
            <div style={{ marginTop: 16, background: IKB, color: "#fff", padding: "10px 20px", borderRadius: 4, display: "inline-block", fontSize: 18, fontWeight: 600, transform: `scale(${popIn(f, 60)})` }}>High Ceiling</div>
          </div>
          <div style={{ flex: 1, background: "rgba(255,255,255,0.92)", borderRadius: 8, padding: 28, boxShadow: "0 2px 16px rgba(0,0,0,0.06)" }}>
            <h3 style={{ fontSize: 28, fontWeight: 700, color: ORANGE, marginBottom: 16, fontFamily: FONT_MONO }}>SOE</h3>
            {rows.map((r, i) => (<div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px solid ${GREY2}`, fontSize: 20, fontFamily: FONT_SANS, opacity: sf(f, i, 15) }}><span style={{ color: GREY3 }}>{r[0]}</span><span style={{ fontWeight: 600, color: ORANGE }}>{r[2]}</span></div>))}
            <div style={{ marginTop: 16, background: ORANGE, color: "#fff", padding: "10px 20px", borderRadius: 4, display: "inline-block", fontSize: 18, fontWeight: 600, transform: `scale(${popIn(f, 65)})` }}>High Stability</div>
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", right: 48, bottom: 24, fontSize: 88, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>02</div>
    </AbsoluteFill>
  );
};

const Scene3Salary = () => {
  const f = useCurrentFrame();
  const levels = [["Junior 0-2y", "8K-15K/mo", "100-180K/yr"], ["Mid 3-5y", "15K-40K+Opt", "180-300K/yr"], ["Senior 5-8y", "40K-60K+Equ", "250-400K/yr"], ["Expert 8y+", "60K-120K", "400-600K/yr"]];
  return (
    <AbsoluteFill>
      <Img src={staticFile("bg-03.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.15 }} />
      <div style={{ padding: "64px 72px" }}>
        <h2 style={{ fontFamily: FONT_MONO, fontSize: 56, color: IKB, marginBottom: 8, opacity: sf(f, 0, 0, 0), fontWeight: 700 }}>Salary Comparison</h2>
        <div style={{ display: "flex", gap: 24, padding: "12px 28px", fontSize: 20, fontWeight: 600, color: GREY3, fontFamily: FONT_MONO, opacity: sf(f, 0, 15) }}><div style={{ flex: 1 }}>Level</div><div style={{ flex: 1 }}>Private</div><div style={{ flex: 1 }}>SOE</div></div>
        {levels.map((l, i) => (<div key={i} style={{ display: "flex", gap: 24, padding: "14px 28px", borderBottom: `1px solid ${GREY2}`, fontSize: 22, fontFamily: FONT_SANS, opacity: sf(f, i, 25), background: i % 2 === 0 ? "rgba(0,47,167,0.03)" : "transparent" }}><span style={{ flex: 1, color: GREY3 }}>{l[0]}</span><span style={{ flex: 1, fontWeight: 700, color: IKB }}>{l[1]}</span><span style={{ flex: 1, fontWeight: 700, color: ORANGE }}>{l[2]}</span></div>))}
        <div style={{ marginTop: 24, padding: "18px 28px", background: "rgba(255,255,255,0.9)", borderLeft: `4px solid ${ORANGE}`, borderRadius: 4, fontSize: 20, opacity: sf(f, 0, 65), fontFamily: FONT_SANS }}>SOE housing fund 12% + insurance = Real gap only ~20-30%</div>
      </div>
      <div style={{ position: "absolute", right: 48, bottom: 24, fontSize: 88, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>03</div>
    </AbsoluteFill>
  );
};

const Scene4Barrier = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Img src={staticFile("bg-04.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.15 }} />
      <div style={{ padding: "64px 72px", height: "100%", display: "flex", flexDirection: "column" }}>
        <h2 style={{ fontFamily: FONT_MONO, fontSize: 56, color: IKB, marginBottom: 8, opacity: sf(f, 0, 0, 0), fontWeight: 700 }}>Entry Barrier</h2>
        <div style={{ display: "flex", gap: 32, flex: 1, marginTop: 32 }}>
          <div style={{ flex: 1, background: "rgba(0,47,167,0.05)", borderRadius: 12, padding: 32, opacity: sf(f, 0, 20), border: `1px solid rgba(0,47,167,0.15)` }}>
            <div style={{ fontSize: 44, marginBottom: 16 }}>Private</div>
            <h3 style={{ fontSize: 30, fontWeight: 700, color: IKB, marginBottom: 24, fontFamily: FONT_MONO }}>Good Fit</h3>
            {["Bachelor enough", "Agent project >= Degree", "AI skill premium +35%", "Age not a barrier", "10% no degree req"].map((t, i) => (<p key={i} style={{ fontSize: 24, lineHeight: 2.2, fontFamily: FONT_SANS, opacity: sf(f, i, 30) }}>+ {t}</p>))}
          </div>
          <div style={{ flex: 1, background: "rgba(255,107,53,0.05)", borderRadius: 12, padding: 32, opacity: sf(f, 0, 25), border: `1px solid rgba(255,107,53,0.15)` }}>
            <div style={{ fontSize: 44, marginBottom: 16 }}>SOE</div>
            <h3 style={{ fontSize: 30, fontWeight: 700, color: ORANGE, marginBottom: 24, fontFamily: FONT_MONO }}>Depends</h3>
            {["Master required", "Certs matter", "Exam+Interview+BG", "Age limits common", "Process 1-2 months"].map((t, i) => (<p key={i} style={{ fontSize: 24, lineHeight: 2.2, fontFamily: FONT_SANS, opacity: sf(f, i, 35) }}>- {t}</p>))}
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", right: 48, bottom: 24, fontSize: 88, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>04</div>
    </AbsoluteFill>
  );
};

const Scene5Trends = () => {
  const f = useCurrentFrame();
  const trends = [["+215%", "Private Agent Jobs Growth", "Boss/Liepin/Zhaopin latest data"], ["From Zero", "SOE Agent Jobs Emerge", "2024=0, 2026 Spring hiring surge"], ["Window", "Best Entry Before 2026 End", "MCP protocol just started, few know it"]];
  return (
    <AbsoluteFill>
      <Img src={staticFile("bg-05.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.15 }} />
      <div style={{ padding: "64px 72px" }}>
        <h2 style={{ fontFamily: FONT_MONO, fontSize: 56, color: IKB, marginBottom: 8, fontWeight: 700 }}>2026 Trends</h2>
        {trends.map((t, i) => (<div key={i} style={{ display: "flex", gap: 24, padding: "24px 28px", background: "rgba(255,255,255,0.92)", borderRadius: 8, marginBottom: 16, marginTop: i === 0 ? 32 : 0, opacity: sf(f, i, 20), boxShadow: "0 2px 8px rgba(0,0,0,0.04)" }}><div style={{ fontSize: 48, fontWeight: 200, color: IKB, fontFamily: FONT_MONO, minWidth: 72, textAlign: "center", lineHeight: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div><div style={{ flex: 1 }}><div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 6 }}><span style={{ fontSize: 36, fontWeight: 900, color: IKB, fontFamily: FONT_MONO }}>{t[0]}</span><span style={{ fontSize: 26, fontWeight: 700, fontFamily: FONT_SANS }}>{t[1]}</span></div><div style={{ fontSize: 20, color: GREY3, fontFamily: FONT_SANS }}>{t[2]}</div></div></div>))}
      </div>
      <div style={{ position: "absolute", right: 48, bottom: 24, fontSize: 88, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>05</div>
    </AbsoluteFill>
  );
};

const Scene6CTA = () => {
  const f = useCurrentFrame();
  const actions = ["Python + LangChain + RAG = Deployable Agent", "MCP Protocol = Learn now, window closing", "Complete Agent Project > Degree > Certificates"];
  return (
    <AbsoluteFill>
      <Img src={staticFile("bg-06.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.2 }} />
      <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: 8, background: `linear-gradient(90deg,${IKB},${ORANGE})` }} />
      <div style={{ padding: "72px 72px", height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <h1 style={{ fontFamily: FONT_MONO, fontSize: 64, fontWeight: 700, color: IKB, marginBottom: 40, opacity: sf(f, 0, 0, 0) }}>What Now?</h1>
        {actions.map((a, i) => (<div key={i} style={{ display: "flex", alignItems: "center", gap: 24, padding: "20px 28px", background: i === 2 ? "rgba(0,47,167,0.08)" : "rgba(255,255,255,0.92)", borderRadius: 8, marginBottom: 16, opacity: sf(f, i, 15), boxShadow: "0 2px 8px rgba(0,0,0,0.04)" }}><div style={{ fontFamily: FONT_MONO, fontSize: 40, fontWeight: 200, color: IKB, minWidth: 48, textAlign: "center" }}>{i + 1}</div><div style={{ fontSize: 26, fontWeight: 600, fontFamily: FONT_SANS }}>{a}</div></div>))}
        <div style={{ fontSize: 32, fontWeight: 700, color: IKB, marginTop: 40, fontFamily: FONT_MONO, opacity: sf(f, 0, 60) }}>Best Entry Window: Before End of 2026.</div>
      </div>
      <div style={{ position: "absolute", right: 48, bottom: 24, fontSize: 88, fontWeight: 200, color: GREY2, fontFamily: FONT_MONO }}>06</div>
    </AbsoluteFill>
  );
};

const SceneWrapper = ({ Component, sceneIndex }) => {
  const localFrame = useCurrentFrame();
  const globalFrame = localFrame + sceneIndex * SCENE_DUR;
  return (
    <AbsoluteFill>
      <Component />
      <SubtitleBar frame={globalFrame} />
    </AbsoluteFill>
  );
};

export const RemotionVideo = () => {
  const scenes = [Scene1Cover, Scene2Comparison, Scene3Salary, Scene4Barrier, Scene5Trends, Scene6CTA];
  return (<AbsoluteFill style={{ background: PAPER }}>{scenes.map((S, i) => (<Sequence key={i} from={i * SCENE_DUR} durationInFrames={SCENE_DUR}><SceneWrapper Component={S} sceneIndex={i} /></Sequence>))}</AbsoluteFill>);
};
