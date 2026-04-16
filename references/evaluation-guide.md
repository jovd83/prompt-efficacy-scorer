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
- prompt with strict output formatting for downstream automation

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

1. Run the skill against the prompts in `evals/evals.json`.
2. Compare results against the expected output guidance in each eval.
3. Add a new eval whenever you discover a new failure mode.
4. Keep the eval set small but varied; prefer representative edge cases over many near-duplicates.

## Out Of Scope

This repository does not currently ship:
- an automated grader
- a tokenizer-backed measurement script
- model-vendor-specific benchmark suites

These can be added later if they clearly improve signal without bloating the repository.
