# Research note — Optional mini-module: LLM-assisted replication in economics

Verified 2026-08-28. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

| Claim in SPEC | Status | Evidence |
|---|---|---|
| "Scott Cunningham-style workflow of using coding agents to reproduce published results" | VERIFIED (exists) — **mostly paywalled** | Cunningham (Baylor) runs a 50+ post "Claude Code" series on [Scott's Mixtape Substack](https://causalinf.substack.com/). Directly on-topic: *Claude Code 15: Can LLMs Replicate a PNAS Paper? (Part 2)* — replicated Card et al.'s immigration-rhetoric classification with gpt-4o-mini for **$10.99, 2.6h compute, 69% agreement** ([post](https://causalinf.substack.com/p/claude-code-15-the-results-are-in), `isAccessibleForFree: false`); *Claude Code 24: Multiple Agents Auditing Your Diff-in-Diff Code* — same spec run through Stata `csdid`/`csdid2`, R `did`, Python `diff-diff`/`differences`, "almost never do they agree" ([post](https://causalinf.substack.com/p/claude-code-24-multiple-agents-auditing), paywalled). **Free**: [How and why I am using hooks (part 1)](https://causalinf.substack.com/p/how-and-why-i-am-using-hooks-part) (« don't edit raw data » enforced by hooks), his tooling repo [MixtapeTools](https://github.com/scunning1975/mixtapetools), and the interview [The AI Economist, 2026-06-12](https://www.aieconomist.io/articles/scott-cunningham-claude-code-ai-economists) (verification with Caitlin Myers found data issues the agent missed; "econometric knowledge becomes more valuable"). Substack paywalled posts can be unlocked once per reader via "claim my free post" — not a course-grade link. |
| "Published examples of LLM-assisted replication in economics" (2–3) | VERIFIED, **thin in economics proper** | (1) Brodeur et al., *Comparing Human-Only, AI-Assisted, and AI-Led Teams on Assessing Research Reproducibility in Quantitative Social Science*, I4R DP 195 / IZA DP 17645, 2025, in press PNAS 2026 — 288 researchers, 103 teams, 3 arms; human-only ≈ AI-assisted ≫ AI-led (**+57 pp** success for humans over AI-led); AI-assisted found 0.4 more major errors/team than AI-led ([IZA page](https://www.iza.org/publications/dp/17645/comparing-human-only-ai-assisted-and-ai-led-teams-on-assessing-research-reproducibility-in-quantitative-social-science), [free PDF](https://docs.iza.org/dp17645.pdf)). (2) Kohler, Zollikofer, Einsiedler, Hoyle & Ash, *Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results*, [arXiv 2604.21965](https://arxiv.org/abs/2604.21965) (Apr 2026) — 48 papers, 4 scaffolds × 4 LLMs, agents recover results from methods + data without original code; best agents: sign agreement > 85%, within 95% CI > 70%; failures split between agent limits and under-specified papers. (3) Xu & Yang, *Scaling Reproducibility: An AI-Assisted Workflow for Large-Scale Replication and Reanalysis*, [arXiv 2602.16733](https://arxiv.org/abs/2602.16733) (Feb 2026) — 384 political-science studies / 3,523 models; reproducibility 20.8% → 82.5% after DA-RT; 92.1% when packages accessible. Adjacent: HLER multi-agent econ pipeline [arXiv 2603.07444](https://arxiv.org/abs/2603.07444); CORE-Bench [arXiv 2409.11363](https://arxiv.org/abs/2409.11363). **Verdict**: peer-reviewed *economics* examples = Brodeur et al. only (and it is about *assessment*, mixed social-science sample). Frame the module as "early evidence from social science", not "established economics practice". |
| "Agents good at re-running pipelines, translating Stata→Python/R, spotting undocumented steps" | VERIFIED (partially) | Kohler et al. and Xu & Yang support re-running/reimplementing; Cunningham CC24 supports cross-language translation *and* shows packages disagree — translation is a source of discrepancies, not just a fix. |
| "Not good at judging identification, silently fixing discrepancies" | VERIFIED | Brodeur et al.: AI-led teams found fewer major errors and proposed fewer robustness checks; Cunningham interview: agent-missed data issues. |
| "Pin everything (uv lockfile), log every action (git), verify with assertions" | VERIFIED (practice) | Matches [Vilhuber — Self-checking reproducibility](https://larsvilhuber.github.io/self-checking-reproducibility/) and AEA Data Editor guidance ([aeaweb.org/journals/data](https://www.aeaweb.org/journals/data)). |
| Public replication packages exist for paper selection | VERIFIED | AEA journals require packages (openICPSR); [I4R](https://i4replication.org/) publishes reproduction reports — a ready list of papers whose packages are known to (not) run. |

## 2. Best deeper-dive resources

1. Brodeur et al. 2025, [free PDF](https://docs.iza.org/dp17645.pdf) — the one randomized study; the "AI-led loses by 57 pp" number is the module's motivation slide.
2. Kohler et al. 2026, [arXiv 2604.21965](https://arxiv.org/abs/2604.21965) — what a reproduction *agent* looks like and where it fails; read §on root causes.
3. [Vilhuber — Self-checking reproducibility](https://larsvilhuber.github.io/self-checking-reproducibility/) — the checklist students should turn into assertions.
4. [I4R — Institute for Replication](https://i4replication.org/) — pick papers here; reports show what the human reproducers found, i.e. the answer key.
5. *Ambitious:* Cunningham's [MixtapeTools](https://github.com/scunning1975/mixtapetools) (free) + the AI Economist [interview](https://www.aieconomist.io/articles/scott-cunningham-claude-code-ai-economists); if they subscribe, CC15/CC24 on the Substack.

## 3. Pedagogical risks

- **Stata**: most econ packages are Stata; students have no licence. Mitigation: selection criterion "package runs in Python or R, or the agent is asked to *translate* and that translation is the memo's subject".
- **Data access**: many packages have restricted data. Mitigation: I4R / openICPSR "public data" filter as a hard criterion.
- **Compute**: 80B coder + big datasets on laptops. Mitigation: "main table reproducible on a laptop in < 10 min" criterion (already in Task 03 brief).
- **Grading honesty vs incentive**: students will claim success. Mitigation: require the assertion file and the git log in the memo; grade the failure analysis (spec already says so).
- **Paywalled canon**: the Cunningham posts can't be assigned. Mitigation: cite the free interview + hooks post; summarize the numbers on the site with attribution.

## 4. Suggested spec edits

- Mini-module motivation: « Walk through the Scott Cunningham-style workflow » → « Motivate with Brodeur et al. (2025/PNAS 2026): AI-led reproduction teams succeed 57 pp less often than humans; then the Cunningham-style workflow (agent + audit + git) as the response ».
- Add « Evidence base is early and mostly social-science-wide (Kohler et al. 2026; Xu & Yang 2026); the module's claim is methodological, not "agents replicate economics" ».
- Research-track project: add selection criteria « public data, non-Stata (or translation is the deliverable), < 10 min on a laptop, ideally a paper with an I4R report to compare against ».
- Method requirements: add « the memo must include the assertions file and `git log --oneline` of the agent's actions ».
