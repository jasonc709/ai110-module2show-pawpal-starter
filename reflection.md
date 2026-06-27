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
My scheduler mainly considers task time, pet ownership, completion status, frequency, and basic conflicts. I prioritized time first because pet owners need to know what task comes next during the day. I also prioritized pet name and completion status because those filters make the schedule easier to read when there are multiple pets or many tasks. Conflict detection matters because two tasks at the same exact time could be hard for one owner to handle.



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff my scheduler makes is that conflict detection only checks for exact matching start times. For example, it catches two tasks both scheduled at 08:00, but it does not catch an 08:00 task that lasts 30 minutes overlapping with an 08:15 task. This is reasonable for this project because it keeps the logic lightweight and easy to understand while still warning the user about the clearest scheduling conflicts.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI for edge cases really frequently. In the lecture I learned that AI tend to opt for the happy path so I made sure to ask the AI about potential edge cases the code could encounter and asked it to write tests for me.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I didnt accept the AIs suggestion when I wanted to write a data class instead of a regular class for one of my classes since I wasnt sure what a data class was yet. I searched it up and learned that a data class is a class that primarily stores data and doesn't perform general tasks.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested that the generated schedule didn't include the low priority task when the owner doesn't have enough time. This ensures that there's a purpose for the priority filter and the owners preferences otherwise these features would just be there for show.
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I'm pretty confident my scheduler works correctly since I understand almost every changes the AI made. I would test that filter works even when animals have the same name by filtering the ID.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm happy with how the scheduler became more than a basic task list. It can sort tasks, filter them, detect conflicts, handle recurring tasks, and use the owner's available hours to decide what fits into the schedule. I also like that the Streamlit UI shows useful feedback with success messages, warning boxes, and tables.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would improve the conflict detection logic. Right now it mainly checks for tasks that start at the exact same time. I would redesign it to check for overlapping task durations, such as an 8:00 task lasting 30 minutes conflicting with an 8:15 task.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned is that AI is helpful for generating code quickly, but I still need to act as the lead architect. I had to decide which suggestions made sense, keep the design simple, and make sure the code, UML, README, tests, and reflection all matched the actual project.