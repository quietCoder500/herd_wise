# Herd Wise MVP Plan for a Beginner Solo Developer

## Goal

Turn this Django prototype into a usable MVP in the next 24 days.

This version is intentionally realistic for a beginner working alone. The goal is not to build everything. The goal is to build a small, working, dependable product that proves the idea.

## What the MVP should include

The MVP should focus on only these core features:
- user signup and login,
- one farm per user or a simple farm ownership model,
- create and view animals,
- create and view animal groups,
- create and use at least one record template,
- create and view livestock records,
- a simple portal UI that works without major bugs,
- a deployment setup that can be shown to others.

## What is intentionally out of scope for this MVP

Do not spend time on these yet:
- advanced permissions,
- many user roles,
- rich analytics,
- complex reporting,
- fancy automation,
- polished enterprise UI,
- lots of custom styling,
- perfect testing coverage.

---

## Rule for the next 24 days

Work in small chunks. Finish one thing before starting the next.

If a task feels too big, break it into a 30-minute or 1-hour version.

---

## Phase 1 — Lock the Scope (Days 1–2)

### Objective
Make the MVP tiny and clear.

### Tasks
- [x] Write a short MVP description in plain English.
- [x] Decide the exact features that must exist by launch.
- [ ] Decide the exact features that can wait.
- [x] Write 3 user stories:
  - [x] As a farmer, I can sign up and log in.
  - [x] As a farmer, I can create and view animals.
  - [x] As a farmer, I can create a record and see it later.
- [x] Make a simple checklist of what “done” means.

### Done when
- You can explain the app in one paragraph.
- You know exactly what to build first.

---

## Phase 2 — Get the App Running Cleanly (Days 3–4)

### Objective
Create a stable local baseline.

### Tasks
- [x] Install dependencies.
- [x] Run the project locally.
- [x] Fix any current errors before building new features.
- [x] Make sure migrations run.
- [ ] Make sure the admin panel and login flow work.
- [x] Create a simple local setup note for yourself.

### Done when
- The project runs locally without mystery errors.
- You can log in and see the app.

---

## Phase 3 — Build the Core Data Flow (Days 5–8)

### Objective
Make the main business objects usable.

### Tasks
- [ ] Review the current farm, animal group, animal, template, and record models.
- [ ] Make sure the models can be created through the admin or forms.
- [ ] Create basic forms for:
  - [ ] farm creation,
  - [ ] animal group creation,
  - [ ] animal creation.
- [ ] Confirm records can be created and stored.
- [ ] Make sure the data is visible in simple pages.

### Done when
- You can create a farm, an animal group, and an animal.
- You can create a record and see it again.

---

## Phase 4 — Add Basic Permissions (Days 9–10)

### Objective
Keep the app safe without overcomplicating it.

### Tasks
- [ ] Make sure only logged-in users can access the portal.
- [ ] Make sure users only see their own farm data.
- [ ] Add simple access checks to all portal views.
- [ ] Avoid building a complicated multi-role system for now.

### Done when
- A logged-out user cannot access the main portal.
- A user cannot easily see another user’s data.

---

## Phase 5 — Build the Minimum Portal UI (Days 11–14)

### Objective
Create a usable interface for the MVP.

### Tasks
- [ ] Create a simple dashboard for logged-in users.
- [ ] Add links to:
  - [ ] farms,
  - [ ] animals,
  - [ ] templates,
  - [ ] records.
- [ ] Replace any obvious placeholder text.
- [ ] Make the pages readable and not broken.
- [ ] Add a simple search bar if time allows.
- [ ] Keep styling simple and consistent.

### Done when
- A user can navigate the app without getting lost.
- The interface feels like a real product, even if it is simple.

---

## Phase 6 — Finish Record Templates (Days 15–17)

### Objective
Make the record system actually useful.

### Tasks
- [ ] Finish the record template creation flow.
- [ ] Save one working template to the database.
- [ ] Make sure a record can be created from that template.
- [ ] Make sure the saved record is readable later.
- [ ] Keep the number of field types small.

### Done when
- One template can be created and one record can be created from it.

---

