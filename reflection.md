# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- The initial design that I want to go with has 4 classes. Owner is for the owner name of the pet and the amount of time they have available in a day. Pet is for the pet name/species and how it is associated with an owner. Task stores a title, duration, and priority level. The final class is Scheduler which takes a list of tasks and an available time budget to create a daily plan.


Owner - stores owner identity and the time constraint (total minutes available per day)
Pet - stores pet identity and links back to its owner
Task - the core data unit; describes what needs to be done, how long it takes, and how important it is
Scheduler - the planning engine; filters and orders tasks so that high-priority tasks are scheduled first and the plan fits within the owner's available time

**b. Design changes**

Yes, the design changed during implementation. The biggest shift was moving tasks out of the Scheduler and into Pet instead, since tasks logically belong to a pet. Owner then got a method to collect all tasks across its pets, and the Scheduler just reads from there. Task also grew new fields like frequency, completed, and time_of_day as features got added. ScheduledTask gained a pet attribute once multiple pets were involved.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler uses two constraints: the owner's available time budget and each task's priority. Time is the hard limit - nothing gets scheduled if it doesn't fit. Priority decides the order. I added duration as a tiebreaker within the same priority level so shorter tasks get scheduled first, fitting more into the day overall.

**b. Tradeoffs**

Conflict detection only flags tasks that share the exact same time_of_day string. It won't catch two tasks that overlap in duration but start at different times. That felt like a reasonable tradeoff because pet owners don't usually schedule with minute-level precision, and adding full duration-overlap logic would complicate things more than it's worth for this use case.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across every phase but in different ways. Early on it helped with brainstorming the class structure and relationships. Later I used it to implement specific methods like the sorting lambda and timedelta logic for recurring tasks. The most useful prompts were specific ones like "how should Scheduler retrieve tasks from Owner's pets?" - vague prompts gave less useful answers.

**b. Judgment and verification**

The clearest example was conflict detection. AI suggested a version using defaultdict and itertools.combinations which was shorter and technically more correct for 3+ conflicts. I understood it but kept my explicit loop instead because the Pythonic version was hard to read at a glance. Since other people will read this code, I chose clarity over cleverness and verified my choice by tracing through both versions manually.

---

## 4. Testing and Verification

**a. What you tested**

The suite covers 11 behaviors: task completion, task addition, sort order, untimed tasks falling last, daily and weekly recurrence, as-needed tasks not recurring, conflict detection with and without duplicates, an empty owner plan, and a task getting skipped for exceeding the time budget. These were important because they cover the behaviors users depend on most directly.

**b. Confidence**

I'd say 4 out of 5. The core logic is solid and all 11 tests pass. The main gap is duration-overlap conflicts and I'd also want more tests around mixed completed and pending tasks to make sure the scheduler always filters correctly.

---

## 5. Reflection

**a. What went well**

The data flow ended up really clean. Owner, Pet, and Task form a natural hierarchy and once that was locked in, every other decision got easier. The test suite also came together well since each test covers exactly one behavior.

**b. What you would improve**

I'd add real duration-overlap conflict detection and a timeline view so the schedule feels more visual. I'd also wire up task completion in the Streamlit UI so the recurring logic is actually visible to the user.

**c. Key takeaway**

AI moves fast but it isn't careful. It generates working code quickly but not always the right code for your specific design. Being the lead architect meant constantly asking whether a suggestion actually fit what I'd already built, and the moments I pushed back were the moments I understood my own system best.
