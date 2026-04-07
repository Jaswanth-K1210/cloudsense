"""Inline HTML dashboard served at GET /."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CloudSense // FinOps RL Benchmark</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,900&family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --ink:      #0e0d0b;
    --ink-2:    #15130f;
    --surface:  #1a1814;
    --rule:     #2b2822;
    --rule-2:   #3a3630;
    --paper:    #ece8df;
    --paper-2:  #c9c3b4;
    --muted:    #7d7669;
    --amber:    #e89a2b;
    --amber-2:  #ffc467;
    --green:    #7fa65a;
    --red:      #c85a4a;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: var(--ink);
    color: var(--paper);
    font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 14px;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
    font-feature-settings: "ss01", "ss02";
    overflow-x: hidden;
  }
  /* Grain overlay */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    background-image:
      radial-gradient(circle at 15% 20%, rgba(232,154,43,0.08), transparent 40%),
      radial-gradient(circle at 85% 80%, rgba(232,154,43,0.04), transparent 45%);
  }
  body::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 2;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.9 0 0 0 0 0.85 0 0 0 0 0.7 0 0 0 0.22 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    mix-blend-mode: overlay;
    opacity: 0.25;
  }
  .page { position: relative; z-index: 3; max-width: 1240px; margin: 0 auto; padding: 28px 40px 80px; }

  /* ─── Top bar ─── */
  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--rule);
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.14em;
    color: var(--muted);
  }
  .topbar .mark { color: var(--paper); }
  .topbar .mark b { color: var(--amber); font-weight: 500; }
  .status { display: inline-flex; align-items: center; gap: 8px; }
  .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 0 0 rgba(127,166,90,0.6);
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(127,166,90,0.55); }
    70%  { box-shadow: 0 0 0 9px rgba(127,166,90,0);   }
    100% { box-shadow: 0 0 0 0 rgba(127,166,90,0);     }
  }

  /* ─── Hero ─── */
  .hero {
    position: relative;
    padding: 70px 0 50px;
    border-bottom: 1px solid var(--rule);
  }
  .hero .eyebrow {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 24px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
  }
  .hero .eyebrow::before {
    content: "";
    width: 28px; height: 1px; background: var(--amber);
  }
  .hero h1 {
    font-family: "Fraunces", ui-serif, Georgia, serif;
    font-weight: 300;
    font-size: clamp(72px, 13vw, 200px);
    letter-spacing: -0.04em;
    line-height: 0.88;
    margin: 0;
    color: var(--paper);
    font-variation-settings: "opsz" 144;
  }
  .hero h1 em {
    font-style: italic;
    font-weight: 400;
    color: var(--amber);
  }
  .hero .lede {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 40px;
    align-items: end;
    margin-top: 40px;
    padding-top: 24px;
    border-top: 1px dashed var(--rule);
  }
  .hero .lede p {
    max-width: 62ch;
    color: var(--paper-2);
    font-size: 14px;
    margin: 0;
  }
  .hero .lede p b { color: var(--paper); font-weight: 500; }
  .meta-block {
    text-align: right;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    line-height: 1.9;
  }
  .meta-block span { color: var(--paper); }

  /* ─── Ticker strip ─── */
  .ticker {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border-bottom: 1px solid var(--rule);
  }
  .ticker > div {
    padding: 26px 24px;
    border-right: 1px solid var(--rule);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .ticker > div:last-child { border-right: none; }
  .ticker .k {
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .ticker .v {
    font-family: "Fraunces", serif;
    font-size: 38px;
    font-weight: 300;
    letter-spacing: -0.02em;
    color: var(--paper);
    font-variation-settings: "opsz" 72;
  }
  .ticker .v .unit { font-size: 14px; color: var(--amber); margin-left: 4px; font-family: "JetBrains Mono", monospace; }
  .ticker .sub { font-size: 11px; color: var(--paper-2); }

  /* ─── Section heading ─── */
  .section {
    padding: 56px 0 28px;
    border-bottom: 1px solid var(--rule);
  }
  .section-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 36px;
  }
  .section-head .idx {
    font-size: 10px;
    letter-spacing: 0.2em;
    color: var(--amber);
    text-transform: uppercase;
  }
  .section-head h2 {
    font-family: "Fraunces", serif;
    font-weight: 300;
    font-size: 36px;
    letter-spacing: -0.02em;
    margin: 0;
    color: var(--paper);
  }
  .section-head h2 em { font-style: italic; color: var(--amber); }

  /* ─── Task cards ─── */
  .tasks {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    border: 1px solid var(--rule);
  }
  .task {
    padding: 28px 26px 24px;
    border-right: 1px solid var(--rule);
    display: flex;
    flex-direction: column;
    gap: 14px;
    background: transparent;
    transition: background 300ms ease;
    position: relative;
  }
  .task:last-child { border-right: none; }
  .task:hover { background: var(--ink-2); }
  .task:hover .arrow { transform: translateX(4px); color: var(--amber); }
  .task .tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .task .tag::before {
    content: "";
    width: 8px; height: 8px;
    background: var(--amber);
    display: inline-block;
  }
  .task.easy   .tag::before { background: var(--green); }
  .task.medium .tag::before { background: var(--amber); }
  .task.hard   .tag::before { background: var(--red);   }
  .task h3 {
    font-family: "Fraunces", serif;
    font-weight: 400;
    font-size: 28px;
    margin: 0;
    color: var(--paper);
    letter-spacing: -0.01em;
    line-height: 1.1;
  }
  .task p {
    color: var(--paper-2);
    font-size: 12.5px;
    margin: 0;
    min-height: 70px;
  }
  .task .stats {
    display: flex;
    justify-content: space-between;
    padding-top: 18px;
    border-top: 1px dashed var(--rule);
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
  .task .stats b {
    display: block;
    font-family: "Fraunces", serif;
    font-size: 22px;
    font-weight: 400;
    font-style: normal;
    color: var(--paper);
    margin-top: 4px;
    text-transform: none;
    letter-spacing: -0.01em;
  }
  .task .stats .score b { color: var(--amber); }
  .task .arrow {
    position: absolute;
    top: 26px; right: 24px;
    color: var(--muted);
    transition: transform 300ms ease, color 300ms ease;
    font-family: "JetBrains Mono", monospace;
  }

  /* ─── Two-col: actions + endpoints ─── */
  .two-col {
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: 48px;
  }
  .col h4 {
    font-family: "JetBrains Mono", monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--amber);
    margin: 0 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--rule);
  }
  .list {
    display: flex;
    flex-direction: column;
  }
  .list .row {
    display: grid;
    grid-template-columns: 28px 1fr auto;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px dashed var(--rule);
    align-items: baseline;
  }
  .list .row:last-child { border-bottom: none; }
  .list .num {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.1em;
  }
  .list .name {
    color: var(--paper);
    font-size: 13px;
  }
  .list .name b {
    color: var(--amber);
    font-weight: 500;
  }
  .list .desc {
    font-size: 11.5px;
    color: var(--paper-2);
    text-align: right;
  }
  .endpoint {
    display: grid;
    grid-template-columns: 52px 1fr;
    gap: 14px;
    padding: 13px 0;
    border-bottom: 1px dashed var(--rule);
    align-items: center;
  }
  .endpoint:last-child { border-bottom: none; }
  .method {
    font-size: 9.5px;
    letter-spacing: 0.1em;
    padding: 4px 0;
    text-align: center;
    color: var(--ink);
    background: var(--paper);
    font-weight: 700;
  }
  .method.post { background: var(--amber); }
  .endpoint a {
    color: var(--paper);
    text-decoration: none;
    font-size: 13px;
    border-bottom: 1px solid transparent;
    transition: border-color 200ms, color 200ms;
  }
  .endpoint a:hover {
    color: var(--amber);
    border-color: var(--amber);
  }
  .endpoint span.note {
    display: block;
    font-size: 10.5px;
    color: var(--muted);
    margin-top: 2px;
  }

  /* ─── CTA footer ─── */
  .cta {
    padding: 72px 0 40px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 40px;
    align-items: end;
    border-bottom: 1px solid var(--rule);
  }
  .cta h3 {
    font-family: "Fraunces", serif;
    font-weight: 300;
    font-size: clamp(44px, 6vw, 78px);
    letter-spacing: -0.03em;
    line-height: 0.95;
    margin: 0;
    color: var(--paper);
    max-width: 14ch;
  }
  .cta h3 em { font-style: italic; color: var(--amber); }
  .btns { display: flex; flex-direction: column; gap: 10px; }
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    gap: 28px;
    padding: 14px 20px;
    border: 1px solid var(--rule-2);
    color: var(--paper);
    text-decoration: none;
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    transition: all 200ms ease;
    min-width: 240px;
  }
  .btn:hover {
    background: var(--amber);
    color: var(--ink);
    border-color: var(--amber);
  }
  .btn.primary {
    background: var(--amber);
    color: var(--ink);
    border-color: var(--amber);
  }
  .btn.primary:hover {
    background: var(--amber-2);
    border-color: var(--amber-2);
  }
  .btn .ar { font-family: "JetBrains Mono", monospace; }

  /* ─── Footer ─── */
  footer.foot {
    padding-top: 26px;
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
  }
  footer.foot a { color: var(--muted); text-decoration: none; }
  footer.foot a:hover { color: var(--amber); }

  /* ─── Reveal ─── */
  .reveal { opacity: 0; transform: translateY(20px); animation: rise 900ms cubic-bezier(.2,.7,.1,1) forwards; }
  .r1 { animation-delay: 80ms; }
  .r2 { animation-delay: 200ms; }
  .r3 { animation-delay: 340ms; }
  .r4 { animation-delay: 460ms; }
  .r5 { animation-delay: 580ms; }
  .r6 { animation-delay: 700ms; }
  @keyframes rise {
    to { opacity: 1; transform: translateY(0); }
  }

  /* ─── Responsive ─── */
  @media (max-width: 900px) {
    .page { padding: 20px 22px 60px; }
    .hero { padding: 40px 0 36px; }
    .hero .lede { grid-template-columns: 1fr; gap: 20px; }
    .meta-block { text-align: left; }
    .ticker { grid-template-columns: repeat(2, 1fr); }
    .ticker > div:nth-child(2) { border-right: none; }
    .ticker > div:nth-child(1), .ticker > div:nth-child(2) { border-bottom: 1px solid var(--rule); }
    .tasks { grid-template-columns: 1fr; }
    .task { border-right: none; border-bottom: 1px solid var(--rule); }
    .task:last-child { border-bottom: none; }
    .two-col { grid-template-columns: 1fr; gap: 40px; }
    .cta { grid-template-columns: 1fr; }
    .btn { min-width: auto; width: 100%; }
  }
</style>
</head>
<body>
<div class="page">

  <!-- ───── Top bar ───── -->
  <div class="topbar reveal r1">
    <div class="mark">CLOUD<b>SENSE</b> &nbsp;/&nbsp; OPENENV BENCHMARK</div>
    <div class="status"><span class="dot"></span> ENVIRONMENT ONLINE &nbsp;·&nbsp; V1.0.0</div>
  </div>

  <!-- ───── Hero ───── -->
  <section class="hero">
    <div class="eyebrow reveal r2">FINOPS · REINFORCEMENT LEARNING · Q1 2025</div>
    <h1 class="reveal r3">Teach&nbsp;agents<br/>to spend <em>wisely.</em></h1>
    <div class="lede reveal r4">
      <p>
        CloudSense is an OpenEnv-compatible RL benchmark that simulates real AWS accounts
        with authentic pricing, utilization, and dependency graphs. Agents must identify
        waste, optimize spend, and reason about <b>blast radius</b> &mdash; the cascading
        infrastructure impact of every action &mdash; without breaking production.
      </p>
      <div class="meta-block">
        Issue No. <span>001</span><br/>
        Region <span>US-EAST-1</span><br/>
        Pricing <span>ON-DEMAND</span><br/>
        Model <span>QWEN 2.5 72B</span>
      </div>
    </div>
  </section>

  <!-- ───── Ticker strip ───── -->
  <div class="ticker reveal r5">
    <div>
      <div class="k">Tasks</div>
      <div class="v">03</div>
      <div class="sub">Easy / Medium / Hard</div>
    </div>
    <div>
      <div class="k">Resources</div>
      <div class="v">61<span class="unit">total</span></div>
      <div class="sub">6 · 15 · 40 per task</div>
    </div>
    <div>
      <div class="k">Monthly spend</div>
      <div class="v">$18.3<span class="unit">k</span></div>
      <div class="sub">Summed across accounts</div>
    </div>
    <div>
      <div class="k">Blast levels</div>
      <div class="v">05</div>
      <div class="sub">None → Critical</div>
    </div>
  </div>

  <!-- ───── Tasks ───── -->
  <section class="section">
    <div class="section-head">
      <div>
        <div class="idx">§ 01 &nbsp;·&nbsp; CURRICULUM</div>
      </div>
      <h2>Three <em>escalating</em> scenarios</h2>
    </div>

    <div class="tasks">
      <div class="task easy">
        <div class="tag">EASY · STARTUP</div>
        <h3>Startup<br/>Cleanup</h3>
        <p>A 6-resource dev/staging account. Obvious waste, no production, no dependencies. Tests basic cost-optimization fundamentals.</p>
        <div class="stats">
          <div>Steps<b>10</b></div>
          <div>Spend<b>$627</b></div>
          <div class="score">Baseline<b>0.94</b></div>
        </div>
        <div class="arrow">→</div>
      </div>
      <div class="task medium">
        <div class="tag">MEDIUM · MID-SIZE</div>
        <h3>Mid-Size<br/>Audit</h3>
        <p>15 resources mixing prod and non-prod. Must distinguish seasonal spikes, failover replicas, and expiring reservations from genuine waste.</p>
        <div class="stats">
          <div>Steps<b>20</b></div>
          <div>Spend<b>$3.5k</b></div>
          <div class="score">Baseline<b>0.78</b></div>
        </div>
        <div class="arrow">→</div>
      </div>
      <div class="task hard">
        <div class="tag">HARD · ENTERPRISE</div>
        <h3>Enterprise<br/>FinOps</h3>
        <p>40 interdependent resources. Cross-region replication, oversized Elasticsearch, NAT Gateway traps. Requires blast-radius reasoning.</p>
        <div class="stats">
          <div>Steps<b>45</b></div>
          <div>Spend<b>$14.2k</b></div>
          <div class="score">Baseline<b>0.76</b></div>
        </div>
        <div class="arrow">→</div>
      </div>
    </div>
  </section>

  <!-- ───── Actions + Endpoints ───── -->
  <section class="section">
    <div class="section-head">
      <div><div class="idx">§ 02 &nbsp;·&nbsp; REFERENCE</div></div>
      <h2>Action space <em>&amp;</em> API</h2>
    </div>

    <div class="two-col">
      <div class="col">
        <h4>Action Space / 09 verbs</h4>
        <div class="list">
          <div class="row"><div class="num">01</div><div class="name"><b>rightsize_resource</b></div><div class="desc">shrink to cheaper instance type</div></div>
          <div class="row"><div class="num">02</div><div class="name"><b>terminate_resource</b></div><div class="desc">remove unused infrastructure</div></div>
          <div class="row"><div class="num">03</div><div class="name"><b>add_lifecycle_policy</b></div><div class="desc">S3 tiering · ~70% savings</div></div>
          <div class="row"><div class="num">04</div><div class="name"><b>enable_autoscaling</b></div><div class="desc">dynamic capacity · ~20% savings</div></div>
          <div class="row"><div class="num">05</div><div class="name"><b>purchase_reservation</b></div><div class="desc">steady workloads · ~30% savings</div></div>
          <div class="row"><div class="num">06</div><div class="name"><b>change_storage_class</b></div><div class="desc">Glacier / IA tiers</div></div>
          <div class="row"><div class="num">07</div><div class="name"><b>schedule_uptime</b></div><div class="desc">business-hours only</div></div>
          <div class="row"><div class="num">08</div><div class="name"><b>request_more_info</b></div><div class="desc">defer, gather context</div></div>
          <div class="row"><div class="num">09</div><div class="name"><b>skip_resource</b></div><div class="desc">safe for critical prod</div></div>
        </div>
      </div>

      <div class="col">
        <h4>HTTP Endpoints / OpenEnv</h4>
        <div class="endpoint">
          <div class="method">GET</div>
          <div><a href="/health">/health</a><span class="note">liveness probe</span></div>
        </div>
        <div class="endpoint">
          <div class="method">GET</div>
          <div><a href="/version">/version</a><span class="note">name · version · api level</span></div>
        </div>
        <div class="endpoint">
          <div class="method">GET</div>
          <div><a href="/tasks">/tasks</a><span class="note">list available scenarios</span></div>
        </div>
        <div class="endpoint">
          <div class="method post">POST</div>
          <div><a href="/docs#/default/reset_reset_post">/reset?task_id=&lt;id&gt;</a><span class="note">begin a new episode</span></div>
        </div>
        <div class="endpoint">
          <div class="method post">POST</div>
          <div><a href="/docs#/default/step_step_post">/step</a><span class="note">execute action · JSON body</span></div>
        </div>
        <div class="endpoint">
          <div class="method">GET</div>
          <div><a href="/state">/state</a><span class="note">current observation</span></div>
        </div>
        <div class="endpoint">
          <div class="method post">POST</div>
          <div><a href="/docs#/default/close_close_post">/close</a><span class="note">end current episode</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ───── CTA ───── -->
  <section class="cta">
    <h3>Run the<br/>benchmark<br/><em>yourself.</em></h3>
    <div class="btns">
      <a class="btn primary" href="/docs"><span>OPEN API DOCS</span><span class="ar">→</span></a>
      <a class="btn" href="/tasks"><span>LIST TASKS</span><span class="ar">→</span></a>
      <a class="btn" href="https://github.com/Jaswanth-K1210/cloudsense" target="_blank" rel="noopener"><span>SOURCE · GITHUB</span><span class="ar">↗</span></a>
      <a class="btn" href="https://huggingface.co/spaces/Jaswanth-K/cloudsense" target="_blank" rel="noopener"><span>SPACE · HUGGING FACE</span><span class="ar">↗</span></a>
    </div>
  </section>

  <footer class="foot">
    <div>© CLOUDSENSE · OPENENV FINOPS BENCHMARK</div>
    <div>AWS US-EAST-1 · ON-DEMAND · Q1 2025</div>
  </footer>

</div>
</body>
</html>"""
