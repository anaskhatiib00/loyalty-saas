# Frontend Architecture Guide

This document defines the frontend architecture rules for the Loyalty SaaS project.

The goal is to keep the codebase scalable, easy to understand, easy to maintain, and ready for multiple developers.


## 1. Core Frontend Principles

The frontend is built as a commercial SaaS application, not a demo or tutorial project.

Every frontend decision should support:

- Thousands of businesses
- Multiple countries
- Multiple locations
- Many employees per business
- Different user roles
- Long-term maintainability
- Fast onboarding for future developers

The frontend should be:

- Clean
- Responsive
- Modular
- Reusable
- Easy to understand
- Easy to extend
- Safe to refactor

We prefer small, focused modules over large files that mix UI, state, API calls, and business logic.

## 2. Feature-First Architecture

The frontend is organized by business capabilities rather than by technical file types.

Each feature owns everything it needs.

Example:

```text
features/
│
├── customers/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── CustomerOperations/
│   ├── CustomerDigitalCard/
│   ├── CustomerTimeline/
│   ├── CustomerRewards/
│   └── ...
│
├── employees/
│
├── wallets/
│
├── rewards/
│
├── analytics/
│
└── subscriptions/
```

Avoid creating large generic folders where unrelated components accumulate.

Instead, each business capability should be isolated into its own module.


## 3. Standard Module Structure

Every business capability should follow the same internal structure.

Example:

```text
CustomerOperations/
│
├── components/
├── hooks/
├── services/
├── utils/
├── types/
│
├── CustomerOperations.tsx
│
└── index.ts
```

### Responsibilities

**components/**

Contains small UI components.

Examples:

- ProgramOverview
- PrimaryAction
- ActivityCorrections
- ManualTools

Components should focus only on rendering.

---

**hooks/**

Contains feature-specific hooks.

Examples:

- useCustomerOperations
- useCustomerRewards
- useCustomerTimeline

Hooks coordinate:

- state
- validation
- API calls
- mutations
- derived values

---

**services/**

Contains feature-specific business helpers.

Examples:

- buildRewardMessage()
- createCorrectionPayload()
- calculateRewardStatus()

These should never render UI.

---

**utils/**

Contains generic helper functions.

Examples:

- formatCardNumber()
- calculatePercentage()
- groupActivitiesByDay()

Utilities should be pure functions.

---

**types/**

Contains feature-specific TypeScript types.

Examples:

- ProgramOverviewModel
- CustomerOperation
- RewardStatus

Avoid declaring large interfaces directly inside React components.

---

**Feature Component**

Example:

CustomerOperations.tsx

Acts as the orchestrator.

Its responsibilities:

- compose child components
- connect hooks
- pass props
- define layout

It should contain very little business logic.

---

**index.ts**

Defines the public API of the module.

Other features should import from index.ts instead of deep file paths.


## 4. Component Responsibilities

Every React component must have a clear responsibility.

### Page Components

Located inside:

app/

Responsibilities:

- Route entry point
- Read route params
- Compose feature modules

Pages should contain almost no business logic.

---

### Feature Components

Examples:

- CustomerOperations
- CustomerDigitalCard
- CustomerTimeline

Responsibilities:

- Arrange the feature layout
- Connect hooks
- Pass data to child components

Feature components should avoid direct API calls whenever possible.

---

### Presentation Components

Examples:

- ProgramOverview
- PrimaryAction
- RewardCard
- TimelineItem

Responsibilities:

- Display data
- Emit user events

Presentation components should:

- avoid API calls
- avoid business logic
- avoid complex calculations

They should be reusable.

---

### Dialog Components

Examples:

- EditCustomerDialog
- CreateRewardDialog

Responsibilities:

- Display forms
- Collect user input
- Delegate submission to hooks

Dialogs should not contain business rules.

---

### Shared Components

Located inside:

src/components/

Examples:

- Button
- Card
- Badge
- EmptyState

These should remain generic.

Never place business-specific logic inside shared components.


## 5. Engineering Principles

These principles guide every frontend decision.

---

### 1. Product First

Always solve the business problem before writing code.

Ask:

- What is the shop owner trying to accomplish?
- What is the employee trying to accomplish?
- What is the customer trying to accomplish?

The workflow should always be more important than the implementation.

---

### 2. Simplicity Wins

The best interface is the one that requires the fewest decisions.

Avoid unnecessary buttons.

Avoid unnecessary dialogs.

Avoid unnecessary configuration.

If a workflow can be completed with one click instead of three, prefer one click.

---

### 3. One Responsibility

Every file should have one clear responsibility.

Examples:

✓ Display a reward.

✓ Manage customer operations.

✓ Format loyalty progress.

Avoid files that perform many unrelated tasks.

---

### 4. Reuse Before Rebuild

Before creating a new component, ask:

Can an existing component be reused?

Prefer composition over duplication.

---

### 5. Build for Growth

Every feature should assume that the application will grow.

Design components that can evolve naturally instead of requiring complete rewrites.

---

### 6. Consistency

Follow the established architecture.

Do not invent new patterns unless the existing architecture can no longer support the feature.

Consistency is more valuable than cleverness.

---

### 7. Safe Refactoring

Large refactors should happen incrementally.

Prefer replacing old implementations gradually instead of rewriting everything at once.

---

### 8. Commercial Quality

Every screen should feel production-ready.

Every workflow should feel polished.

Every interaction should inspire confidence.

We are building software that businesses will pay to use every day.