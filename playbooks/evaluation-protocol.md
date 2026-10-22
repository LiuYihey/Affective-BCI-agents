# Designing an evaluation

Run this before you report an accuracy. The purpose is not to make the number
larger — it is to make the number answer a question someone can act on.

---

## 1. Write down the claim first

Before touching a split, finish this sentence:

> On a recording I did not train on, from a person I did not train on, the
> model predicts **\_\_\_** with accuracy **\_\_\_**.

If you cannot fill in both blanks, the experiment has no claim yet, and any
number you produce will be ambiguous. The blank that matters most is the
first one: **what was held out** determines what your result generalises to.

| Held out | Result generalises to | Hardest realistic case |
|---|---|---|
| Nothing (train = test) | The recording you trained on | — |
| Windows within a session | That person, that session | Mild |
| Sessions within a person | That person, other days | Moderate |
| People | New people, same protocol | Hard |
| Datasets | New people, new protocol, new device | Hardest |

## 2. Split the right unit

**Checklist**

- [ ] The split unit is the **person**, not the window. Splitting windows
      leaks: adjacent windows from the same trial share signal and label.
- [ ] No window from a session appears in both train and test.
- [ ] If the corpus has multiple recordings per subject, **all** of them are
      in the same fold.
- [ ] The test set was touched **once**, after the model was frozen.
- [ ] If hyperparameters were tuned, the tuning used a **validation** split
      drawn from the training data only.

> Splitting by window rather than by subject is the most common way an
> otherwise sound model reports a number that does not survive contact with a
> new person. See
> [Evaluation & Leakage Control](../resources/by-area/evaluation.md) for the
> audits that measured how much this matters.

## 3. Check what else the model could be reading

A model can reach a good score without reading the variable you care about.

**Checklist**

- [ ] **Aperiodic background.** Run the model on the aperiodic component
      alone. If accuracy holds, the model learned the subject's baseline
      spectrum, not their emotion. In one audit of EEG and ECG foundation
      models, six of seven depended on the aperiodic component.
      ([source](https://doi.org/10.48550/arXiv.2606.08583))
- [ ] **Spectral confounds.** Emotion labels and frequency bands are not
      independent. Check whether band power alone predicts the label.
- [ ] **Site or device.** If subjects were recorded on different equipment,
      the model may be classifying hardware.
- [ ] **Label shortcuts.** If the label came from a stimulus the model can
      infer from the recording alone, that is the finding.

## 4. Say how much you can say

**Checklist**

- [ ] Report **per-person** performance alongside the pooled number, not just
      the pooled number.
- [ ] Report the **spread**, not only the mean.
- [ ] Report the number of people the score is based on.
- [ ] If the score uses target-side data, say so. A method that consumes a
      little of the new person's data is a different method from one that
      consumes none, and the scores are not comparable.
- [ ] If only a small amount of target-side data was used, report **how much**.
      The difference between a per-person model and a group model is often
      larger than the difference between two architectures.
      ([source](https://doi.org/10.48550/arXiv.2607.27655))

## 5. Explain it, if you claim it is explainable

A saliency map is not an explanation.

**Checklist**

- [ ] If you interpret the model, perturb the input and check the prediction
      moves. A saliency map that does not correspond to a perturbation that
      changes the output is decoration.
      ([source](https://doi.org/10.1038/s42256-019-0048-x))
- [ ] If the model is a decoder, a **channel or montage removal** test is a
      cheap check on whether it learned spatial relations or something else.
      ([source](https://doi.org/10.48550/arXiv.2606.15278))

---

## Common failure modes

| What was reported | What it actually shows |
|---|---|
| 95% accuracy, window-level split | The model can recognise the subject |
| 92% accuracy, selected on the test set | The model can recognise the test set |
| Per-person 71%, group 62% | Personalisation is worth ~9 points |
| Cross-dataset 55%, within-dataset 91% | The corpus, not the emotion, carried the signal |
| Accuracy with no variance across subjects | Something leaked |

---

## Related

- [Evaluation & Leakage Control](../resources/by-area/evaluation.md) — the
  references behind this checklist
- [Generalization & Transfer](../resources/by-area/generalization.md) — what the
  held-out unit decides
- [Reviewing a pilot system](maturity-ladder.md)
