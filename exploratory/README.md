# Exploratory checks

This directory is the **exploratory tier**: small scripts and their verbatim
output that were written to settle a point in a review conversation, and then
reproduced by a second party on the same implementation. Each subdirectory
names the issue that produced it and contains the script plus its `output.txt`.

What an exploratory artifact is:

- reproduced on the same implementation at a named commit, so the numbers are
  checkable;
- scoped to the ring size, seed, and conventions stated in the script docstring;
- archived so a later protocol can say "this example is reproduction" rather
  than presenting it as a new prediction.

What it is not:

- a frozen protocol (no preregistered prediction, no protocol commit before
  evaluation);
- a result. Do not cite an exploratory artifact as evidence in a research note,
  the Program pages, the knowledge base, or the main site. A research note may
  reference one as the origin of a question, labeled `exploratory`;
- a repo-wide check. These scripts are not run by CI unless a workflow says so.

To promote an exploratory finding, write a frozen protocol under
`docs/research/protocols/`, commit the implementation before evaluation, and
register the result following `docs/research/README.md`. The exploratory
artifact stays here unchanged as the record of where the question came from.
