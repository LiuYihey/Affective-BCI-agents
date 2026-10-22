<div align="center">

<img src="assets/logo.png" width="760" alt="Affective BCI Agents">

# Affective BCI Agents

**A working map of the field that turns a brain signal into an action.**

127 references · 9 research areas · 16 corpora · 188 verified links

[![References](https://img.shields.io/badge/references-127-2F6EA5?style=flat-square)](resources/papers.md)
[![Areas](https://img.shields.io/badge/research%20areas-9-2F6EA5?style=flat-square)](resources/by-area/README.md)
[![Links](https://img.shields.io/badge/links-188%20verified-0FDC78?style=flat-square)](resources/README.md)
[![Code](https://img.shields.io/badge/public%20code-13-2F6EA5?style=flat-square)](resources/papers.md)
[![License](https://img.shields.io/badge/license-MIT-C4622D?style=flat-square)](LICENSE)

</div>

---

## What this is

Affective BCI turns a brain signal into something that **helps a person** — a
display that adjusts, a word that comes back, a stimulation that fires at the
right moment. Getting there is not one problem but a chain, and each link in
the chain breaks in its own way.

This repository is a map of that chain. Every reference is filed under the
**research area** it belongs to, with a note on what it settles and where it
falls short. The areas are the ones the survey itself is built from, so a
reader of the survey and a reader of this index use the same words.

<img src="assets/figures/sense_think_act.png" width="100%" alt="Sense, Think and Act: the closed loop from neural signal to user-facing action, with the gate that decides what reaches the user">

**Sense — Think — Act.** The signal becomes a belief, the belief becomes a
proposal, and something decides whether the proposal reaches the person. Most
systems in this field stop after the first step and report an accuracy; the
loop is where the hard problems live.

---

## Start here

<table>
<tr>
<td width="50%" valign="top">

**New to the field**

1. [Affective Targets & Corpora](resources/by-area/corpora.md) — why the label
   matters more than the signal
2. [Evaluation & Leakage Control](resources/by-area/evaluation.md) — the split
   decides the question your number answers
3. [Closed-Loop Systems](resources/by-area/closed-loop.md) — how a decoder
   becomes a system

</td>
<td width="50%" valign="top">

**Building a system**

4. [Generalization & Transfer](resources/by-area/generalization.md) — will it
   work on a person you have never seen
5. [Decoding Architectures](resources/by-area/architectures.md) — what to build
6. [Application Domains](resources/by-area/applications.md) — where it goes

</td>
</tr>
<tr>
<td valign="top">

**Reviewing work in this area**

- [Evaluation & Leakage Control](resources/by-area/evaluation.md) — leakage,
  spectral confounds, split protocols
- [Evidence Maturity](resources/by-area/maturity.md) — what a pilot study has to
  report before it counts
- [Governance & Ethics](resources/by-area/governance.md) — consent, retention,
  re-identification

</td>
<td valign="top">

**Working on the index**

The index is generated, so a pull request cannot change what it contains. Open
an issue instead, and say which area the reference belongs to.

- [Add a reference](.github/ISSUE_TEMPLATE/add-reference.yml)
- [Add a dataset](.github/ISSUE_TEMPLATE/add-dataset.yml)
- [Report a broken link](.github/ISSUE_TEMPLATE/broken-link.yml)

</td>
</tr>
</table>

---

## The research areas

Nine areas, in five tiers. The tiers are the order a reader meets them in:
what the recording is, how it becomes a prediction, whether the prediction can
be believed, what it is used for, and what has to be settled before any of it
runs.

<img src="assets/figures/taxonomy.png" width="100%" alt="Nine research areas in five tiers: Foundations (signal acquisition and quality, affective targets and corpora), Methods (decoding architectures, generalization and transfer), Validation (evaluation and leakage control, evidence maturity), Systems (closed-loop systems, application domains), and Boundaries (governance and ethics)">

| Tier | Research area | What it settles | Refs |
|:--|:--|:--|--:|
| **Foundations** | [Signal Acquisition & Quality](resources/by-area/signal.md) | What the recording measures, and how much of it can be trusted | 8 |
| | [Affective Targets & Corpora](resources/by-area/corpora.md) | Why a measurable proxy stands in for emotion, and what it then means | 33 |
| **Methods** | [Decoding Architectures](resources/by-area/architectures.md) | How a recording is organised, and which objective decides what the model keeps | 28 |
| | [Generalization & Transfer](resources/by-area/generalization.md) | The unit held out during testing states how far a result can travel | 36 |
| **Validation** | [Evaluation & Leakage Control](resources/by-area/evaluation.md) | A favourable split or repeated test-set access can beat a better architecture | 9 |
| | [Evidence Maturity](resources/by-area/maturity.md) | Lab estimates the state; Pilot changes something; Field holds up over time | 19 |
| **Systems** | [Closed-Loop Systems](resources/by-area/closed-loop.md) | Sense proposes, Act decides, a harness keeps the system inside what was tested | 19 |
| | [Application Domains](resources/by-area/applications.md) | Four families of system, and what each does with an estimate once it has it | 39 |
| **Boundaries** | [Governance & Ethics](resources/by-area/governance.md) | A neural recording reveals more than the purpose it was collected for | 7 |

The nine areas in one table: [research-area index](resources/by-area/README.md).

A reference is filed under every area it informs, so the counts above sum to
more than 127. The area it informs most often is its primary home.

---

## Four kinds of system

<img src="assets/figures/applications.png" width="100%" alt="Four families of affective BCI system: affect monitoring and assessment, neurofeedback and self-regulation, neuroadaptive interfaces, and responsive neuromodulation">

**Monitoring** estimates a state and stops there. **Neurofeedback** hands the
state back to the person to regulate. **Neuroadaptive** interfaces change the
environment to fit the person. **Responsive neuromodulation** changes the
person's brain state directly. The four are not interchangeable, and a result
from one does not transfer to another.

---

## Corpora and evidence

<img src="assets/figures/corpora_scale.png" width="100%" alt="Participants per corpus, log scale, grouped by how the target was elicited">

**Corpora.** Sixteen corpora, grouped by how the target was elicited — by the
experimenter, reported by the participant, or read from behaviour. The groups
are not interchangeable, and a number from one does not transfer to another.

<table>
<tr>
<td width="52%" valign="middle" align="center">

<img src="assets/figures/levels.png" width="500" alt="Lab, Pilot and Field: what each maturity level tests">

</td>
<td valign="middle">

**Maturity.** Lab tests the estimate. Pilot lets the estimate change something
during a limited experiment. Field uses the complete system repeatedly in the
setting it was built for. Most published work stops at the first.

The ladder runs one way: a Lab result does not become a Pilot result because
the method was reused, and a Pilot result does not become a Field result
because the evaluation was thorough.

</td>
</tr>
</table>

---

## What is here

| Path | What it holds |
|:--|:--|
| [`resources/by-area/`](resources/by-area/README.md) | The nine research-area pages — every reference, linked, with a note |
| [`resources/papers.md`](resources/papers.md) | All 127 references in one table |
| [`resources/papers.json`](resources/papers.json) | The same index as data, for filtering |
| [`resources/corpora.md`](resources/corpora.md) | All 16 corpora, with scale, modality, target and source |
| [`playbooks/`](playbooks/README.md) | Checklists for designing an evaluation, a loop, or a review |
| [`assets/figures/`](assets/figures) | Figures, exported at 200 dpi |
| [`scripts/`](scripts) | The generator, the figure builders, and the four checkers |

Every reference is one click away, and the links are verified in CI, so a dead
DOI fails the build rather than sitting in a table.

```
python scripts/check_index.py          # the index agrees with itself
python scripts/check_links.py          # verify every link
```

---

## Contributing

Additions welcome — a corpus, a method, a system, a critique that changes how
the field should be measured. See [CONTRIBUTING.md](CONTRIBUTING.md).

The pages under `resources/` are generated from the survey's own source, which
is not public, so a pull request cannot change them. Open an issue instead,
and say which area the reference belongs to.

---

<div align="center">

**If this map was useful, a star helps others find it.**

</div>
