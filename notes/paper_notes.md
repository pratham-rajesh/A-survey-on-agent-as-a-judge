# Notes: "A Survey on Agent-as-a-Judge"

Source: You, Cai, Zhang, Xu, Liu, Yu, Li, Li (2026), arXiv:2611.18067v1, submitted 13 Nov 2026, CC BY 4.0.
Read from the arXiv HTML and the PDF (the HTML build stops at Table 5, so Sections 6-7 and the appendix come from the PDF).
Section and table numbers below follow the PDF.

## One-paragraph summary (own words)

A plain LLM judge sees a fixed packet (the thing being judged plus some instructions or references) and answers from that alone. That breaks down when the answer depends on something that is not in the packet: what actually happened in a workspace after an agent ran, whether a code patch really passes, or whether a medical claim matches current guidance. The survey calls evaluators that go and get that missing evidence "Agent-as-a-Judge". It gives an operational definition (at least one real checking step, and the findings must feed the verdict), then sorts the design space into four mechanisms: multi-agent collaboration, tool integration, memory and planning. It collects published reward-model scores, fills in missing cells by running released code, and finds that agentic judges do not win across the board. It closes with application needs and open problems around cost, reliability, safety and governance.

## Definition and scope (Sec. 2)

- LLM-as-a-Judge (fixed context): verdict = J(evaluand x, supplied context C).
- Agent-as-a-Judge: a loop. State s_t, action a_t chosen by a policy, observation o_t returned by the world, state update, and a final verdict g(s_T).
- Qualifies if at least one step obtains evidence, runs a targeted verification, or reassesses a judgment using another check's findings, and those findings are used.
- Control can be: prescribed (fixed workflow), planned from the input before execution, or revised from observations during execution.
- Does NOT qualify alone (Appendix A, Table 6): one-shot or CoT scoring; independent scores then averaged or voted; different personas scoring the same object independently; a plan that no check ever uses.
- Two motivating failures: (1) decisive evidence about external state is missing from the text (agent trajectories, code that must be run, GUI effects); (2) needed facts are outside the judge's own knowledge (drug dosages, updated guidelines, primary literature).

## Taxonomy (Sec. 3, Fig. 2 in the paper)

- **Multi-agent collaboration** (3.1)
  - Roles (24 papers, 102 role-level records coded in Appendix B):
    - Adversarial: raise objections or cross-examine (AgentsCourt: plaintiff and defendant).
    - Perspective: same case, different identity or expertise (AgentsBench: professional and lay judges).
    - Analytical: turn the evaluand into inspectable evidence (GEMA-Score extracts clinical entities; MATH-VF formalizes reasoning for critics and tools).
    - Verdict-control: aggregate, stop, reroute or authorize (MATEval; CollabEval consensus and unchanged-result checks).
  - Implementation classes: persona prompts, structured workflows, deterministic controllers, tool-integrated components.
  - Collaboration modes:
    - Sequential: later stages consume upstream artifacts (AgentsCourt, CodeVisionary). Benefit: traceability. Risk: upstream lock-in.
    - Reciprocal: agents read each other's rationale and revise (AgentsBench, CollabEval, HiMATE, critic-defender safety evaluation). Risk: agreement that suppresses useful minority evidence.
    - Parallel: independent assessments combined by a resolver (AgentV-RL forward/backward verifiers, Multi-Agent Verification aspect approvals, Meta-Judges, DARE, No-human-in-the-loop majority vote plus severity hierarchy).
- **Tool integration** (3.2)
  - Interfaces (manual coding of 34 tool-augmented judges, 60 interface uses): code execution 17, web search 13, local search 8, vision model 7, solver 5, image ops 3, shell 3, computer use 2, translation 2.
  - Selection (increasingly adaptive): fixed-rule (VerifiAgent, Auto-Eval Judge) -> evidence-triggered (OpenReward, TALE, UrduFactCheck) -> observation-guided (GUI-PRA, CodeVisionary, VeriCUA) -> active probing (VAGEN, agentic-verifier, InteractionJudge).
  - Functions: knowledge expansion (OpenReward, TALE, DREAM), evidence access and transformation (Auto-Eval Judge, TaTToo, ARM-Thinker), operational verification (TIR-Judge, VerifiAgent, MATH-VF, AgentV-RL), trace-based judgment (TIM-PRM, GUI-PRA, VAGEN, CodeVisionary).
