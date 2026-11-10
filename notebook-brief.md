# Notebook source brief — AI × Labor Markets

Upload this file plus the eight PDFs below into Gemini Notebook (notebook.google.com), then run the prompts at the end. The book of record for every claim is the paper, not this brief.

## Sources to upload (all open access via DOI)
1. Acemoglu & Restrepo (2019), *Automation and New Tasks* — JEP — doi.org/10.1257/jep.33.2.3
2. Eloundou, Manning, Mishkin & Rock (2023), *GPTs are GPTs* — arXiv — doi.org/10.48550/arxiv.2303.10130
3. Acemoglu, Autor, Hazell & Restrepo (2022), *AI and Jobs: Evidence from Online Vacancies* — JOLE — doi.org/10.1086/718327
4. Acemoglu (2024), *The simple macroeconomics of AI* — Economic Policy — doi.org/10.1093/epolic/eiae042
5. Cazzaniga, Jaumotte, Li et al. (2024), *Gen-AI* — IMF SDN — doi.org/10.5089/9798400262548.006
6. Tolan, Pesole, Martínez-Plumed et al. (2021), *Measuring the Occupational Impact of AI* — JAIR — doi.org/10.1613/jair.1.12647
7. Eisfeldt, Schubert & Zhang (2023), *Generative AI and Firm Values* — NBER w31222 — doi.org/10.3386/w31222
8. Zarifhonarvar (2023), *Economics of ChatGPT* — JEBDE — doi.org/10.1108/jebde-10-2023-0021

Also upload the numbers: `data/labor-model.csv` (BLS monthly series, Sep 2016–Sep 2026).

## The six tensions to interrogate
1. **Exposure is not displacement.** Every index here scores whether a model *could* do a task. None shows an employer cancelling a role. Where is the adoption channel?
2. **Pre-2023 and post-2023 are different literatures.** Task-based automation research vs LLM exposure indices — different questions, different data. Are any of the eight papers using the other's evidence as if it were their own?
3. **Macro and micro claims can both be true.** A modest aggregate productivity effect and large reallocation are compatible. Which papers conflate them?
4. **The data cannot separate AI from interest rates.** Information-sector employment is −4.2% year-over-year while health care is +1.9%. What design would distinguish AI exposure from cost-of-capital and pandemic over-hiring?
5. **Who loses is an entry-level question.** Occupation aggregates cannot see seniority. What would hiring-composition data show that headcount does not?
6. **What would falsify the thesis?** State the observation that would make you abandon it before you look for supporting evidence.

## Prompts to run inside the notebook
- "Across these sources, list every distinct measure of AI exposure, with its unit of analysis (occupation, task, firm, country). Flag any paper that mixes units."
- "For each paper, extract: identification strategy, data source, time period, unit of analysis, main finding stated in the paper's own words. Output as a table."
- "Which claims in these papers depend on adoption assumptions that the data cannot test? Quote the sentence where each assumption enters."
- "Build the strongest counterargument to 'AI exposure will reduce employment in exposed occupations', citing only these sources."
- "Cross-reference the BLS series against the exposure literature: which measurable labor-market outcome would move first, and by how much, if the displacement thesis were correct?"

## What not to do
Do not let the notebook summarize these papers into a consensus. There isn't one. The deliverable is a table of disagreements, not an average.
