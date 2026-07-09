# Loyalty SaaS Engineering Principles

This document defines how we think when building the Loyalty SaaS.

Technology changes.

Frameworks change.

Libraries change.

Engineering principles should remain stable.

Every architectural decision, UX decision, and implementation should align with these principles.

The goal is not simply to build software.

The goal is to build software that businesses enjoy using every day and that engineers enjoy maintaining for years.


## 1. We Build Workflows, Not Pages

Users do not think in pages.

They think in tasks.

Examples:

A coffee shop employee wants to scan a customer.

A manager wants to correct an accidental scan.

A customer wants to know how close they are to a free reward.

The software should be organized around these workflows rather than around CRUD operations or individual screens.

Every new feature should answer one question first:

"What workflow are we improving?"


## 2. Product Before Code

Before writing code, understand the business problem.

Never build a feature simply because it is technically interesting.

Ask:

- Who uses this?
- Why do they need it?
- Can the workflow be simplified?
- Is there a faster way?

Great products come from solving problems, not from writing more code.


## 3. The Best UI Requires the Least Thinking

Every additional decision slows the user down.

Prefer:

One obvious button.

One obvious workflow.

One obvious next step.

The software should guide users naturally.

If users need instructions for a common task, the design should be improved.


Every line of code should make the product easier to use, easier to maintain, or easier to grow. If it does none of those things, question whether it belongs.