- **Memory** (3.3), a write-manage-read loop
  - What is stored: process memory (within-run buffer; TALE, GUI-PRA), artifact memory (crops, pages, reports; ARM-Thinker, CodeVisionary), experience memory (failure pools, template trees; FACT-AUDIT, Table-Critic).
  - How it is read: direct carry-forward, condensed readout, selective retrieval.
  - What triggers updates: per step, budget (too long or noisy), outcome (a failure or success worth keeping).
  - Observation: most agentic judges keep only a short within-run buffer; few curate reusable experience across cases. The original Agent-as-a-Judge paper's own memory module is called a cautionary example (ablation shows limited benefit and possible error propagation).
- **Planning** (3.4, Table 1)
  - What to check: case-specific protocols (DREAM), rubric planning (APRES), sub-aspect planning (Evaluation Agent).
  - How to check: route planning (EvalPlanner), claim-level planning (AgentV-RL), step-level routing (TIM-PRM, VerifiAgent), evidence-channel dispatch (CodeVisionary, Auto-Eval Judge).
- **Synthesis** (3.5)
  - Timeline: debate and tool use are early; planning is shifting toward case-specific, atomic rubrics; memory is the thinnest.
  - Findings become verdicts through formulaic aggregation, deliberative resolution, or severity / source-grounded rules.
  - Findings also decide whether to keep checking: consensus, unchanged-result and stability checks, retrieval escalation. The paper warns that agreement or stability is not the same as calibrated confidence.

## Evaluation (Sec. 4)

Evidence mostly comes from shared judge-quality benchmarks, not from benchmarks built to test evidence-seeking.

### Table 2: reward-model and verifier benchmarks

| Benchmark | Form | Evaluand | Domain | Signal | Scale |
|---|---|---|---|---|---|
| RewardBench | pair-wise | response pair | chat, safety, reasoning, code/math | chosen-rejected preference | 2,985 |
| RM-Bench | pair-wise | response pair | chat, code, math, safety | subtle correctness under style variation | 1,237 |
| JudgeBench | pair-wise | response pair | knowledge, reasoning, math, code | objective correctness label | 620 |
| IFBench | pair-wise | response pair | instruction following | constraint satisfaction | 444 |
| VerifyBench | point-wise | completion | reference-based answer verification | binary correctness against reference | 3,000 |
| ProcessBench | step-wise | reasoning trace | mathematical reasoning | earliest-error step label | 3,400 |

### Table 3: local reward-model results (percent)

Marker meaning, as stated by the paper: † = extracted from the original papers' comparison tables; ∗ = Agentic Reward Model uses ArmoRM-Llama3-8B as its base reward model, with Llama3-8B Instruct and Qwen2.5-Coder-7B inside its verification modules. The paper says it keeps published scores where they exist and reproduces missing benchmark entries from public code, but it does not flag which individual cells were reproduced. Rows without † are therefore either published elsewhere or reproduced by the authors; I treat them as "not extracted from the original comparison tables". RewardBench and RM-Bench were converted to percentages.

Agentic judges: TIR-Judge, Agentic Reward Model, Multi-Agent Verification, VerifiAgent, Themis. Non-agentic reasoning reward models used as baselines: RRM, RM-R1, Think-RM.

**RewardBench**

