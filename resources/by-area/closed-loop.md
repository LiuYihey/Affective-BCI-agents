# Closed-Loop Systems

> **Systems tier** — What the prediction is used for, once it exists.

Sense proposes, Act decides, a harness keeps the system inside what was tested.

Sense turns the signal into a belief, Think proposes an action, Act decides what may reach the user. A harness keeps an adaptive system inside the range in which it was tested. Most published systems stop after Sense and report an accuracy; the loop is where the hard problems live.

**19 references** are listed here; 11 of them are filed primarily under this area.

## What to look for

- Sense, Think and Act
- Action gating and fallbacks
- Agent harness and retained state
- Real-time operation and latency

## References

| Paper | Year | Venue | Note | Links |
| --- | ---: | --- | --- | --- |
| [Building Better Biomarkers: Brain Models in Translational Neuroimaging](https://doi.org/10.1038/nn.4478) | 2017 | Nature Neuroscience | Defines a biomarker backwards from its intended use, the basis of the governance rules. | [DOI](https://doi.org/10.1038/nn.4478) |
| [BrainBench: Benchmarking Large Language Models for Comprehensive EEG Understanding](https://doi.org/10.48550/arXiv.2608.04156) | 2026 |  | Instruction-conditioned benchmarks for language models that analyse EEG. | [DOI](https://doi.org/10.48550/arXiv.2608.04156) [arXiv](https://arxiv.org/abs/2608.04156) |
| [Towards Subject Agnostic Affective Emotion Recognition](https://ceur-ws.org/Vol-3566/paper4.pdf) | 2023 | Proceedings of the 2nd International Workshop on Multimodal Human Understanding for the Web and Social Media (MUWS 2023), co-located with the 32nd ACM International Conference on Information and Knowledge Management | Subject-agnostic representations across several affect corpora. | [link](https://ceur-ws.org/Vol-3566/paper4.pdf) |
| [A Minimalist Brain-Computer Musical Interface for Real-Time Emotion-Driven Sonification: System Design and Preliminary Evaluation](https://doi.org/10.48550/arXiv.2606.01473) | 2026 |  | A musical BCI where the control signal showed no effect on the target emotion. | [DOI](https://doi.org/10.48550/arXiv.2606.01473) [arXiv](https://arxiv.org/abs/2606.01473) |
| [MindMelody: A Closed-Loop EEG-Driven System for Personalized Music Intervention](https://doi.org/10.48550/arXiv.2605.01235) | 2026 |  | EEG-driven music generation, and a report without significance tests. | [DOI](https://doi.org/10.48550/arXiv.2605.01235) [arXiv](https://arxiv.org/abs/2605.01235) |
| [MindPilot: Closed-loop Visual Stimulation Optimization for Brain Modulation with EEG-guided Diffusion](https://doi.org/10.48550/arXiv.2602.10552) | 2026 |  | EEG-guided image generation, with a second experiment that removes the neural input. | [DOI](https://doi.org/10.48550/arXiv.2602.10552) [arXiv](https://arxiv.org/abs/2602.10552) |
| [A pilot study of closed-loop neuromodulation for treatment-resistant post-traumatic stress disorder](https://doi.org/10.1038/s41467-023-38712-1) | 2023 | Nature Communications | Amygdala-triggered stimulation, with a control group still missing. | [DOI](https://doi.org/10.1038/s41467-023-38712-1) |
| [Closed-loop neuromodulation in an individual with treatment-resistant depression](https://doi.org/10.1038/s41591-021-01480-w) | 2021 | Nature Medicine | A personalised biomarker that did trigger stimulation, and reached remission. | [DOI](https://doi.org/10.1038/s41591-021-01480-w) |
| [A Survey on AI Agent Harness](https://doi.org/10.13140/RG.2.2.31393.57447) | 2026 |  | The agent harness literature the governance layer is built on. | [DOI](https://doi.org/10.13140/RG.2.2.31393.57447) [link](https://github.com/HKUST-KnowComp/Awesome-Agent-Harness) |
| [BrainAgent: A Large Language Model-Driven Multi-Agent Framework for Autonomous Brain Signal Understanding](https://doi.org/10.48550/arXiv.2606.25400) | 2026 |  | An LLM-driven multi-agent framework over EEG. | [DOI](https://doi.org/10.48550/arXiv.2606.25400) [arXiv](https://arxiv.org/abs/2606.25400) |
| [EEGDancer: Dynamic Emotion Latent Space Masked Modeling with Reinforcement Learning for EEG Continuous Emotion Prediction](https://doi.org/10.48550/arxiv.2606.05855) | 2026 | arXiv preprint arXiv:2606.05855 | Dynamic emotion latent space with masked modelling. | [DOI](https://doi.org/10.48550/arxiv.2606.05855) [arXiv](https://arxiv.org/abs/2606.05855) |
| [Energy Landscapes of Emotion: Quantifying Brain Network Stability During Happy and Sad Face Processing Using EEG-Based Hopfield Energy](https://doi.org/10.48550/arxiv.2603.27644) | 2026 | arXiv preprint arXiv:2603.27644 | Emotion as the stability of a network, rather than a label. | [DOI](https://doi.org/10.48550/arxiv.2603.27644) [arXiv](https://arxiv.org/abs/2603.27644) |
| [Intracranial Neural Biomarkers of Psychiatric Symptoms and Their Utility for Guiding Neuromodulation Therapy: A Systematic Review](https://doi.org/10.1016/j.biopsych.2025.10.005) | 2026 | Biological Psychiatry | Which intracranial biomarkers could actually guide stimulation. | [DOI](https://doi.org/10.1016/j.biopsych.2025.10.005) |
| [Affective Brain Computer InterfaceUsing closed-loop BCI to recognize emotions and solve emotion problems](https://doi.org/10.62051/39m2yk04) | 2025 | Transactions on Computer Science and Intelligent Systems Research | A closed-loop BCI that recognises affect and responds in kind. | [DOI](https://doi.org/10.62051/39m2yk04) |
| [An Adaptive Brain-Computer Interface Game with Blink Controls and Cognitive State Monitoring](https://doi.org/10.1145/3708557.3716365) | 2025 | Companion Proceedings of the 30th International Conference on Intelligent User Interfaces | An adaptive game where the interface follows the user's state. | [DOI](https://doi.org/10.1145/3708557.3716365) |
| [The NeuroBench Framework for Benchmarking Neuromorphic Computing Algorithms and Systems](https://doi.org/10.1038/s41467-025-56739-4) | 2025 | Nature Communications | A benchmark framework for neuromorphic computing. | [DOI](https://doi.org/10.1038/s41467-025-56739-4) [code](https://github.com/lava-nc/lava) |
| [A High-Performance Speech Neuroprosthesis](https://doi.org/10.1038/s41586-023-06377-x) | 2023 | Nature | 62 words per minute from a speech neuroprosthesis. | [DOI](https://doi.org/10.1038/s41586-023-06377-x) |
| [Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria](https://doi.org/10.1056/NEJMoa2027540) | 2021 | New England Journal of Medicine | Speech decoded in a person who cannot speak. | [DOI](https://doi.org/10.1056/NEJMoa2027540) |
| [Brain–machine interfaces from motor to mood](https://doi.org/10.1038/s41593-019-0488-y) | 2019 | Nature Neuroscience | From motor control to mood: what brain-machine interfaces could reach. | [DOI](https://doi.org/10.1038/s41593-019-0488-y) |

---

**Also in the Systems tier:** [Application Domains](applications.md).

All nine areas: [research-area index](README.md) · back to the [resource index](../README.md).
