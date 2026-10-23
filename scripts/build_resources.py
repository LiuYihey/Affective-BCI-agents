"""Build the resource index for Affective BCI Agents.

Reads the survey's LaTeX source and bibliography, works out which research
area each reference belongs to, and emits a machine-readable index plus
Markdown pages that list every reference with a clickable link.

Local input (never committed):
    paper/references.bib
    paper/sections/*.tex

Committed output:
    resources/papers.json
    resources/papers.md
    resources/by-area/*.md

The index is organised by research area, not by the order of the survey's
sections. A reference is filed under every area it informs; the area it
informs most often is its primary home.

Usage:
    python scripts/build_resources.py
    python scripts/build_resources.py --bib paper/references.bib
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# 1. Research areas
# --------------------------------------------------------------------------

# The index is organised by research area. The areas are named after the
# topics the literature is actually about, not after questions a reader might
# ask, so that the same words carry the same meaning in the index, in the
# survey, and in a talk about the field.
#
# Each entry is (title, scope, aspects, tier, settles).
#
# "settles" is the one-line statement of what the area answers. It is short
# enough to sit in a table column, and it is the same sentence in the README,
# in the area index, and on the area's own page.
AREAS = OrderedDict([
    ("signal", (
        "Signal Acquisition & Quality",
        "The acquisition method sets the first limit on interpretation: scalp "
        "EEG is wearable and inexpensive but mixes neural activity with eye and "
        "muscle sources, while intracranial coverage differs from patient to "
        "patient and prevents direct transfer to scalp recordings.",
        ["Modalities and what they capture", "Signal quality and artefact handling",
         "Spatial coverage and channel count", "Few-channel and wearable recording"],
        "Foundations",
        "What the recording measures, and how much of it can be trusted")),
    ("corpora", (
        "Affective Targets & Corpora",
        "Emotion cannot be observed directly, so every study uses a measurable "
        "proxy as its target. A stimulus-elicited target is assigned by the "
        "experimenter, a self-reported target comes from the participant, and "
        "an expression-observed target is read from behaviour. The three are "
        "related but not interchangeable, and a model trained on one can "
        "succeed by recognising the clip rather than the state.",
        ["Target validity and time scale", "Annotation protocols",
         "Corpus size and subject coverage", "Cross-corpus comparability"],
        "Foundations",
        "Why a measurable proxy stands in for emotion, and what it then means")),
    ("architectures", (
        "Decoding Architectures",
        "A multichannel recording can be arranged as a grid, a graph, or a "
        "sequence, and the arrangement decides what the model is able to see. "
        "The training objective is the more consequential choice: it "
        "determines whether the representation is tied to a task, a subject, "
        "or a device.",
        ["Architectures: CNN, GNN, Transformer, SSM",
         "Self-supervised pre-training", "Cross-dataset and cross-signal pre-training",
         "Device-agnostic representations"],
        "Methods",
        "How a recording is organised, and which objective decides what the "
        "model keeps")),
    ("generalization", (
        "Generalization & Transfer",
        "Recordings change across people, across sessions, and across devices. "
        "The amount of target-side data available for adaptation is part of "
        "the method rather than a detail of the protocol, and a method that "
        "needs a labelled target is a method that has to be re-run for every "
        "new user.",
        ["Within-subject to cross-dataset", "Domain generalization",
         "Unsupervised and source-free adaptation", "Personalization"],
        "Methods",
        "The unit held out during testing states how far a result can travel")),
    ("evaluation", (
        "Evaluation & Leakage Control",
        "The test split decides which question an accuracy answers, and a model "
        "can reach a high score by reading a spectral confound rather than the "
        "variable of interest. Reporting the split, the held-out unit, and the "
        "controls against leakage is the minimum for a number to mean anything.",
        ["Split protocols and split unit", "Leakage from windows and sessions",
         "Aperiodic and spectral confounds", "Perturbation-based explanation checks"],
        "Validation",
        "A favourable split or repeated test-set access can beat a better "
        "architecture")),
    ("maturity", (
        "Evidence Maturity",
        "A result supports a claim only at the level whose evidence it "
        "actually provides, and the evidence for a level has to be gathered at "
        "that level. Missing controls and undefined outcome measures are what "
        "separate one level from the next.",
        ["Lab, Pilot and Field", "Missing controls and contingencies",
         "Outcome measures and user benefit", "Reproducibility of the pipeline"],
        "Validation",
        "Lab estimates the state; Pilot changes something; Field holds up over "
        "time")),
    ("closed-loop", (
        "Closed-Loop Systems",
        "Sense turns the signal into a belief, Think proposes an action, Act "
        "decides what may reach the user. A harness keeps an adaptive system "
        "inside the range in which it was tested. Most published systems stop "
        "after Sense and report an accuracy; the loop is where the hard "
        "problems live.",
        ["Sense, Think and Act", "Action gating and fallbacks",
         "Agent harness and retained state", "Real-time operation and latency"],
        "Systems",
        "Sense proposes, Act decides, a harness keeps the system inside what "
        "was tested")),
    ("applications", (
        "Application Domains",
        "Monitoring estimates a state and stops, neurofeedback hands it to the "
        "person, neuroadaptive interfaces change the environment, and "
        "responsive neuromodulation changes the brain state directly. The four "
        "families do not share an evaluation, so a result from one is not "
        "evidence for another.",
        ["Monitoring and clinical assessment", "Neurofeedback and self-regulation",
         "Neuroadaptive interfaces", "Responsive neuromodulation"],
        "Systems",
        "Four families of system, and what each does with an estimate once it "
        "has it")),
    ("governance", (
        "Governance & Ethics",
        "Consent to record a signal does not authorise later inference from "
        "it, and an adaptive system needs a stated boundary before it reaches "
        "one. The risk is not only that a recording leaks, but that a system "
        "built for one purpose quietly acquires another.",
        ["Re-identification risk", "Consent scope and secondary use",
         "Retained state and deletion", "Clinician and user oversight"],
        "Boundaries",
        "A neural recording reveals more than the purpose it was collected for")),
])

# The tiers group the areas into the order a reader meets them.
TIERS = OrderedDict([
    ("Foundations", ["signal", "corpora"]),
    ("Methods", ["architectures", "generalization"]),
    ("Validation", ["evaluation", "maturity"]),
    ("Systems", ["closed-loop", "applications"]),
    ("Boundaries", ["governance"]),
])

# One line on what a tier is for. Shown on every page filed in that tier.
TIER_NOTES = {
    "Foundations": "What the recording is, and what the label means.",
    "Methods": "How a recording becomes a prediction.",
    "Validation": "Whether the prediction can be believed, and how far.",
    "Systems": "What the prediction is used for, once it exists.",
    "Boundaries": "What has to be settled before any of it runs.",
}

# Subsection title -> area. Keyed by title so the mapping survives edits
# to the order of the survey's sections.
# Framing sections. A reference cited here is cross-cutting: it supports the
# argument of the survey as a whole and does not belong to one area.
FRAMING_SECTIONS = {"__intro__", "__decoding_intro__", "__agent_intro__",
                    "__applications_intro__", "__levels_intro__",
                    "__challenges_intro__", "__conclusion__"}

SECTION_AREA = {
    # 02 Decoding
    "Acquisition Modalities": "signal",
    "Decoding Targets and Datasets": "corpora",
    "Evaluation Settings and Leakage": "evaluation",
    "Distribution Shift and Transfer": "generalization",
    "Model Architectures and Pre-Training": "architectures",
    # 03 Agent loop
    "Sense: Building a Reliable Observation": "closed-loop",
    "Think: Turning an Estimate into a Proposal": "closed-loop",
    "Act: Controlling What Reaches the User": "closed-loop",
    "How Action Changes Later Data": "closed-loop",
    "Who Controls the Action": "closed-loop",
    # 04 Applications
    "Affect Monitoring and Assessment": "applications",
    "Neurofeedback and Self-Regulation": "applications",
    "Neuroadaptive Interfaces": "applications",
    "Responsive Neuromodulation": "applications",
    # 05 Levels
    "Lab: testing the estimate": "maturity",
    "Pilot: testing the interaction": "maturity",
    "Field: testing long-term use": "maturity",
    # 06 Challenges
    "Target validity": "corpora",
    "Transfer": "generalization",
    "Real-time operation": "closed-loop",
    "Demonstrated benefit": "maturity",
    "Governance": "governance",
}

# Fallback for references the survey cites only as framing: infer the area
# from the title. Ordered by specificity.
TITLE_AREA = [
    ("governance", r"\b(govern|ethic|consent|privacy|re-identif|anonym|"
                   r"authenticat|retention|four prior)\w*\b"),
    ("corpora", r"\b(dataset|corpus|SEED|DEAP|DREAMER|AMIGOS|MPED|FACED|"
                r"annotation|label|target|benchmark)\w*\b"),
    ("evaluation", r"\b(evaluat|leakage|audit|explain|interpretab|spectral)\b"),
    ("generalization", r"\b(cross-subject|domain|transfer|generaliz|adapt)\w*\b"),
    ("closed-loop", r"\b(closed-loop|neurofeedback|agent|music|real-time|"
                    r"stimulat|neuroprosthe)\w*\b"),
    ("applications", r"\b(clinical|depress|patient|disorder|monitor|"
                      r"neuroadapt|self-regulat)\w*\b"),
    ("architectures", r"\b(graph|transformer|mamba|attention|convolution|"
                       r"network|pre-train|contrastive|representation)\w*\b"),
    ("signal", r"\b(modality|electrode|scalp|intracranial|artifact|artefact|"
                r"few-channel|fNIRS|fMRI|iEEG)\w*\b"),
]

# file -> (preamble label, [subsection titles])
SURVEY_FILES = OrderedDict([
    ("paper/sections/01_introduction.tex",
     ("__intro__", [])),
    ("paper/sections/02_brain_decoding.tex",
     ("__decoding_intro__", ["Acquisition Modalities", "Decoding Targets and Datasets",
                             "Evaluation Settings and Leakage", "Distribution Shift and Transfer",
                             "Model Architectures and Pre-Training"])),
    ("paper/sections/03_bci_agent.tex",
     ("__agent_intro__", ["Sense: Building a Reliable Observation",
                          "Think: Turning an Estimate into a Proposal",
                          "Act: Controlling What Reaches the User",
                          "How Action Changes Later Data",
                          "Who Controls the Action"])),
    ("paper/sections/04_applications.tex",
     ("__applications_intro__", ["Affect Monitoring and Assessment",
                                 "Neurofeedback and Self-Regulation",
                                 "Neuroadaptive Interfaces",
                                 "Responsive Neuromodulation"])),
    ("paper/sections/05_levels.tex",
     ("__levels_intro__", ["Lab: testing the estimate",
                           "Pilot: testing the interaction",
                           "Field: testing long-term use"])),
    ("paper/sections/06_challenges.tex",
     ("__challenges_intro__", ["Target validity", "Transfer", "Real-time operation",
                               "Demonstrated benefit", "Governance"])),
    ("paper/sections/07_conclusion.tex",
     ("__conclusion__", [])),
])

# --------------------------------------------------------------------------
# 2. Bibliography parsing
# --------------------------------------------------------------------------

ARXIV_DOI = re.compile(r"10\.48550/arXiv\.(\d{4}\.\d{4,5})", re.I)
ARXIV_URL = re.compile(r"arxiv\.org/(?:abs|pdf)/([\w.\-]+)", re.I)


def clean_latex(text: str) -> str:
    # Footnote markers are removed first: the generic command strip below would
    # otherwise turn "\dagger" into a space and leave an empty "$^{ }$" behind.
    for marker in (r"$^{\dagger}$", r"$^{\ddagger}$", r"^{\dagger}",
                   r"^{\ddagger}", r"\dagger", r"\ddagger"):
        text = text.replace(marker, "")
    text = re.sub(r"\\[a-zA-Z]+\s*", " ", text)
    for a, b in (("{", ""), ("}", ""), ("~", " "), ("\\&", "&"), ("\\_", "_"),
                 ("--", "-"), ("\\%", "%"), ("\\textsuperscript", ""), ("\\$", "")):
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip()


def strip_cites(cell: str) -> str:
    """Remove \\cite{...} and its trailing punctuation from a table cell."""
    cell = re.sub(r"\\cite\{[^}]*\}", "", cell)
    # Footnote markers go before the generic command strip, which would
    # otherwise blank out "\dagger" and leave an empty "$^{ }$" in the cell.
    for marker in (r"$^{\dagger}$", r"$^{\ddagger}$", r"^{\dagger}",
                   r"^{\ddagger}", r"\dagger", r"\ddagger"):
        cell = cell.replace(marker, "")
    cell = re.sub(r"\\[a-zA-Z]+\s*", " ", cell)
    return cell.replace("{", "").replace("}", "").strip()


def parse_bib(path: Path) -> "OrderedDict[str, dict]":
    text = path.read_text(encoding="utf-8")
    entries: "OrderedDict[str, dict]" = OrderedDict()
    for chunk in re.split(r"(?=@\w+\{)", text):
        m = re.match(r"@(\w+)\{([^,]+),", chunk)
        if not m:
            continue
        kind, key = m.group(1).lower(), m.group(2).strip()

        def field(name: str) -> str:
            fm = re.search(r"\b%s\s*=\s*[\{\"](.+?)[\"\}]\s*,?\s*\n" % name, chunk, re.S)
            return clean_latex(fm.group(1)) if fm else ""

        doi = field("doi")
        url = field("url")
        arxiv = ""
        am = ARXIV_DOI.search(doi) or ARXIV_URL.search(url)
        if am:
            # The canonical abs URL drops the version suffix, so the link
            # always resolves to the current version of the preprint.
            arxiv = "https://arxiv.org/abs/" + re.sub(r"v\d+$", "", am.group(1))

        entries[key] = {
            "key": key,
            "title": field("title"),
            "venue": field("journal") or field("booktitle") or field("publisher"),
            "year": field("year"),
            "type": kind,
            "doi": ("https://doi.org/" + doi) if doi else "",
            "arxiv": arxiv,
            "url": url if url and not ARXIV_URL.search(url) else "",
        }
    return entries


# --------------------------------------------------------------------------
# 3. Citation map and table extraction
# --------------------------------------------------------------------------

CITE_RE = re.compile(r"\\cite\{([^}]+)\}")


def citation_map() -> "dict[str, Counter]":
    """cite key -> Counter(section label -> number of citations)."""
    counts: "dict[str, Counter]" = {}
    for rel, (pre_label, sub_titles) in SURVEY_FILES.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        marks = [(m.start(), m.group(1)) for m in
                 re.finditer(r"\\subsection\{([^}]*)\}", text)]
        if not marks:
            spans = [(pre_label, text)]
        else:
            spans = []
            if marks[0][0] > 0:
                spans.append((pre_label, text[: marks[0][0]]))
            for i, (pos, name) in enumerate(marks):
                end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
                spans.append((name, text[pos:end]))
        for label, body in spans:
            for m in CITE_RE.finditer(body):
                for k in m.group(1).split(","):
                    k = k.strip()
                    if k:
                        counts.setdefault(k, Counter())[label] += 1
    return counts


TABLE_LABELS = {
    "tab:datasets": "corpus",
    "tab:decoders": "method",
    "tab:systems": "system",
}


def extract_tables() -> "dict[str, list[dict]]":
    """label -> rows of {name, cite keys, cells, group, source}."""
    out: "dict[str, list[dict]]" = {}
    for path in (ROOT / "paper/sections").glob("*.tex"):
        text = path.read_text(encoding="utf-8")
        for label in TABLE_LABELS:
            i = text.find("\\label{%s}" % label)
            if i < 0:
                continue
            j = text.find("\\end{tabularx}", i)
            body = text[i:j]
            rows = []
            group = ""
            for raw in body.split("\\\\"):
                gm = re.search(r"\\grouphead\{[^}]*\}\{([^}]*)\}", raw)
                if gm:
                    group = clean_latex(gm.group(1))
                    continue
                if "&" not in raw or "\\cite" not in raw:
                    continue
                keys = []
                for m in CITE_RE.finditer(raw):
                    for k in m.group(1).split(","):
                        k = k.strip()
                        if k and k not in keys:
                            keys.append(k)
                if not keys:
                    continue
                cells = [clean_latex(strip_cites(c)) for c in raw.split("&")]
                name = cells[0].strip()
                if not name:
                    continue
                # The citation in the name cell identifies the corpus itself;
                # later citations in the row are supporting references.
                source = keys[0]
                rows.append({"name": name, "keys": keys, "cells": cells,
                             "group": group, "source": source})
            out[label] = rows
    return out


# --------------------------------------------------------------------------
# 4. Annotations
# --------------------------------------------------------------------------

# Official implementations, each confirmed reachable and matching the paper.
CODE_OVERRIDES = {
    "song2020dynamical": "https://github.com/xueyunlong12589/DGCNN",
    "chang2025hyperbolic": "https://github.com/JiangChang-BRAIN/MSHCL",
    "yan2025cross": "https://github.com/Xeaver/EmotionCLIP",
    "xie2026harnesssurvey": "https://github.com/HKUST-KnowComp/Awesome-Agent-Harness",
    "tang2026peakflow": "https://github.com/jukebox333/PeakFlow",
    "kukhilava2025evaluation": "https://github.com/EmotionLab/EEGain",
    "gui2026spotr": "https://github.com/5GYYYYY/SPOTR",
    "li2026boundary": "https://github.com/WuCB-BCI/PAA",
    "zhou2026local": "https://github.com/Danielz-z/LGF-EEG-Emotion",
    "wu2026region": "https://github.com/RyanLi-X/RSM-CoDG",
    "tang2025sda": "https://github.com/XuanSuTrum/SDA-DDA",
    "hu2026see": "https://github.com/xian-sh/SeeEmotion",
    "yik2025neurobench": "https://github.com/lava-nc/lava",
}

# One line per reference saying why a practitioner would open it. Hand-written
# for the references that anchor a table or a claim; the rest fall back to a
# note derived from the question they inform.
NOTES = {
    "zheng2015investigating": "The reference corpus for stimulus-elicited emotion labels.",
    "zheng2019emotionmeter": "Four emotion classes, three sessions, the standard benchmark for cross-session work.",
    "chen2023faced": "The largest stimulus-elicited corpus here: 123 participants, nine classes.",
    "liu2022comparing": "Adds eye tracking to SEED-V, so the label has an independent behavioural channel.",
    "koelstra2012deap": "The standard continuous valence and arousal corpus.",
    "soleymani2012mahnob": "Valence, arousal and dominance with peripheral channels and predictability ratings.",
    "katsigiannis2018dreamer": "Valence, arousal and dominance with ECG, widely used for cross-subject comparison.",
    "mirandacorrea2021amigos": "Self-report plus external annotation, which makes target substitution visible.",
    "song2019mped": "Seven emotion categories with three questionnaires, the hardest categorical corpus here.",
    "jiang2025seedvii": "Six emotions plus neutral with continuous intensity, and four sessions.",
    "guo2026mad": "Records all three target sources separately, and defines the annotation levels used throughout.",
    "sani2018mood": "Multiday intracranial mood tracking, the basis for the Lab level.",
    "yang2026crosstask": "Personalised intracranial prediction during a live task, with online participants.",
    "xiao2023decoding": "Prefrontal intracranial coverage for depression severity.",
    "bijanzadeh2022decoding": "116 hours over 11 participants, and a gap between per-person and group accuracy.",
    "alagapan2023cingulate": "A marker that follows recovery without ever triggering stimulation.",
    "kukhilava2025evaluation": "A survey of 216 papers: how many hold participants apart, and how many do not say.",
    "suo2026evaluation": "A controlled audit showing how much a favourable split can inflate accuracy.",
    "bindra2026spectral": "Six of seven foundation models depend on the aperiodic background component.",
    "wang2025hedn": "The clearest example of how much target-side data changes the reported score.",
    "qing2026dive": "Same data, pre-trained and task-specific, with the gap between them measured.",
    "zhang2025multidataset": "Mixed label spaces across five corpora, the hardest cross-dataset setting.",
    "zhou2026prism": "A state-space backbone with expert-routed channel gating.",
    "zhang2022parse": "Semi-supervised alignment with a small labelled target set.",
    "song2020dynamical": "The dynamic graph convolution most cross-subject work is compared against.",
    "rudin2019explain": "The case for perturbing inputs instead of reading saliency maps.",
    "woo2017buildingbiomarkers": "Defines a biomarker backwards from its intended use, the basis of the governance rules.",
    "scangos2021closedloop": "A personalised biomarker that did trigger stimulation, and reached remission.",
    "gill2023pilot": "Amygdala-triggered stimulation, with a control group still missing.",
    "zhang2026mindmelody": "EEG-driven music generation, and a report without significance tests.",
    "monroydcroz2026minimalist": "A musical BCI where the control signal showed no effect on the target emotion.",
    "baradari2025neurochat": "Engagement-adaptive dialogue, where adaptation changed the measure but not learning.",
    "wen2025adaptivecopilot": "Workload-adaptive guidance, where adaptation produced more errors than the baseline.",
    "li2026mindpilot": "EEG-guided image generation, with a second experiment that removes the neural input.",
    "kosmyna2026neuroskill": "An agentic system that invokes tools, with no user-level outcome reported.",
    "sitaram2017neurofeedback": "Why the display has to be truly contingent for the result to mean anything.",
    "debettencourt2015": "Yoked and no-feedback conditions, the controls that separate signal from response.",
    "huang2023neurofeedback": "Learning across ten sessions, which does not show transfer beyond the loop.",
    "li2025universal": "A shared channel vocabulary, and a subject-specific encoder on top of it.",
    "chen2025emod": "Making discrete classes and continuous ratings share one target space.",
    "zhou2026brainbench": "Instruction-conditioned benchmarks for language models that analyse EEG.",
    "xie2026harnesssurvey": "The agent harness literature the governance layer is built on.",
    "rao2018direct": "Open-loop stimulation, which can identify a target but not test biomarker timing.",
    "zich2020modulatory": "Modulatory connectivity as a control signal for emotion regulation.",
    "nassibi2025systematic": "A map of the diagnostic EEG literature for affective states.",
    "kwok2025fairness": "A fairness audit across EEG depression datasets, and the subgroup gap it finds.",
    "li2025neuraldiffuser": "Reconstructing viewed images from archived fMRI.",
    "fallahi2026neuroshield": "Representations that identify the person who produced a recording.",
    "steinert2020wiredemotions": "What a neural recording reveals beyond the purpose it was collected for.",
    "yuste2017fourpriorities": "Four priorities for neurotechnology, including data sharing.",
    "li2026rector": "Channel and montage removal as a test of whether a model learned relations.",
    "koelstra2012deap": "The standard continuous valence and arousal corpus.",
    "zhou2024mimamba": "A state-space backbone that scales to long sequences.",
    "yan2025cross": "EEG matched against text, and the small annotated set it needs.",
    "chao2023rgan": "A graph network with an adaptive receptive field.",
    "sitaram2017neurofeedback": "Why contingency decides whether a neurofeedback result means anything.",
    "nassibi2025systematic": "A map of the diagnostic EEG literature for affective states.",
    "kukhilava2025evaluation": "A survey of 216 papers on how the split was chosen.",
    "wang2025fourier": "Builds the periodic and aperiodic distinction into the architecture.",
}


# Short reasons to open a reference that no table or claim anchors.
FALLBACK_NOTES = {
    "tang2026peakflow": "Handles the case where the peak in a rating does not mark the peak in the signal.",
    "xu2025refs": "Feature selection when part of the annotation is missing.",
    "liu2024fewchannel": "Decoding from few electrodes, which is what a wearable actually provides.",
    "qasim2023neuronal": "Amygdala and hippocampus activity predicting mood on the next day.",
    "dehghani2020probing": "fMRI connectivity during emotion regulation, the imaging counterpart.",
    "piho2020mutual": "Choosing the analysis window from the data instead of by hand.",
    "hwang2026b": "A flow-matching formulation of the brain foundation model.",
    "mahuas2026cocot": "Contrastive pre-training before the task-specific stage.",
    "minnick2026implicit": "Behaviour decoded implicitly, from the next step of the signal.",
    "lopes2026learning": "Shared representations with a subject-specific encoder on top.",
    "weng2026masked": "Masked and generative objectives combined for cross-subject learning.",
    "gong2026mscgc": "Causal graph convolution with a Kolmogorov-Arnold parameterisation.",
    "gui2026spotr": "One-token reconstruction as the pre-training objective.",
    "segal2026stst": "Joint embedding prediction for spatio-temporal structure.",
    "sigdel2026rg": "Scale-free dynamics, for corpora where there are few subjects.",
    "cui2026transformer": "A transformer over the spatio-temporal dimension of the recording.",
    "sandino2025learning": "Pairwise relations instead of absolute values, so amplitude shifts do not matter.",
    "zhang2024brantx": "One alignment model across several physiological signals.",
    "zhang2023brant": "Pre-training on intracortical signals, where data is scarce but channels are dense.",
    "tao2023cwsa": "Channel-wise attention combined with self-attention over time.",
    "zhong2022regularized": "Regularisation that keeps a graph model from overfitting the training subjects.",
    "imtiaz2026enhanced": "Domain adaptation with no source data at hand, which is the realistic case.",
    "jang2025crossmodal": "Active learning that chooses which samples to label next.",
    "kuang2026graph": "Graph regularisation on the electrode adjacency structure.",
    "meng2026group": "Learnable prototypes instead of one model per subject.",
    "zhou2026local": "Local and global features together, which is what generalisation needs.",
    "wu2026region": "Collaborative domain alignment over brain regions.",
    "liu2025ssas": "Source selection across subjects, so the target uses the closest source.",
    "hong2025adaptive": "Adaptive alignment, where the amount of alignment is learned.",
    "li2025freqdgt": "Frequency-adaptive graph construction.",
    "tang2025sda": "Semi-supervised domain adaptation with a changing distribution.",
    "gong2025tahag": "Two-stage alignment with a hybrid graph structure.",
    "gu2023dggn": "A generative step that produces target-like data for alignment.",
    "shen2023contrastive": "Contrastive training that removes subject-specific variation.",
    "jaiswal2023subject": "Subject-agnostic representations across several affect corpora.",
    "wu2022transfer": "A review of transfer learning for EEG-based BCIs.",
    "wang2021prototype": "Prototypes in the SPD manifold, where covariance is the natural representation.",
    "wan2021transfer": "A review of transfer learning in EEG analysis.",
    "he2020euclidean": "Transfer that works in the SPD space of covariance matrices.",
    "kim2026closed": "Soft bioelectronic interfaces for closed-loop neurofeedback.",
    "pham2026cross": "Reconstructing intracranial activity from scalp recordings.",
    "zhou2026brain": "Topography as the structure the model builds on.",
    "li2026sa": "Hyperbolic geometry for depression recognition.",
    "hu2026see": "Facial expression used as a proxy label for EEG emotion.",
    "jiang2025interpretable": "A fuzzy model whose filters are readable by a person.",
    "zhang2022visual2eeg": "Knowledge distilled from visual stimuli into EEG representations.",
    "drysdale2017depressionsubtypes": "Resting-state subtypes of depression, and their response to treatment.",
    "zhou2026brainagent": "An LLM-driven multi-agent framework over EEG.",
    "xiong2025affective": "A closed-loop BCI that recognises affect and responds in kind.",
    "duraisamy2025adaptive": "An adaptive game where the interface follows the user's state.",
    "herbuela2025realtime": "Real-time multimodal estimation, behaviour alongside the signal.",
    "willett2023speech": "62 words per minute from a speech neuroprosthesis.",
    "moses2021neuroprosthesis": "Speech decoded in a person who cannot speak.",
    "zotev2020simultaneous": "Simultaneous fMRI and EEG neurofeedback, and what each adds.",
    "shanechi2019brain": "From motor control to mood: what brain-machine interfaces could reach.",
    "zhou2026eegdancer": "Dynamic emotion latent space with masked modelling.",
    "djibrina2026energy": "Emotion as the stability of a network, rather than a label.",
    "he2026i": "Spectral Riemannian representations with temporal attention.",
    "kabotyanski2026intracranial": "Which intracranial biomarkers could actually guide stimulation.",
    "pan2026arousal": "Annotation-efficient continuous arousal estimation.",
    "hazra2025bridging": "Accuracy and explainability held together rather than traded off.",
    "yik2025neurobench": "A benchmark framework for neuromorphic computing.",
    "oganesian2024brain": "A review of BCIs for neuropsychiatric disorders.",
    "lozano2013": "Deep brain stimulation guided by a functional circuit model.",
    "chaudhary2016bci": "The clinical landscape of BCIs for communication and rehabilitation.",
}


def annotation_for(key: str, entry: dict, area: str, table_rows: list[dict]) -> str:
    """A one-line reason to open this reference."""
    if key in NOTES:
        return NOTES[key]
    for row in table_rows:
        if key in row["keys"]:
            cells = [c for c in row["cells"] if c]
            detail = ", ".join(cells[1:3]) if len(cells) > 2 else ""
            return "%s: %s" % (row["name"], detail) if detail else row["name"]
    return FALLBACK_NOTES.get(key, "")


# --------------------------------------------------------------------------
# 5. Emit
# --------------------------------------------------------------------------

LINK_FIELDS = (("doi", "DOI"), ("arxiv", "arXiv"), ("url", "link"), ("code", "code"))


def link_cell(entry: dict) -> str:
    parts = []
    seen = set()
    for f, label in LINK_FIELDS:
        url = entry.get(f)
        if not url or url in seen:
            continue
        seen.add(url)
        parts.append("[%s](%s)" % (label, url))
    return " ".join(parts) if parts else "&mdash;"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="paper/references.bib")
    args = ap.parse_args()

    entries = parse_bib(ROOT / args.bib)
    cites = citation_map()
    tables = extract_tables()

    table_by_key = {}
    for label, rows in tables.items():
        for row in rows:
            for k in row["keys"]:
                table_by_key.setdefault(k, []).append((label, row))

    records = []
    for key, entry in entries.items():
        c = cites.get(key, Counter())
        areas = []
        for section, _ in c.most_common():
            cl = SECTION_AREA.get(section)
            if cl and cl not in areas:
                areas.append(cl)

        # A reference cited only in framing sections carries the argument of the
        # survey as a whole; it is filed under the area it touches most,
        # or left cross-cutting when nothing else applies.
        framing_only = bool(c) and all(
            s in FRAMING_SECTIONS for s in c)
        if not areas:
            areas = ["maturity"]

        # The maturity tier is what a reference supports, not where it is
        # mentioned. A study is usually cited in the levels section and again
        # where its result is discussed, so the level decides the home.
        level_sections = {"Lab: testing the estimate": "Lab",
                           "Pilot: testing the interaction": "Pilot",
                           "Field: testing long-term use": "Field"}
        levels = [level_sections[s] for s in c if s in level_sections]

        weights = Counter()
        for section, n in c.items():
            cl = SECTION_AREA.get(section)
            if cl:
                weights[cl] += n
        primary = (min(weights.items(),
                       key=lambda kv: (-kv[1], list(AREAS).index(kv[0])))[0]
                   if weights else areas[0])

        if levels:
            primary = "maturity"
            areas = ["maturity"] + [x for x in areas if x != "maturity"]

        # Framing-only references get an area from their own title, since the
        # surrounding prose places them but does not test them.
        if framing_only:
            hay = (entry["title"] + " " + entry["venue"]).lower()
            for cl, pattern in TITLE_AREA:
                if re.search(pattern, hay, re.I):
                    primary = cl
                    areas = [cl]
                    break

        rec = dict(entry)
        rec["primary_area"] = primary
        rec["areas"] = areas
        rec["tier"] = AREAS[primary][3]
        rec["sections"] = sorted(c.keys())
        rec["cite_count"] = sum(c.values())
        rec["code"] = CODE_OVERRIDES.get(key, "")
        rec["levels"] = levels
        rec["note"] = annotation_for(key, entry, primary,
                                      [r for _, r in table_by_key.get(key, [])])
        records.append(rec)

    records.sort(key=lambda r: (list(AREAS).index(r["primary_area"]),
                                 -(int(r["year"]) if r["year"].isdigit() else 0),
                                 r["title"].lower()))

    out = ROOT / "resources"
    (out / "by-area").mkdir(parents=True, exist_ok=True)

    corpora = []
    for label, rows in tables.items():
        if label != "tab:datasets":
            continue
        for row in rows:
            src = entries.get(row["source"], {})
            corpora.append({
                "name": row["name"],
                "group": row["group"],
                "scale": row["cells"][1] if len(row["cells"]) > 1 else "",
                "modality": row["cells"][2] if len(row["cells"]) > 2 else "",
                "target": row["cells"][4] if len(row["cells"]) > 4 else "",
                "obtained": row["cells"][5] if len(row["cells"]) > 5 else "",
                "source": row["source"],
                "source_link": src.get("doi") or src.get("arxiv") or src.get("url") or "",
                "refs": [k for k in row["keys"] if k in entries],
            })

    (out / "papers.json").write_text(json.dumps({
        "areas": {k: {"title": v[0], "summary": v[1], "aspects": v[2],
                      "tier": v[3], "settles": v[4]}
                  for k, v in AREAS.items()},
        "tiers": {t: list(areas) for t, areas in TIERS.items()},
        "corpora": corpora,
        "papers": records,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Reference index",
        "",
        "Every reference in the index, with a direct link, grouped by the area "
        "it belongs to and ordered by year within that area.",
        "",
        "| Paper | Year | Venue | Area | Links |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for r in records:
        lines.append("| [%s](%s) | %s | %s | %s | %s |" % (
            r["title"], r["doi"] or r["arxiv"] or r["url"] or "#",
            r["year"], r["venue"], AREAS[r["primary_area"]][0], link_cell(r)))
    lines += ["", "The same references, one area per page: "
              "[research-area index](by-area/README.md)."]
    (out / "papers.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for key, (title, summary, aspects, tier, settles) in AREAS.items():
        members = [r for r in records if key in r["areas"]]
        prim = sum(1 for r in members if r["primary_area"] == key)
        page = ["# %s" % title, "",
                "> **%s tier** — %s" % (tier, TIER_NOTES[tier]), "",
                settles + ".", ""]
        page += textwrap.wrap(summary, 76)
        page += ["",
                 "**%d references** are listed here; %d of them are filed primarily "
                 "under this area." % (len(members), prim), "",
                 "## What to look for", ""]
        page += ["- %s" % a for a in aspects]
        page += ["", "## References", "",
                 "| Paper | Year | Venue | Note | Links |",
                 "| --- | ---: | --- | --- | --- |"]
        for r in members:
            page.append("| [%s](%s) | %s | %s | %s | %s |" % (
                r["title"], r["doi"] or r["arxiv"] or r["url"] or "#",
                r["year"], r["venue"], r["note"], link_cell(r)))
        # Sibling areas in the same tier, so a reader can move sideways.
        siblings = [k for k in TIERS[tier] if k != key]
        page += ["", "## Elsewhere in the %s tier" % tier, ""]
        if siblings:
            page.append("**%s** — %s." % (
                ", ".join("[%s](%s.md)" % (AREAS[k][0], k) for k in siblings),
                "; ".join(AREAS[k][4] for k in siblings)))
        else:
            page.append("This is the only area in the %s tier, and the last "
                        "thing a reader has to settle before any of the work "
                        "runs." % tier)
        page += ["",
                 "All nine areas: [research-area index](README.md) · "
                 "back to the [resource index](../README.md)."]
        (out / "by-area" / ("%s.md" % key)).write_text(
            "\n".join(page) + "\n", encoding="utf-8")

    # Index page for the directory itself, so that resources/by-area/ opens
    # on something useful rather than a file listing.
    page = ["# Research areas", "",
            "The nine areas the index is organised around, in the five tiers a "
            "reader meets them in.", ""]
    for tier, keys in TIERS.items():
        page += ["## %s" % tier, "", TIER_NOTES[tier], "",
                 "| Research area | References | What it settles |",
                 "|:--|--:|:--|"]
        for key in keys:
            title, _, _, _, settles = AREAS[key]
            members = [r for r in records if key in r["areas"]]
            page.append("| [%s](%s.md) | %d | %s |"
                        % (title, key, len(members), settles))
        page.append("")
    page += ["## Elsewhere", "",
             "Back to the [resource index](../README.md) · "
             "[all references in one table](../papers.md) · "
             "[the corpus list](../corpora.md)."]
    (out / "by-area" / "README.md").write_text(
        "\n".join(page) + "\n", encoding="utf-8")

    # Corpora page, grouped by how the target was obtained.
    page = ["# Corpora", "",
            "Every corpus in the field, grouped by how the target was obtained.",
            "The grouping matters more than the size: a label assigned by the",
            "experimenter, reported by the participant, or read from behaviour",
            "answer different questions, and a number from one group does not",
            "transfer to another.", ""]
    groups = []
    for c in corpora:
        if c["group"] and (not groups or groups[-1] != c["group"]):
            groups.append(c["group"])
    for g in groups:
        members = [c for c in corpora if c["group"] == g]
        page += ["## %s" % g, "",
                 "| Corpus | Scale | Modality | Target | How the target is obtained | Source |",
                 "| --- | --- | --- | --- | --- | --- |"]
        for c in members:
            link = ("[source](%s)" % c["source_link"]) if c["source_link"] else "&mdash;"
            page.append("| **%s** | %s | %s | %s | %s | %s |" % (
                c["name"], c["scale"], c["modality"], c["target"], c["obtained"], link))
        page.append("")
    page += ["## The same corpora, by scale", "",
             "![Participants per corpus, log scale, grouped by how the target was "
             "elicited](../assets/figures/corpora_scale.png)", "",
             "<p align=\"center\"><sub><b>Corpus scale</b> — participants per corpus "
             "on a log scale, grouped by how the target was elicited.</sub></p>", ""]
    (out / "corpora.md").write_text("\n".join(page) + "\n", encoding="utf-8")

    total = len(records)
    linked = sum(1 for r in records if r["doi"] or r["arxiv"] or r["url"])
    print("papers %d | linked %d | unlinked %d" % (total, linked, total - linked))
    for r in records:
        if not (r["doi"] or r["arxiv"] or r["url"]):
            print("  MISSING:", r["key"], "|", r["title"])
    print()
    for tier, keys in TIERS.items():
        print("  [%s]" % tier)
        for key in keys:
            prim = sum(1 for r in records if r["primary_area"] == key)
            cross = sum(1 for r in records
                        if key in r["areas"] and r["primary_area"] != key)
            print("    %-14s primary %3d  cross %3d  total %3d  %s"
                  % (key, prim, cross, prim + cross, AREAS[key][0]))


if __name__ == "__main__":
    main()
