# Is that accuracy real?

The test split decides which question an accuracy answers. A favourable split or repeated access to the test set can beat a better architecture.

**21 references** list here; 12 are filed primarily under this question.

## What to look for

- Split protocols
- Leakage
- Spectral confounds
- Model explanation checks

## References

| Paper | Year | Venue | Note | Links |
| --- | ---: | --- | --- | --- |
| [MAD: A Multimodal and Multi-perspective Affective Dataset with Hierarchical Annotations](https://doi.org/10.48550/arXiv.2603.06206) | 2026 |  | Records all three target sources separately, and defines the annotation levels used throughout. | [DOI](https://doi.org/10.48550/arXiv.2603.06206) [arXiv](https://arxiv.org/abs/2603.06206) |
| [Evaluation in EEG Emotion Recognition: State-of-the-Art Review and Unified Framework](https://doi.org/10.48550/arXiv.2505.18175) | 2025 |  | A survey of 216 papers on how the split was chosen. | [DOI](https://doi.org/10.48550/arXiv.2505.18175) [arXiv](https://arxiv.org/abs/2505.18175) [code](https://github.com/EmotionLab/EEGain) |
| [A novel Fourier Adjacency Transformer for advanced EEG emotion recognition](https://doi.org/10.1007/978-3-032-05162-2_2) | 2025 | Medical Image Computing and Computer Assisted Intervention - MICCAI 2025 | Builds the periodic and aperiodic distinction into the architecture. | [DOI](https://doi.org/10.1007/978-3-032-05162-2_2) |
| [Hierarchical Dynamic Graph Convolutional Network With Interpretability for EEG-Based Emotion Recognition](https://doi.org/10.1109/TNNLS.2022.3225855) | 2025 | IEEE Transactions on Neural Networks and Learning Systems | HD-GCN: DREAMER, High/low valence and arousal classification | [DOI](https://doi.org/10.1109/TNNLS.2022.3225855) |
| [A spectral audit framework reveals task-dependent aperiodic reliance across EEG and ECG deep learning](https://doi.org/10.48550/arXiv.2606.08583) | 2026 |  | Six of seven foundation models depend on the aperiodic background component. | [DOI](https://doi.org/10.48550/arXiv.2606.08583) [arXiv](https://arxiv.org/abs/2606.08583) |
| [Closed-Loop Brain-Computer Interfaces (BCI) Enhanced With AI-Driven Neurofeedback Using Soft Bioelectronic Networks: A Comparative Study With IBRAINTECH and Proposal of a New Hybrid Model](https://doi.org/10.5121/ijgca.2026.17101) | 2026 | International Journal of Grid Computing & Applications | Soft bioelectronic interfaces for closed-loop neurofeedback. | [DOI](https://doi.org/10.5121/ijgca.2026.17101) |
| [Cross-Subject Generalization in EEG Emotion Recognition](https://doi.org/10.48550/arXiv.2607.27655) | 2026 |  | A controlled audit showing how much a favourable split can inflate accuracy. | [DOI](https://doi.org/10.48550/arXiv.2607.27655) [arXiv](https://arxiv.org/abs/2607.27655) |
| [Cross-Subject Intracranial EEG Reconstruction from Scalp Recordings Using Multi-Scale Cross-Attention Transformers](https://doi.org/10.48550/arXiv.2605.18897) | 2026 |  | Reconstructing intracranial activity from scalp recordings. | [DOI](https://doi.org/10.48550/arXiv.2605.18897) [arXiv](https://arxiv.org/abs/2605.18897) |
| [Learning from Brain Topography: A Hierarchical Local-Global Graph-Transformer Network for EEG Emotion Recognition](https://doi.org/10.48550/arxiv.2601.10525) | 2026 | arXiv preprint arXiv:2601.10525 | Topography as the structure the model builds on. | [DOI](https://doi.org/10.48550/arxiv.2601.10525) [arXiv](https://arxiv.org/abs/2601.10525) |
| [SA-HGNN: Sample-Adaptive Hyperbolic Graph Neural Network for EEG-Based Depression Recognition](https://doi.org/10.48550/arXiv.2607.02063) | 2026 |  | Hyperbolic geometry for depression recognition. | [DOI](https://doi.org/10.48550/arXiv.2607.02063) [arXiv](https://arxiv.org/abs/2607.02063) |
| [See the Emotion: A Facial Emoji Proxy Modeling for EEG Emotion Recognition](https://doi.org/10.48550/arXiv.2607.02912) | 2026 | Proceedings of the 43rd International Conference on Machine Learning (ICML) | Facial expression used as a proxy label for EEG emotion. | [DOI](https://doi.org/10.48550/arXiv.2607.02912) [arXiv](https://arxiv.org/abs/2607.02912) [code](https://github.com/xian-sh/SeeEmotion) |
| [Interpretable Dual-Filter Fuzzy Neural Networks for Affective Brain-Computer Interfaces](https://doi.org/10.48550/arXiv.2502.17445) | 2025 |  | A fuzzy model whose filters are readable by a person. | [DOI](https://doi.org/10.48550/arXiv.2502.17445) [arXiv](https://arxiv.org/abs/2502.17445) |
| [Visual-to-EEG Cross-Modal Knowledge Distillation for Continuous Emotion Recognition](https://doi.org/10.1016/j.patcog.2022.108833) | 2022 | Pattern Recognition | Knowledge distilled from visual stimuli into EEG representations. | [DOI](https://doi.org/10.1016/j.patcog.2022.108833) |
| [Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead](https://doi.org/10.1038/s42256-019-0048-x) | 2019 | Nature Machine Intelligence | The case for perturbing inputs instead of reading saliency maps. | [DOI](https://doi.org/10.1038/s42256-019-0048-x) |
| [Building Better Biomarkers: Brain Models in Translational Neuroimaging](https://doi.org/10.1038/nn.4478) | 2017 | Nature Neuroscience | Defines a biomarker backwards from its intended use, the basis of the governance rules. | [DOI](https://doi.org/10.1038/nn.4478) |
| [Resting-state connectivity biomarkers define neurophysiological subtypes of depression](https://doi.org/10.1038/nm.4246) | 2017 | Nature Medicine | Resting-state subtypes of depression, and their response to treatment. | [DOI](https://doi.org/10.1038/nm.4246) |
| [Intracranial Neural Biomarkers of Psychiatric Symptoms and Their Utility for Guiding Neuromodulation Therapy: A Systematic Review](https://doi.org/10.1016/j.biopsych.2025.10.005) | 2026 | Biological Psychiatry | Which intracranial biomarkers could actually guide stimulation. | [DOI](https://doi.org/10.1016/j.biopsych.2025.10.005) |
| [Cingulate dynamics track depression recovery with deep brain stimulation](https://doi.org/10.1038/s41586-023-06541-3) | 2023 | Nature | A marker that follows recovery without ever triggering stimulation. | [DOI](https://doi.org/10.1038/s41586-023-06541-3) |
| [Decoding Depression Severity From Intracranial Neural Activity](https://doi.org/10.1016/j.biopsych.2023.01.020) | 2023 | Biological Psychiatry | Prefrontal intracranial coverage for depression severity. | [DOI](https://doi.org/10.1016/j.biopsych.2023.01.020) |
| [Neural modulation enhancement using connectivity-based EEG neurofeedback with simultaneous fMRI for emotion regulation](https://doi.org/10.1016/j.neuroimage.2023.120320) | 2023 | NeuroImage | Connectivity neurofeedback: Emotion regulation, EEG with concurrent fMRI | [DOI](https://doi.org/10.1016/j.neuroimage.2023.120320) |
| [Decoding naturalistic affective behaviour from spectro-spatial features in multiday human iEEG](https://doi.org/10.1038/s41562-022-01310-0) | 2022 | Nature Human Behaviour | 116 hours over 11 participants, and a gap between per-person and group accuracy. | [DOI](https://doi.org/10.1038/s41562-022-01310-0) |
