# Evaluation Guide

This guide explains how to evaluate changes to `prompt-efficacy-scorer` without overfitting to a tiny set of example prompts.

## Goals

A good revision should improve at least one of these outcomes without harming the others:
- clearer diagnosis quality
- better preservation of user intent
- better optimized rewrites
- fewer unnecessary rewrites of already-good prompts
- stronger handling of structured agent prompts and memory boundaries

## Recommended Eval Categories

Maintain coverage across these categories:
- contradictory prompt
- high-quality prompt that should receive only light-touch edits
- underspecified prompt that needs structure, not just trimming
- verbose but necessary prompt that should not be over-compressed
- agent or system prompt with runtime memory, project-local memory, or shared-memory language
- prompt with strict output formatting for downstream automation, including a template with placeholders
- prompt that reads untrusted input (tickets, documents, PR content) or gives an agent tools
- prompt aimed at a named model from each vendor the skill has guidance for

## What To Look For

For each eval, check:
- Did the audit identify the real failure modes?
- Did the score roughly match the actual prompt quality?
- Did the rewrite preserve intent?
- Did the rewrite improve structure and execution reliability?
- Did the skill avoid inventing missing requirements?

## Failure Modes To Watch

- Over-shortening a prompt until important nuance is lost
- Rewriting the user's task into a different task
- Declaring a prompt weak without naming concrete contradictions or gaps
- Treating every prompt as if it needs a full rewrite
- Mixing memory scopes together in agent prompts

## Lightweight Regression Process

1. Run each prompt in `evals/evals.json` twice: once with the skill and once without it (or with the previous version of the skill).
2. Grade both outputs against the eval's `expectations`, and read the outputs side by side, not only the pass rates.
3. Add a new eval whenever you discover a new failure mode.
4. Keep the eval set small but varied; prefer representative edge cases over many near-duplicates.

## Writing Expectations That Measure Something

An expectation that both configurations pass doesn't tell you whether the skill helps. A strong model without the skill already finds most contradictions and missing context. The skill earns its keep on calibration, restraint, and honest accounting of changes, so aim expectations there:
- Make "light-touch" measurable, for example "no new mandatory output sections" or "the rewrite stays within about twice the original length, or explains why not".
- Check that added rules and defaults are labeled as assumptions, not presented as the user's own requirements.
- Check that the rewrite keeps every explicit user constraint, or names the one it changed and why.
- Split compound expectations, such as persistence versus sharing, so a partial pass is visible.

## Out Of Scope

This repository does not currently ship:
- an automated grader
- a tokenizer-backed measurement script
- model-vendor-specific benchmark suites

These can be added later if they clearly improve signal without bloating the repository.
