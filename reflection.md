# Reflection: Large Language Model Limitations & Ethics in Domain-Specific Tasks

Deploying Large Language Models (LLMs) in high-stakes, domain-specific fields like personal finance and tax advisory introduces unique technical limitations and critical ethical liabilities. While LLMs excel at translating dense regulatory text into readable, conversational summaries, their architectural design compromises their reliability in rules-based environments.

## Technical Limitations
1. **Hallucinations & Mathematical Precision**: LLMs are probabilistic text-predictors, not computational engines. When calculating tax liabilities or capital gains, they frequently hallucinate non-existent sections of tax codes or commit simple arithmetic errors.
2. **Outdated Slabs**: Tax codes are dynamic, updating annually with Union Budgets. LLMs suffer from static training cutoffs and cannot natively account for live policy changes (e.g., standard deduction changes in FY 2024-25) without external integration.
3. **Lack of Edge-Case Nuance**: A standard LLM cannot fully map specialized legal provisions (like business deduction overrides or foreign tax credits) to a user's unique context, leading to generalized, potentially inaccurate advice.

## Ethical Implications & Risks
1. **Liability of Unauthorized Advice**: Providing tax advice borders on regulated professional consulting. Users acting on incorrect computations could face financial penalties, tax audits, or interest charges, raising the question of developer and platform accountability.
2. **User Data Privacy**: Finance queries are highly sensitive. Users often input real salary parameters, PAN details, or asset values. Passing this data to proprietary LLM endpoints without strict encryption and zero-data retention policies violates basic data privacy ethics.

## Mitigation Strategies
To deploy safely, systems must implement clear, non-intrusive legal disclaimers. Furthermore, standard prompts must be combined with a **Retrieval-Augmented Generation (RAG)** pipeline to query live, verified tax database documents. Finally, embedding programmatic calculator widgets alongside the chat interface ensures calculations are performed by deterministic code, not probabilistic model guesses.
