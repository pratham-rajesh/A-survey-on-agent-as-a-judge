# Supporting papers

Each entry was checked against its arXiv abstract page (title, authors, date) before use. Numbers marked "(read in full text)" come from the paper body, the rest from the abstract.

## 1. Agent-as-a-Judge: Evaluate Agents with Agents (Zhuge et al., 2024)
arXiv:2410.10934 · submitted 14 Oct 2024 · 13 authors incl. Jürgen Schmidhuber

- The origin of the term. Judging agentic systems by only their final outcome ignores the step-by-step process, and human evaluation is too labour-intensive. The fix: use an agentic system as the judge, as an extension of LLM-as-a-Judge with intermediate feedback over the whole task-solving process.
- Introduces DevAI, a benchmark of 55 automated AI-development tasks with 365 hierarchical user requirements. Applied to three code agents (MetaGPT, GPT-Pilot, OpenHands).
- Alignment with the human-consensus verdicts across the 365 requirements (read in full text, Table 3): for OpenHands, Agent-as-a-Judge 92.07% (gray-box) and 90.44% (black-box) vs. LLM-as-a-Judge 70.76% and 60.38%. Human majority vote reaches 94.26%.
- Component ablation (Table 4, judging OpenHands): ask 65.03% -> + graph 75.95% -> + read 82.24% -> + locate 90.44% -> + retrieve 90.16%. Locating the right files gives the biggest late jump; retrieve adds nothing there.
- Cost (Sec. 4.4): human evaluators took 86.5 hours (about 1,297.50 USD at an assumed 15 USD/h). Agent-as-a-Judge cost 30.58 USD and 118.43 minutes; LLM-as-a-Judge cost 29.63 USD and 10.99 minutes. So in this setup the agentic judge was about 10x slower than the plain LLM judge but not much more expensive in dollars. Useful reality check for the cost discussion.

## 2. A Survey on LLM-as-a-Judge (Gu et al., 2024; revised 2025)
arXiv:2411.15594 · 16 authors, first author Jiawei Gu

- Frames the field around one question: how can reliable LLM-as-a-Judge systems be built? Covers strategies for consistency, bias mitigation and adapting to different assessment scenarios, plus a way to measure judge reliability with a new benchmark.
- Its bias catalogue (read in full text) names position bias, length bias, concreteness bias and self-enhancement bias among others, and describes swap-and-compare as a mitigation for position bias. Good source for the "known failure modes" paragraph.
- Adds the reliability-first viewpoint that the agentic survey takes for granted: before adding tools, ask whether the plain judge is consistent.

## 3. From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge (Li et al., 2024; revised 2025)
arXiv:2411.16594 · 13 authors, first author Dawei Li

- Defines LLM-as-a-judge from input and output perspectives (scoring, ranking, selection) and organizes the field along three questions: what to judge, how to judge, how to benchmark.
- That three-question lens contrasts nicely with the agentic survey, which organizes by the evaluator's own checking process rather than by task.
- Supplies the "why LLM judges took off" background: flexible on open-ended tasks where matching-based metrics fail.

## 4. Reliability without Validity (Norman, Rivera, Hughes, 2026)
arXiv:2606.19544 · submitted 17 Jun 2026

- Large-scale audit: 21 judges from nine providers on MT-Bench, JudgeBench and RewardBench, 118 runs, about 541,000 judgments.
- Four findings: (a) exact-match agreement overstates ability; the gap to Cohen's kappa is 33-41 percentage points on MT-Bench; (b) judge rankings shift by up to 14 positions across benchmarks; (c) a "consistency-bias paradox": test-retest reliability above 0.95 can coexist with position bias above 0.10 for two production judges; (d) verbosity bias is small (below 0.011) under their single pairwise rubric.
- Why it matters here: the agentic survey's evidence is the same three benchmarks. If rankings move this much between benchmarks, a few points of difference in Table 3 is a weak signal. Strong counterpoint for the "two cents" section.

## 5. Challenges and Recommendations for LLM-as-a-Judge in Multilingual Settings and for Low-Resource Languages (Doğruöz et al., 2026)
arXiv:2607.02235 · submitted 2 Jul 2026

- Looks at ACL Anthology papers: only 33 of 650 papers mentioning LLM-as-a-judge focus on multilingual or low-resource settings.
- Finds inconsistent outcomes, a tendency to over-trust the judge, and widespread reliance on a single judge model per study. Ends with a checklist of recommendations.
- Fits the agentic story: UrduFactCheck (cited in the survey) is an example of an agentic judge built for a low-resource language. The paper also shows that "no human validation" is the default, which is the same concern as evaluating the evaluator.

## How these fit together

- Zhuge et al. = the original agentic idea, with the only cost and ablation numbers I could verify.
- Gu et al. and Li et al. = the LLM-as-a-Judge baseline the agentic survey builds on.
- Norman et al. and Doğruöz et al. = 2026 caution about how we validate judges at all.