| Method | Model | Chat | Chat-Hard | Safety | Reason | Overall |
|---|---|---|---|---|---|---|
| TIR-Judge † | TIR-Judge-8B | 94.7 | 77.4 | 88.8 | 95.7 | 89.1 |
| Agentic Reward Model | ArmoRM-Llama3-8B ∗ | 90.8 | 70.0 | 86.5 | 93.2 | 87.6 |
| Multi-Agent Verification | Qwen3-8B | 78.5 | 80.2 | 86.1 | 86.7 | 82.9 |
| VerifiAgent | Qwen3-8B | 69.8 | 65.8 | 78.6 | 61.3 | 68.9 |
| Themis | Themis-7B | 82.7 | 42.3 | 45.7 | 37.1 | 52.0 |
| RRM † | RRM-7B | 87.7 | 70.4 | 80.7 | 90.0 | 82.2 |
| RM-R1 † | RM-R1-Distill-7B | 88.9 | 66.2 | 78.4 | 87.0 | 80.1 |
| Think-RM † | Think-RM-7B | 94.4 | 77.9 | 85.2 | 86.4 | 86.0 |

**RM-Bench**

| Method | Model | Chat | Math | Code | Safety | Overall |
|---|---|---|---|---|---|---|
| TIR-Judge † | TIR-Judge-8B | 80.1 | 91.9 | 69.0 | 93.9 | 83.7 |
| Agentic Reward Model | ArmoRM-Llama3-8B ∗ | 60.0 | 58.3 | 54.5 | 86.8 | 64.9 |
| Multi-Agent Verification | Qwen3-8B | 62.6 | 67.8 | 52.4 | 84.9 | 66.9 |
| VerifiAgent | Qwen3-8B | 41.3 | 80.0 | 45.9 | 74.5 | 60.4 |
| Themis | Themis-7B | 48.4 | 49.9 | 53.9 | 48.4 | 50.2 |
| RRM † | RRM-7B | 58.4 | 81.8 | 56.7 | 84.9 | 70.4 |
| RM-R1 † | RM-R1-Distill-7B | 64.0 | 83.9 | 56.2 | 85.3 | 72.4 |
| Think-RM † | Think-RM-7B | 69.3 | 76.0 | 56.5 | 93.7 | 73.9 |

**JudgeBench**

| Method | Model | Math | Code | Knowledge | Reason | Overall |
|---|---|---|---|---|---|---|
| TIR-Judge † | TIR-Judge-8B | 71.8 | 70.7 | 60.8 | 71.7 | 66.7 |
| Agentic Reward Model | ArmoRM-Llama3-8B ∗ | 63.4 | 49.2 | 47.0 | 56.7 | 51.9 |
| Multi-Agent Verification | Qwen3-8B | 54.3 | 42.5 | 45.7 | 39.0 | 44.8 |
| VerifiAgent | Qwen3-8B | 50.0 | 39.6 | 41.6 | 53.9 | 45.5 |
| Themis | Themis-7B | 42.9 | 48.0 | 54.8 | 51.6 | 51.1 |
| RRM † | RRM-7B | 83.2 | 61.9 | 64.3 | 64.2 | 67.0 |
| RM-R1 † | RM-R1-Distill-7B | 82.1 | 71.4 | 64.9 | 62.2 | 67.7 |
| Think-RM † | Think-RM-7B | 67.9 | 42.9 | 67.5 | 67.3 | 64.6 |

(The "Overall" column is not a plain mean of the four listed subsets; for example TIR-Judge on JudgeBench averages 68.75 over its four subsets but is listed as 66.7. The paper does not say how Overall is weighted, so I transcribe it as printed and do not recompute it.)

What the paper concludes: no uniform agentic advantage. On RM-Bench only TIR-Judge clearly beats the non-agentic reasoning reward models. On JudgeBench strong non-agentic models match or slightly exceed the best agentic entry, and most agentic judges are weaker, especially outside their strongest categories. The authors read this as consistent with preference- and reasoning-oriented reward training working well on fixed response pairs, and say these comparisons only partly capture active evidence-seeking.

Numbers derived for the article (my arithmetic from the table above):
- Best agentic minus best non-agentic overall: RewardBench 89.1 - 86.0 = +3.1; RM-Bench 83.7 - 73.9 = +9.8; JudgeBench 66.7 - 67.7 = -1.0.

### Table 4: NLG evaluation benchmarks

