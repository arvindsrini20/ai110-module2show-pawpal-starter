# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- The initial design that I want to go with has 4 classes. Owner is for the owner name of the pet and the amount of time they have available in a day. Pet is for the pet name/species and how it is associated with an owner. Task stores a title, duration, and priority level. The final class is Scheduler which takes a list of tasks and an available time budget to create a daily plan.

 
Owner — stores owner identity and the time constraint (total minutes available per day)
Pet — stores pet identity and links back to its owner
Task — the core data unit; describes what needs to be done, how long it takes, and how important it is
Scheduler — the planning engine; filters and orders tasks so that high-priority tasks are scheduled first and the plan fits within the owner's available time

**b. Design changes**

- Did your design change during implementation?

Not for now.

- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The conflict detection only flags tasks that share an exact `time_of_day` string (e.g., two tasks both set to `"07:00"`). It does not check for overlapping durations — so a 30-minute task at `07:00` and a 20-minute task at `07:15` would actually overlap in real life, but the system would not catch it.

This tradeoff is reasonable for this scenario because pet care tasks are rarely scheduled with minute-level precision. A pet owner thinks in rough time slots ("morning", "07:00"), not exact intervals. Implementing true duration-overlap detection would require tracking a running end time for each task and comparing ranges — adding complexity that isn't justified given how loosely these tasks are planned in practice. The simpler check catches the most common and obvious conflicts without overcomplicating the logic.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
