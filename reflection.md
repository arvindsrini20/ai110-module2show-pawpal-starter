# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- The initial design that I want to go with has 4 classes. Owner is for the owner name of the pet and the amount of time they have available in a day. Pet is for the pet name/species and how it is associated with an owner. Task stores a title, duration, and priority level. The final class is Scheduler which takes a list of tasks and an available time budget to create a daily plan.


Owner — stores owner identity and the time constraint (total minutes available per day)
Pet — stores pet identity and links back to its owner
Task — the core data unit; describes what needs to be done, how long it takes, and how important it is
Scheduler — the planning engine; filters and orders tasks so that high-priority tasks are scheduled first and the plan fits within the owner's available time

**b. Design changes**

Yes, the design changed quite a bit once I started actually implementing things. The biggest shift was that in the original UML, the Scheduler held a list of tasks directly. But that didn't make sense once I realized that tasks belong to pets, not to the scheduler. So I moved the task list into Pet, gave Owner a method to collect all tasks across its pets, and had the Scheduler read from Owner instead. This made the data flow much cleaner — each class is responsible for its own data.

Task also grew a lot. It started with just title, duration, and priority, but I added frequency, completed, time_of_day, and due_date as the features expanded. ScheduledTask also gained a pet attribute once tasks could come from multiple pets and the output needed to show which pet each task belonged to.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: the owner's available time budget (in minutes) and each task's priority level (high, medium, or low). Time is the hard constraint — no task gets scheduled if it doesn't fit. Priority is the soft constraint that determines order. I decided time had to come first because there's no point ranking tasks if the plan can't actually be completed. Within the same priority level, I added duration as a tiebreaker so shorter tasks are scheduled first, which lets more tasks fit overall.

**b. Tradeoffs**

The conflict detection only flags tasks that share an exact `time_of_day` string (e.g., two tasks both set to `"07:00"`). It does not check for overlapping durations — so a 30-minute task at `07:00` and a 20-minute task at `07:15` would actually overlap in real life, but the system would not catch it.

This tradeoff is reasonable for this scenario because pet care tasks are rarely scheduled with minute-level precision. A pet owner thinks in rough time slots ("morning", "07:00"), not exact intervals. Implementing true duration-overlap detection would require tracking a running end time for each task and comparing ranges — adding complexity that isn't justified given how loosely these tasks are planned in practice. The simpler check catches the most common and obvious conflicts without overcomplicating the logic.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the whole project in different ways depending on the phase. Early on it was mostly brainstorming — figuring out what classes I needed, what attributes made sense, and how they should relate to each other. The UML design session was almost entirely a back-and-forth conversation where I'd describe what the app needed to do and the AI would suggest a structure, and I'd push back or refine it.

Once I had skeletons, I used AI to help implement methods — things like the lambda key for sort_by_time or the timedelta logic for recurring tasks. The most useful prompts were specific ones like "how should Scheduler retrieve all tasks from Owner's pets?" rather than vague ones like "write the scheduler." Specific questions got focused, usable answers.

**b. Judgment and verification**

The clearest example was the conflict detection method. AI suggested a more Pythonic version using `defaultdict` and `itertools.combinations` — shorter code, handles 3+ tasks at the same time more correctly. I understood what it did but decided to keep the explicit loop version instead. The Pythonic version buried the logic inside a nested list comprehension that would be hard for anyone reading it for the first time to follow. Since this is a course project that others will read, I valued clarity over cleverness. I verified my decision by tracing through both versions with a test case in my head before committing to the simpler one.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers 11 behaviors across five areas: basic task completion and task addition, chronological sort order and untimed tasks falling last, daily and weekly recurrence creating correct due dates and as-needed tasks not recurring, conflict detection flagging duplicate times without false positives, and edge cases like an owner with no pets and a task that exceeds the time budget. These tests mattered because they verify the behaviors that users depend on most — if recurrence is broken or the scheduler silently drops tasks instead of marking them skipped, the app becomes untrustworthy.

**b. Confidence**

I'd rate my confidence at 4 out of 5. The core behaviors are solid and all 11 tests pass cleanly. The gap is duration-overlap conflict detection — two tasks that overlap in real time but don't share an exact start time won't trigger a warning. I'd also want to test what happens when a pet has a mix of completed and pending tasks and make sure the scheduler only sees the pending ones consistently. Those are the edge cases I'd tackle next.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how cleanly the data flow ended up. Owner → Pet → Task is a natural hierarchy that made every other decision easier. Once that was settled, the Scheduler could stay focused on logic without needing to know anything about how tasks were stored. The test suite also came together well — having 11 tests that each test one specific thing made debugging straightforward.

**b. What you would improve**

If I had another iteration I'd add real duration-overlap conflict detection and an actual time-block view for the schedule — something that shows tasks laid out across a timeline instead of just a ranked list. I'd also add the ability to mark tasks complete directly in the Streamlit UI and watch the next occurrence appear automatically, which would make the recurring task feature feel real rather than just a backend detail.

**c. Key takeaway**

The most important thing I learned is that AI is a very fast collaborator but not a careful one. It will give you working code quickly, but it won't always give you the *right* code for your specific design. Being the lead architect meant constantly asking "does this fit the structure I've already built?" rather than just accepting whatever was generated. The moments where I pushed back — like keeping the readable loop over the clever list comprehension — were the moments where I actually understood my own system best.
