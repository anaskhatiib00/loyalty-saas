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


## 4. Split by Responsibility, Not by Line Count

File size is a signal, not a rule.

Do not split a file simply because it exceeds an arbitrary number of lines.

Split a file when doing so improves:

- responsibility
- readability
- reuse
- testability
- maintainability

A 200-line file with one clear responsibility can be healthier than five small files with unclear boundaries.

Examples:

A database model may be long because it defines columns, constraints, indexes, and relationships. That is still one responsibility.

A transaction executor may be longer because several steps must succeed or fail within the same database transaction. Splitting those steps carelessly may weaken transaction safety.

A UI component should usually remain smaller because presentation responsibilities are easier to isolate and compose.

Use line count as a reason to review a file, not as an automatic reason to refactor it.

Refactor when a file begins to:

- handle unrelated business workflows
- mix presentation with API or business logic
- contain branches that belong to separate domain strategies
- become difficult to test independently
- hide the main workflow
- create unclear transaction ownership

Optimize for clear ownership, not the smallest possible files.