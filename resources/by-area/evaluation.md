# Evaluation & Leakage Control

> **Validation tier** — Whether the prediction can be believed, and how far.

A favourable split or repeated test-set access can beat a better architecture.

The test split decides which question an accuracy answers, and a model can
reach a high score by reading a spectral confound rather than the variable
of interest. Reporting the split, the held-out unit, and the controls
against leakage is the minimum for a number to mean anything.

**9 references** are listed here; 4 of them are filed primarily under this area.

## What to look for

- Split protocols and split unit
- Leakage from windows and sessions
- Aperiodic and spectral confounds
- Perturbation-based explanation checks

## References

| Paper | Year | Venue | Note | Links |
| --- | ---: | --- | --- | --- |
| [Evaluation in EEG Emotion Recognition: State-of-the-Art Review and Unified Framework](https://doi.org/10.48550/arXiv.2505.18175) | 2025 |  | A survey of 216 papers on how the split was chosen. | [DOI](https://doi.org/10.48550/arXiv.2505.18175) [arXiv](https://arxiv.org/abs/2505.18175) [code](https://github.com/EmotionLab/EEGain) |
| [Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead](https://doi.org/10.1038/s42256-019-0048-x) | 2019 | Nature Machine Intelligence | The case for perturbing inputs instead of reading saliency maps. | [DOI](https://doi.org/10.1038/s42256-019-0048-x) |
| [A novel Fourier Adjacency Transformer for advanced EEG emotion recognition](https://doi.org/10.1007/978-3-032-05162-2_2) | 2025 | Medical Image Computing and Computer Assisted Intervention - MICCAI 2025 | Builds the periodic and aperiodic distinction into the architecture. | [DOI](https://doi.org/10.1007/978-3-032-05162-2_2) |
| [Hierarchical Dynamic Graph Convolutional Network With Interpretability for EEG-Based Emotion Recognition](https://doi.org/10.1109/TNNLS.2022.3225855) | 2025 | IEEE Transactions on Neural Networks and Learning Systems | HD-GCN: DREAMER, High/low valence and arousal classification | [DOI](https://doi.org/10.1109/TNNLS.2022.3225855) |
| [A spectral audit framework reveals task-dependent aperiodic reliance across EEG and ECG deep learning](https://doi.org/10.48550/arXiv.2606.08583) | 2026 |  | Six of seven foundation models depend on the aperiodic background component. | [DOI](https://doi.org/10.48550/arXiv.2606.08583) [arXiv](https://arxiv.org/abs/2606.08583) |
| [Cross-Subject Generalization in EEG Emotion Recognition](https://doi.org/10.48550/arXiv.2607.27655) | 2026 |  | A controlled audit showing how much a favourable split can inflate accuracy. | [DOI](https://doi.org/10.48550/arXiv.2607.27655) [arXiv](https://arxiv.org/abs/2607.27655) |
| [See the Emotion: A Facial Emoji Proxy Modeling for EEG Emotion Recognition](https://doi.org/10.48550/arXiv.2607.02912) | 2026 | Proceedings of the 43rd International Conference on Machine Learning (ICML) | Facial expression used as a proxy label for EEG emotion. | [DOI](https://doi.org/10.48550/arXiv.2607.02912) [arXiv](https://arxiv.org/abs/2607.02912) [code](https://github.com/xian-sh/SeeEmotion) |
| [Interpretable Dual-Filter Fuzzy Neural Networks for Affective Brain-Computer Interfaces](https://doi.org/10.48550/arXiv.2502.17445) | 2025 |  | A fuzzy model whose filters are readable by a person. | [DOI](https://doi.org/10.48550/arXiv.2502.17445) [arXiv](https://arxiv.org/abs/2502.17445) |
| [Decoding naturalistic affective behaviour from spectro-spatial features in multiday human iEEG](https://doi.org/10.1038/s41562-022-01310-0) | 2022 | Nature Human Behaviour | 116 hours over 11 participants, and a gap between per-person and group accuracy. | [DOI](https://doi.org/10.1038/s41562-022-01310-0) |

## Elsewhere in the Validation tier

**[Evidence Maturity](maturity.md)** — Lab estimates the state; Pilot changes something; Field holds up over time.

All nine areas: [research-area index](README.md) · back to the [resource index](../README.md).
