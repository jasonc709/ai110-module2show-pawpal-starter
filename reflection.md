# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Three core actions a user should be able to perform: Add a pet with basic details like name, species, and age, schedule care tasks such as feeding, walks, medication, or appointments, view today's tasks in time order so the owner knows what needs attention next.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design includes four main classes: Owner, Pet, Task, and Scheduler. The Owner class represents the person using the app and stores a list of pets. The Pet class stores basic pet information and a list of that pet's care tasks. The Task class represents one care activity, including its description, time, frequency, and priorty status. The Scheduler class organizes tasks across all pets so the app can show a clear schedule, sort tasks by time, and later detect conflicts.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I made the Scheduler read tasks from the Owner's pets instead of keeping its own separate list, so there's a single source of truth, and I added unique id fields plus a pet_name link on Task so tasks can be told apart and traced back to their pet.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