## Phase 7 — Add Basic Testing and Bug Fixing (Days 18–20)

### Objective
Reduce the chance of embarrassing bugs.

### Tasks
- [ ] Write a few simple tests for the most important flows.
- [ ] Test signup/login.
- [ ] Test creating an animal.
- [ ] Test creating a record.
- [ ] Fix any broken behavior discovered during testing.

### Done when
- The main user journey works without obvious failures.

---

## Phase 8 — Prepare for Demo/Submission (Days 21–24)

### Objective
Make the project presentable and understandable.

### Tasks
- [ ] Make sure the README is clear.
- [ ] Write a short “How to run this project” section.
- [ ] Make sure the app can be started with one command if possible.
- [ ] Clean up obvious broken or unfinished pages.
- [ ] Remove placeholder comments and confusing code.
- [ ] Prepare a short demo script:
  - [ ] sign up,
  - [ ] create a farm,
  - [ ] create an animal,
  - [ ] create a record.
- [] Take screenshots or notes for presentation.
- [ ] Deploy if possible, or prepare a local demo version.

### Done when
- You can show the app end to end in a short demo.
- The project feels complete enough for submission.

---

## Daily Working Strategy

### Every work session should include:
- [ ] one small goal,
- [ ] one concrete task,
- [ ] one stop point.

### Good daily targets
- [ ] fix one bug,
- [ ] finish one form,
- [ ] add one page,
- [ ] connect one model to a view,
- [ ] write one test.

### Avoid this
- [ ] trying to redesign the whole app,
- [ ] adding features that are not in the MVP,
- [ ] rewriting everything because it feels messy.

---

## Suggested Weekly Rhythm

### Week 1
- focus on getting the app running,
- build the core models and forms,
- create the main user flow.

### Week 2
- finish the portal UI,
- finish record templates,
- add basic testing and bug fixing.

### Week 3
- clean up the app,
- prepare the demo,
- make the project understandable.

---

## Important Advice for You

Because you are a beginner, working alone, and on a deadline, the best approach is:

1. build the simplest version that works,
2. avoid scope creep,
3. finish visible features before polishing,
4. keep the code understandable,
5. focus on the core user journey.

A simple, working MVP is better than a half-finished ambitious app.

---

## Minimum Success Criteria

You should consider this project successful if by the end of 24 days you can show:
- a working signup/login flow,
- a farm and animal management flow,
- a record template and record creation flow,
- a portal page that feels usable,
- and a project that can be run locally or deployed simply.
- [ ] Prepare onboarding instructions for users.
- [ ] Create a short support or bug-report process.
- [ ] Launch to a small group of users.
- [ ] Collect feedback and prioritize fixes.

### Done when
- The MVP is live and usable by real users.
- You have a clear list of improvements to build next.

---

## Recommended Execution Order

If you want the simplest path and are prone to procrastinating, follow this exact order:

1. Lock MVP scope.
2. Fix the app so it runs locally.
3. Implement farm and user access control.
4. Build the basic CRUD flows for farms, animals, and records.
5. Make the portal usable.
6. Add tests.
7. Prepare deployment.
8. Launch.

Do not try to build every feature at once.

---

## Weekly Milestones

### Week 1
- MVP scope locked
- local environment stable
- core models and admin reviewed

### Week 2
- farm and user access control implemented
- core CRUD flows working

### Week 3
- portal UI improved
- search and navigation usable

### Week 4
- tests added
- deployment configuration ready

### Week 5
- launch readiness review
- soft launch or staging deployment

---

## Definition of Done for the MVP

The MVP is ready when all of the following are true:
- A user can sign up and log in.
- A user can create and manage a farm.
- A user can manage animals and animal groups.
- A user can create and use record templates.
- A user can create and view livestock records.
- The app is secure by farm and user permissions.
- The UI is usable and not full of placeholders.
- The app can be deployed safely in a production environment.
- The main user journey is covered by tests.

---

## Final Advice

The biggest risk is trying to build too much too early. Keep the MVP narrow, finish each phase completely, and move forward one step at a time.

If you want, the next step can be to turn this into a day-by-day implementation checklist with concrete coding tasks for the next 2 weeks.
