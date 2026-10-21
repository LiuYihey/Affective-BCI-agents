# Designing a closed loop

A decoder that produces an estimate is not a system. A system has to decide
what to do with the estimate, and — this is the part that is usually missing —
what to do when the estimate is wrong.

<img src="../assets/figures/sense_think_act.png" width="100%" alt="Sense, Think and Act: the closed loop from neural signal to user-facing action, with the gate that decides what reaches the user">

---

## Sense, Think, Act

| Stage | What it does | What goes wrong here |
|---|---|---|
| **Sense** | Turns the recording into a belief about the user's state | The belief is overconfident, or the signal is an artefact |
| **Think** | Turns the belief into a proposal about what to do | The proposal assumes the belief is right, and has no way to say so |
| **Act** | Decides whether the proposal reaches the user | No gate: a wrong estimate reaches the user directly |

Most published systems stop after Sense and report an accuracy. The interesting
failures live in Act.

## The gate

The gate is the component that stands between a proposal and the user. It
answers: *under what conditions is this proposal safe to act on?*

**Checklist**

- [ ] The gate has an **explicit condition**, not just a threshold. "Only act
      when the estimate is confident *and* the signal quality is acceptable"
      is a condition. "Only act when confidence > 0.7" is a threshold, and
      thresholds fail differently.
- [ ] The gate has a **fallback**. What does the system do when the condition
      is not met? Silence, a neutral default, or a request for the user.
- [ ] The gate's condition is **checked on data that was not used to set it**.
- [ ] The gate has a **rate limit**. A gate that fires on 40% of trials is not
      a gate.
- [ ] Failing to act is treated as a legitimate outcome, and is reported as
      such.

> A system whose only lever is the output has no fallback. When the estimate
> goes wrong, the user receives it.

## Contingency

If the output depends on the signal, then a change in the signal produces a
change in the output. That is **contingency**, and it is the only reason a
neurofeedback result can be attributed to the signal rather than to practice,
expectation, or time.

**Checklist**

- [ ] There is a **yoked control**: the same feedback is delivered, but
      uncorrelated with the participant's own signal.
- [ ] There is a **no-feedback control**: the participant does the same task
      without the display.
- [ ] The task requires the participant to **attend** to the signal, or the
      effect may be a general practice effect.
- [ ] The reported effect is not explained by the participant learning to
      produce the desired state without the signal.

> Contingency is what separates a neurofeedback effect from a practice effect,
> and a yoked control is what demonstrates it. Without both, the result is
> consistent with the participant having learned the task.
> ([source](https://doi.org/10.1038/nrn.2016.164))

## The harness

An adaptive system that changes what it does based on a person's state can
leave the range in which it was tested. The harness is the envelope that keeps
it inside.

**Checklist**

- [ ] The harness restricts the system to the **envelope** it was validated in
      — the range of states, intensities, and timescales it was tested on.
- [ ] When the estimate leaves the envelope, the system **degrades or stops**,
      and says so.
- [ ] The system **keeps state** across interactions, and that state is
      inspected and revocable.
- [ ] Tool use and external calls are **bounded** — the system cannot take an
      action that was not authorised in advance.
- [ ] A human remains in the loop at the point where the action has
      consequences for the person.

> The harness literature from agent systems is the closest existing body of
> work on this problem, and it has not been applied to affective BCI.
> ([source](https://doi.org/10.13140/RG.2.2.31393.57447))

## When the loop changes the data

A closed loop makes the recording non-stationary in a way an offline dataset
is not: the user's behaviour changes because of the system, so the next
recording is drawn from a different distribution than the last.

**Checklist**

- [ ] You report whether the **action affected the next signal**, rather than
      assuming a fixed pipeline.
- [ ] The system's response is **not** conditioned on information the person
      did not consent to provide.
- [ ] Any state the system retains is **bounded in time** and inspectable.

## Reporting a closed-loop system

**Checklist**

- [ ] Report **latency** end to end, from signal to the user seeing an
      effect.
- [ ] Report the **gate's firing rate**, and how often it blocked.
- [ ] Report the **contingency** controls you ran.
- [ ] Report the **outcome** for the person, not only the intermediate
      accuracy. A system that improves an accuracy and does not help anyone is
      a measurement, not a system.

---

## Related

- [How do I wire a decoder into a loop that stays safe?](../resources/by-question/closed-loop.md)
- [Can I run this in real time?](../resources/by-question/deployment.md)
- [Reviewing a pilot system](maturity-ladder.md)
