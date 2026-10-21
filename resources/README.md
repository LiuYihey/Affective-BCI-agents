# Resource index

127 references from the affective BCI literature, every one linked. Organised by
the question a reference answers rather than by the order of a paper.

**188 links, all verified.** The link checker runs in CI, so a dead DOI fails
the build instead of sitting in a table.

---

## The eight questions

Each page carries a note per reference on **what it settles**, and where it
falls short.

| | Question | References | Strongest on |
|---|---|---:|---|
| 1 | [Which corpus should I use?](by-question/datasets.md) | 28 | Target definition, annotation cost |
| 2 | [How do I turn a recording into a prediction?](by-question/model.md) | 28 | Architectures, self-supervised pre-training |
| 3 | [Will it work on a person I have never seen?](by-question/transfer.md) | 36 | Domain generalisation, personalisation |
| 4 | [Is that accuracy real?](by-question/evaluation.md) | 21 | Leakage, spectral confounds, split protocols |
| 5 | [How do I wire a decoder into a loop that stays safe?](by-question/closed-loop.md) | 28 | Action gating, agent harnesses, contingency |
| 6 | [Can I run this in real time?](by-question/deployment.md) | 26 | Latency, monitoring, responsive stimulation |
| 7 | [How strong is the evidence?](by-question/maturity.md) | 19 | Lab / Pilot / Field, missing controls |
| 8 | [Where is the boundary?](by-question/governance.md) | 7 | Consent scope, re-identification, retention |

A reference appears under every question it informs, so the counts sum to more
than 127.

---

## Other views

- **[All 127 in one table](papers.md)** — alphabetical, with venue and links
- **[papers.json](papers.json)** — the same index as data. Filter by cluster,
  year, venue, whether code is available, or whether the paper supports a
  Lab / Pilot / Field claim.

```python
import json

data = json.load(open("resources/papers.json", encoding="utf-8"))

# Everything with public code
with_code = [p for p in data["papers"] if p["code"]]

# Everything filed under the evaluation question
eval_papers = [p for p in data["papers"] if "evaluation" in p["clusters"]]

# Papers that support a Field-level claim
field = [p for p in data["papers"] if "Field" in p["levels"]]
```

---

## Corpora

**[All 16 corpora, with scale, modality, target and source](corpora.md)** — grouped
by how the target was elicited: by the experimenter, reported by the
participant, or read from behaviour. The grouping matters more than the size,
because a number from one group does not transfer to another.

<img src="../assets/figures/corpora_scale.png" width="100%" alt="Participants per corpus, log scale, grouped by how the target was elicited">

---

## Regenerating

```
python scripts/check_index.py          # the index agrees with itself
python scripts/check_links.py          # verify every link resolves
python scripts/check_citations.py      # verify prose citations match the index
python scripts/check_relative_links.py # verify relative paths point at real files
```

The index is generated, not hand-written. Edit the generator, not the output.

---

## Related

- [Playbooks](../playbooks/README.md) — checklists for running an evaluation,
  designing a loop, or reviewing a pilot system
- [Contributing](../CONTRIBUTING.md)
