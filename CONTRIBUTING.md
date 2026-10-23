# Contributing

Thanks for helping make this map more useful. Two things are welcome: a
reference that is missing, and a correction to one that is already here.

## Adding a reference

Open **[Add a reference](.github/ISSUE_TEMPLATE/add-reference.yml)** and fill
in the form. The one field that matters most is **why it is worth opening** —
a sentence on what the paper settles, or where it falls short. That sentence
is what makes this index useful rather than a list of titles.

## Adding a dataset

Open **[Add a dataset](.github/ISSUE_TEMPLATE/add-dataset.yml)**. Please state
how the target is obtained, because that is what determines which of the three
groups a corpus belongs to.

## Reporting a broken link

Open **[Broken link](.github/ISSUE_TEMPLATE/broken-link.yml)**. Links are
checked weekly and in CI, but a publisher can change a page without warning.

## Editing the pages directly

The pages under `resources/` are **generated**. Do not edit them by hand —
your change would be overwritten.

The prose pages (`README.md`, `playbooks/`) are written by hand, and those are
the ones worth editing directly. Any DOI or arXiv link in them must
correspond to a reference in the index, which `check_citations.py` enforces.

If you want to change what the index contains, open an issue instead. The
index is generated from the survey's own source, which is not public, so a
pull request cannot regenerate it:

```
python scripts/check_index.py         # the index agrees with itself
python scripts/check_citations.py      # prose citations match the index
python scripts/check_relative_links.py # relative paths point at real files
python scripts/check_links.py          # every link still resolves
python scripts/check_layout.py         # the pages follow the layout conventions
python scripts/check_voice.py          # reader-facing pages stay reader-facing
```

All six run in CI on every push, so a pull request that breaks any of them
fails the build rather than landing broken.

## Two audiences

The repository has two audiences, and a page belongs to one of them.

The **reader-facing** pages — `README.md`, `resources/`, `playbooks/` — are
read by people looking for a paper, a corpus, or a checklist. They talk about
the field. A line about how the repository is generated, which script checks
what, or how CI is wired belongs to this page instead, because it is addressed
to the people changing the repository rather than to the people reading it.

`check_voice.py` enforces the split. If a reader-facing page starts
describing the build, the check fails and the material moves here.

## Page layout

GitHub draws a rule under every second-level heading. A page that also puts a
`---` above the heading therefore shows two rules and reads as two separators,
so the convention here is to let the heading draw the rule and to use `---`
only between blocks of prose. `check_layout.py` enforces this.

Figures are followed by a centred caption in small text, so a reader can tell
what a figure is without reading the paragraph under it:

```
<p align="center"><sub><b>Title</b> — one clause on what the figure shows.</sub></p>
```

## Changing the taxonomy

The nine research areas and the five tiers they sit in are defined in
`scripts/build_resources.py`. Each area carries a title, a scope, the aspects
to look for, its tier, and one line stating what it settles. Changing any of
them means editing `AREAS` and `TIERS` there, then regenerating:

```
python scripts/build_resources.py          # the index and the area pages
python scripts/make_taxonomy_figure.py     # the figure in the README
```

The figure reads the same definitions and the same counts as the index, so
the two cannot drift apart silently. `check_index.py` then confirms that the
committed pages agree with the committed index, that the reference counts in
the hand-written tables are right, and that the "what it settles" wording in
the README is the wording the index defines.

## What earns a place here

The index is organised around nine research areas, grouped into five tiers.
A reference belongs here if it informs one of them.

References are included when they:

- report a method, corpus, or system in affective BCI;
- identify a failure mode in how such work is measured or deployed;
- survey a method, corpus, or system in the field.

References are not included merely because they use EEG, or because they
classify emotion from some other modality. If you think something belongs and
it is not here, open an issue and say which area it belongs to.

## Notes on tone

Notes describe what a reference **shows**, including where it falls short.
"This is the clearest example of how much target-side data changes the reported
score" is useful. "This is an excellent and innovative paper" is not.

## Code of conduct

Be straightforward and assume good faith. Reviews of other people's work should
focus on the work.
