<div align="center">

<img src="assets/logo.png" width="820" alt="Affective BCI Agents">

# Affective BCI Agents

**A working map of the field that decodes how a brain signal becomes an action.**

127 papers, 8 questions, 188 verified links.

[![Links](https://img.shields.io/badge/links-188%20verified-0FDC78?style=flat-square)](resources/README.md)
[![Papers](https://img.shields.io/badge/references-127-2F6EA5?style=flat-square)](resources/papers.md)
[![Code](https://img.shields.io/badge/open--source-13-2F6EA5?style=flat-square)](resources/README.md)
[![License](https://img.shields.io/badge/license-MIT-C4622D?style=flat-square)](LICENSE)

</div>

---

## What this is

Affective BCI turns a brain signal into something that **helps a person** — a
display that adjusts, a word that comes back, a stimulation that fires at the
right moment. Getting there is not one problem but a chain, and each link in
the chain breaks in its own way.

This repository is organised around that chain, not around a paper. Each
section below is a question someone actually asks, and each links to the
references that answer it, with a note on **why you would open that paper**.

```
signal  →  label  →  model  →  generalisation  →  evaluation
                                                        ↓
                              governance  ←  deployment  ←  closed loop
```

Four families of system do this, and they differ in what they do with the
estimate once they have it:

<img src="assets/figures/applications.png" width="100%" alt="Four families of affective BCI system: affect monitoring and assessment, neurofeedback and self-regulation, neuroadaptive interfaces, and responsive neuromodulation">

**Monitoring** estimates a state and stops there. **Neurofeedback** hands the
state back to the person to regulate. **Neuroadaptive** interfaces change the
environment to fit the person. **Responsive neuromodulation** changes the
person's brain state directly. The four are not interchangeable, and a result
from one does not transfer to another.

---

## Start here

<table>
<tr>
<td width="50%" valign="top">

**If you are new to the field**

1. [Which corpus should I use?](resources/by-question/datasets.md) — and why the
   label matters more than the signal
2. [Is that accuracy real?](resources/by-question/evaluation.md) — the split
   decides the question your number answers
3. [How do I wire a decoder into a loop?](resources/by-question/closed-loop.md)

**If you are building a system**

4. [Will it work on a person I have never seen?](resources/by-question/transfer.md)
5. [Can I run this in real time?](resources/by-question/deployment.md)
6. [How strong is the evidence?](resources/by-question/maturity.md)

</td>
<td width="50%" valign="top">

**If you are reviewing work in this area**

- [Is that accuracy real?](resources/by-question/evaluation.md) — leakage,
  spectral confounds, split protocols
- [How strong is the evidence?](resources/by-question/maturity.md) — what a
  pilot study has to report before it counts
- [Where is the boundary?](resources/by-question/governance.md) — consent,
  retention, re-identification

**If you are looking for a survey**

The framework this repository follows is set out in a companion survey. It is
not yet published, so there is no link to follow yet — the framing used in
these pages is drawn from it, and it will be referenced here once it is
available.

</td>
</tr>
</table>

---

## The eight questions

Each one is a page of linked references, with a note per reference on what it
settles and where it does not.

| | Question | What it settles | References |
|---|---|---|---|
| 1 | [Which corpus should I use?](resources/by-question/datasets.md) | Where the signal comes from, how the label was produced, how many people it covers | 28 |
| 2 | [How do I turn a recording into a prediction?](resources/by-question/model.md) | Architectures for organising a recording, and the objectives that decide what the model keeps | 28 |
| 3 | [Will it work on a person I have never seen?](resources/by-question/transfer.md) | The unit held out during testing states how far a result can travel | 36 |
| 4 | [Is that accuracy real?](resources/by-question/evaluation.md) | A favourable split or repeated test-set access can beat a better architecture | 21 |
| 5 | [How do I wire a decoder into a loop that stays safe?](resources/by-question/closed-loop.md) | Sense proposes, Act decides, a harness keeps the system inside what was tested | 28 |
| 6 | [Can I run this in real time?](resources/by-question/deployment.md) | Latency, hardware, and the different risk of each output destination | 26 |
| 7 | [How strong is the evidence?](resources/by-question/maturity.md) | Lab asks if the state can be estimated; Pilot if the estimate changes something; Field if the whole system holds up | 19 |
| 8 | [Where is the boundary?](resources/by-question/governance.md) | A neural recording reveals more than the purpose it was collected for | 7 |

References appear under every question they inform. The counts above therefore
exceed 127.

---

## The map

<img src="assets/figures/sense_think_act.png" width="100%" alt="Sense, Think and Act: the closed loop from neural signal to user-facing action, with the gate that decides what reaches the user">

**Sense — Think — Act.** The signal becomes a belief, the belief becomes a
proposal, and something decides whether the proposal reaches the person. Most
systems in this field stop after the first step and report an accuracy; the
loop is where the hard problems live.

<div align="center">

| | |
|:--|:--|
| <img src="assets/figures/corpora_scale.png" alt="Participants per corpus, log scale, grouped by how the target was elicited"> | <img src="assets/figures/levels.png" alt="Lab, Pilot and Field: what each maturity level tests"> |

</div>

**Corpora.** Sixteen corpora, grouped by how the target was elicited — by the
experimenter, reported by the participant, or read from behaviour. The groups
are not interchangeable, and a number from one does not transfer to another.

**Maturity.** Lab tests the estimate. Pilot lets the estimate change something
during a limited experiment. Field uses the complete system repeatedly in the
setting it was built for. Most published work stops at the first.

---

## What is here

| Path | What it holds |
|---|---|
| [`resources/by-question/`](resources/README.md) | The 8 question pages — every reference, linked, with a note |
| [`resources/papers.md`](resources/papers.md) | All 127 references in one table |
| [`resources/papers.json`](resources/papers.json) | The same index as data, for filtering |
| [`playbooks/`](playbooks/README.md) | Checklists for designing an experiment, a loop, or a review |
| [`assets/figures/`](assets/figures) | Figures, exported at 200 dpi |
| [`scripts/`](scripts/) | The generator and the link checker |

### Reference index

Every reference is one click away. Links are verified in CI, so a dead DOI
fails the build rather than sitting in a table.

```
python scripts/check_index.py          # the index agrees with itself
python scripts/check_links.py          # verify every link
```

---

## Contributing

Additions welcome — a corpus, a method, a system, a critique that changes how
the field should be measured. See [CONTRIBUTING.md](CONTRIBUTING.md).

- [Add a reference](.github/ISSUE_TEMPLATE/add-reference.yml)
- [Add a dataset](.github/ISSUE_TEMPLATE/add-dataset.yml)
- [Report a broken link](.github/ISSUE_TEMPLATE/broken-link.yml)

---

<div align="center">

**If this map was useful, a star helps others find it.**

</div>
