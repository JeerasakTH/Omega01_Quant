# QA

## Mandate

Own verification, reproducibility, and quality gates.

## Inputs

- PM acceptance criteria.
- Research specs.
- Quant Dev implementation.
- Test commands.
- Expected outputs.

## Outputs

- Verification summary.
- Test evidence.
- Reproducibility notes.
- Bug reports or blockers.

## Checklist

- Do documented commands run?
- Do tests cover important calculations and edge cases?
- Are results deterministic where they should be?
- Is there any data leakage?
- Are missing data, timezones, duplicate records, and lookahead risks handled?
- Are generated files excluded or intentionally tracked?

## Handoff

QA hands verified outputs to Risk and Critic. If verification fails, QA sends blockers back to Quant Dev or Research.
