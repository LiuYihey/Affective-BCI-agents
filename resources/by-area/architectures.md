# Decoding Architectures

> **Methods tier** — How a recording becomes a prediction.

How a recording is organised, and which objective decides what the model keeps.

A multichannel recording can be arranged as a grid, a graph, or a sequence,
and the arrangement decides what the model is able to see. The training
objective is the more consequential choice: it determines whether the
representation is tied to a task, a subject, or a device.

**28 references** are listed here; 22 of them are filed primarily under this area.

## What to look for

- Architectures: CNN, GNN, Transformer, SSM
- Self-supervised pre-training
- Cross-dataset and cross-signal pre-training
- Device-agnostic representations

## References

| Paper | Year | Venue | Note | Links |
| --- | ---: | --- | --- | --- |
| [B[FM]$^2$: Brain Foundation Model via Flow Matching with SplitUNet](https://doi.org/10.48550/arXiv.2606.20812) | 2026 |  | A flow-matching formulation of the brain foundation model. | [DOI](https://doi.org/10.48550/arXiv.2606.20812) [arXiv](https://arxiv.org/abs/2606.20812) |
| [BrainBench: Benchmarking Large Language Models for Comprehensive EEG Understanding](https://doi.org/10.48550/arXiv.2608.04156) | 2026 |  | Instruction-conditioned benchmarks for language models that analyse EEG. | [DOI](https://doi.org/10.48550/arXiv.2608.04156) [arXiv](https://arxiv.org/abs/2608.04156) |
| [CoCoT-EEG: Contrastive-Pretrained Multiscale Convolutional Transformer for EEG Decoding](https://doi.org/10.48550/arXiv.2607.09543) | 2026 |  | Contrastive pre-training before the task-specific stage. | [DOI](https://doi.org/10.48550/arXiv.2607.09543) [arXiv](https://arxiv.org/abs/2607.09543) |
| [Implicit Behavioral Decoding from Next-Step Spike Forecasts at Population Scale](https://doi.org/10.48550/arXiv.2605.12999) | 2026 |  | Behaviour decoded implicitly, from the next step of the signal. | [DOI](https://doi.org/10.48550/arXiv.2605.12999) [arXiv](https://arxiv.org/abs/2605.12999) |
| [Learning aligned EEG representations with subject-specific encoders](https://doi.org/10.48550/arXiv.2606.16462) | 2026 |  | Shared representations with a subject-specific encoder on top. | [DOI](https://doi.org/10.48550/arXiv.2606.16462) [arXiv](https://arxiv.org/abs/2606.16462) |
| [Masked Generative-Contrastive Representation Learning for Cross-Dataset EEG-Based Emotion Recognition](https://doi.org/10.48550/arxiv.2607.04139) | 2026 | arXiv preprint arXiv:2607.04139 | Masked and generative objectives combined for cross-subject learning. | [DOI](https://doi.org/10.48550/arxiv.2607.04139) [arXiv](https://arxiv.org/abs/2607.04139) |
| [MSCGC-KAN: Multi-scale Causal Graph Convolution and Kolmogorov-Arnold Feature Mapping for EEG Emotion Recognition](https://doi.org/10.48550/arXiv.2605.26624) | 2026 |  | Causal graph convolution with a Kolmogorov-Arnold parameterisation. | [DOI](https://doi.org/10.48550/arXiv.2605.26624) [arXiv](https://arxiv.org/abs/2605.26624) |
| [NeuroShield: A Device-Agnostic Foundation Model for EEG Authentication](https://doi.org/10.48550/arXiv.2606.20673) | 2026 |  | Representations that identify the person who produced a recording. | [DOI](https://doi.org/10.48550/arXiv.2606.20673) [arXiv](https://arxiv.org/abs/2606.20673) |
| [One Model for All: Universal Pre-training for EEG based Emotion Recognition across Heterogeneous Datasets and Paradigms](https://arxiv.org/abs/2511.08444) | 2026 | IEEE Transactions on Affective Computing | A shared channel vocabulary, and a subject-specific encoder on top of it. | [arXiv](https://arxiv.org/abs/2511.08444) |
| [SPOTR: Spatio-temporal Pooling One-Token Reconstruction for Universal Physiological Signal Self-supervised Learning](https://arxiv.org/abs/2606.21973) | 2026 | Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI-ECAI) | One-token reconstruction as the pre-training objective. | [arXiv](https://arxiv.org/abs/2606.21973) [code](https://github.com/5GYYYYY/SPOTR) |
| [STST-JEPA: Shallow-Target Spatio-Temporal Joint Embedding Prediction Architecture For EEG Self-Supervised Learning](https://doi.org/10.48550/arXiv.2607.06629) | 2026 |  | Joint embedding prediction for spatio-temporal structure. | [DOI](https://doi.org/10.48550/arXiv.2607.06629) [arXiv](https://arxiv.org/abs/2607.06629) |
| [The RG-Flow Transformer: Encoding Scale-Free Dynamics in Scarce EEG](https://doi.org/10.48550/arXiv.2607.11950) | 2026 |  | Scale-free dynamics, for corpora where there are few subjects. | [DOI](https://doi.org/10.48550/arXiv.2607.11950) [arXiv](https://arxiv.org/abs/2607.11950) |
| [Transformer Based Model for Spatiotemporal Feature Learning in EEG Emotion Recognition](https://doi.org/10.48550/arxiv.2606.10718) | 2026 | arXiv preprint arXiv:2606.10718 | A transformer over the spatio-temporal dimension of the recording. | [DOI](https://doi.org/10.48550/arxiv.2606.10718) [arXiv](https://arxiv.org/abs/2606.10718) |
| [A novel Fourier Adjacency Transformer for advanced EEG emotion recognition](https://doi.org/10.1007/978-3-032-05162-2_2) | 2025 | Medical Image Computing and Computer Assisted Intervention - MICCAI 2025 | Builds the periodic and aperiodic distinction into the architecture. | [DOI](https://doi.org/10.1007/978-3-032-05162-2_2) |
| [Learning the relative composition of EEG signals using pairwise relative shift pretraining](https://openreview.net/forum?id=kk8EUOiILZ) | 2025 | Workshop on Foundation Models for the Brain and Body (BrainBodyFM) at the Conference on Neural Information Processing Systems (NeurIPS) | Pairwise relations instead of absolute values, so amplitude shifts do not matter. | [link](https://openreview.net/forum?id=kk8EUOiILZ) |
| [miMamba: EEG-based Emotion Recognition with Multi-scale Inverted Mamba Models](https://doi.org/10.1109/TAFFC.2025.3587443) | 2025 | IEEE Transactions on Affective Computing | A state-space backbone that scales to long sequences. | [DOI](https://doi.org/10.1109/TAFFC.2025.3587443) |
| [Brant-X: A Unified Physiological Signal Alignment Framework](https://doi.org/10.1145/3637528.3671953) | 2024 | Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '24) | One alignment model across several physiological signals. | [DOI](https://doi.org/10.1145/3637528.3671953) |
| [Brant: Foundation Model for Intracranial Neural Signal](https://doi.org/10.52202/075280-1144) | 2023 | Advances in Neural Information Processing Systems 36 (NeurIPS 2023) | Pre-training on intracortical signals, where data is scarce but channels are dense. | [DOI](https://doi.org/10.52202/075280-1144) |
| [EEG-Based Emotion Recognition via Channel-Wise Attention and Self Attention](https://doi.org/10.1109/TAFFC.2020.3025777) | 2023 | IEEE Transactions on Affective Computing | Channel-wise attention combined with self-attention over time. | [DOI](https://doi.org/10.1109/TAFFC.2020.3025777) |
| [Multi-Channel EEG Emotion Recognition through Residual Graph Attention Neural Network](https://doi.org/10.3389/fnins.2023.1135850) | 2023 | Frontiers in Neuroscience | A graph network with an adaptive receptive field. | [DOI](https://doi.org/10.3389/fnins.2023.1135850) |
| [EEG-Based Emotion Recognition Using Regularized Graph Neural Networks](https://doi.org/10.1109/TAFFC.2020.2994159) | 2022 | IEEE Transactions on Affective Computing | Regularisation that keeps a graph model from overfitting the training subjects. | [DOI](https://doi.org/10.1109/TAFFC.2020.2994159) |
| [EEG Emotion Recognition Using Dynamical Graph Convolutional Neural Networks](https://doi.org/10.1109/TAFFC.2018.2817622) | 2020 | IEEE Transactions on Affective Computing | The dynamic graph convolution most cross-subject work is compared against. | [DOI](https://doi.org/10.1109/TAFFC.2018.2817622) [code](https://github.com/xueyunlong12589/DGCNN) |
| [Dive into Waves: Morlet Spectral Transformer for Cross-Subject Emotion Decoding from EEG](https://doi.org/10.48550/arxiv.2606.00884) | 2026 | arXiv preprint arXiv:2606.00884 | Same data, pre-trained and task-specific, with the gap between them measured. | [DOI](https://doi.org/10.48550/arxiv.2606.00884) [arXiv](https://arxiv.org/abs/2606.00884) |
| [EMOD: A Unified EEG Emotion Representation Framework Leveraging V-A Guided Contrastive Learning](https://doi.org/10.1609/aaai.v40i21.38796) | 2026 | Proceedings of the AAAI Conference on Artificial Intelligence | Making discrete classes and continuous ratings share one target space. | [DOI](https://doi.org/10.1609/aaai.v40i21.38796) |
| [RECTOR: Masked Region-Channel-Temporal Modeling for Affective and Cognitive Representation Learning](https://doi.org/10.48550/arXiv.2606.15278) | 2026 |  | RECTOR: SEED, Three-class valence classification | [DOI](https://doi.org/10.48550/arXiv.2606.15278) [arXiv](https://arxiv.org/abs/2606.15278) |
| [Multi-dataset Joint Pre-training of Emotional EEG Enables Generalizable Affective Computing](https://doi.org/10.52202/085713-5515) | 2025 | Advances in Neural Information Processing Systems 38 (NeurIPS 2025) | Mixed label spaces across five corpora, the hardest cross-dataset setting. | [DOI](https://doi.org/10.52202/085713-5515) |
| [Cross-task, explainable and real-time decoding of human emotion states by integrating gray and white matter intracranial neural activity](https://doi.org/10.1038/s43588-026-01021-w) | 2026 | Nature Computational Science | Personalised intracranial prediction during a live task, with online participants. | [DOI](https://doi.org/10.1038/s43588-026-01021-w) |
| [Closed-loop neuromodulation in an individual with treatment-resistant depression](https://doi.org/10.1038/s41591-021-01480-w) | 2021 | Nature Medicine | A personalised biomarker that did trigger stimulation, and reached remission. | [DOI](https://doi.org/10.1038/s41591-021-01480-w) |

## Elsewhere in the Methods tier

**[Generalization & Transfer](generalization.md)** — The unit held out during testing states how far a result can travel.

All nine areas: [research-area index](README.md) · back to the [resource index](../README.md).