| Benchmark | Form | Evaluand | Domain | Human signal | Scale |
|---|---|---|---|---|---|
| SummEval | point-wise | summary | summarization | quality rating | 1,600 |
| TopicalChat-USR | point-wise | response | dialogue | quality rating | 360 |
| QAGS | point-wise | summary | summarization | factuality label | 474 |
| ROCStories | point-wise | story | story generation | error score | 200 |
| WritingPrompts | point-wise | story | story generation | error score | 200 |
| StorySparkQA | point-wise | QA pair | story QA | expert rating | 70 |
| MSLR-COCHRANE | point-wise | summary | biomedical summarization | facet rating | 102 |

The paper reports no comparable leaderboard for NLG: reporting there is "dataset- and lineage-local". Representative systems: ChatEval (debate), MAJ-EVAL, CollabEval; factuality: MADISSE, NarrativeFactScore; translation: HiMATE, M-MAD.

### Other evaluation points

- Reward models are validated in three ways: test-time selection (Best-of-N on MATH, AIME), downstream training (PPO, DPO data, robot action chunks), and fixed-artifact benchmarks.
- High scores on the fixed suites may not predict test-time or downstream gains.
- The suites do not isolate the contribution of planning, tools, evidence acquisition, aggregation or stopping.
- Environment-aware benchmarks (e.g. Agent-as-a-Judge benchmark, VeriCUA) should report evidence-access conditions and decision coverage when abstention is allowed.

## Applications (Sec. 5, Table 5)

| Domain | Judgment target | Gap in fixed-context judging | Agentic capability |
|---|---|---|---|
| Math and code | reasoning steps, executable outputs | correctness may need execution, equivalence checks or hidden step errors | execution, solver checks, multi-verifier agreement |
| Fact-checking | claims, verdicts, justifications | a label is weak without retrieved support | retrieval, evidence grounding, justification checks |
| Conversation | multi-turn behavior | quality depends on goals and state across turns | user simulation, memory, multi-perspective review |
| Multimodal and vision | images and multimodal outputs | evidence sits in regions, pages, cross-modal details | visual inspection, targeted questioning, multimodal tools |
| Medicine | clinical reports and dialogue | safety-sensitive, needs expertise and uncertainty handling | role-specialized evaluation, tool-assisted scoring, simulation |
| Law | legal arguments and verdicts | plausible verdicts may miss opposing arguments | adversarial debate, deliberation, consensus control |
| Finance | reports, agents, risk trajectories | must track report logic, time, trajectory failures | planning, logic extraction, trajectory audit |
| Education | answers, rubrics, rationales | scores need consistent rubrics and inspectable evidence | rubric planning, evidence recognition, cross-review |

## Ablations and analyses reported in the survey

- No component ablation of its own. The survey's analysis is the cross-system comparison (Table 3), the manual codings (roles, tool interfaces) and the timeline.
- Cited from the original Agent-as-a-Judge work: memory module shows limited benefit and possible error propagation (see supporting_papers.md for the original paper's own ablation numbers, which I read directly).

## Open challenges and future directions (Sec. 6)

Challenges:
- Efficiency: extra actions add cost and latency; costs compound when later checks depend on earlier observations; latency limits online use and RL feedback loops.
- Process reliability: wrong target claim, weak retrieval, misread tool output, consensus on a wrong answer, memory preserving mistakes. A verdict can look well supported while its evidence trace is flawed.
- Safety and control: prompt injection, tool misuse, side effects, unsafe rationales propagating between agents, and reward hacking when verdicts become RL rewards. Needs bounded permissions, stopping rules and escalation paths.
- Privacy and governance: persistent evaluation state can hold user information; needs rules on what is stored, retention, access, deletion and reuse.

Future directions: adaptive control (spend effort according to the case), memory management as part of the judging policy, autonomous probing (generate tests, counterexamples, stress cases), and trainable judgment policies (RL and process supervision for decomposition, tool choice, sufficiency and stopping). Progress should be measured by whether the judge seeks appropriate evidence, keeps useful state, and stops or escalates at the right point.
