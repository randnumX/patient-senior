---
name: quiz
description: >
  Run an interactive quiz in chat - multiple-choice and write-the-command
  recall questions - on this session's work, a flashcard deck or a topic, one
  question at a time, with explanations and a score. Use for /quiz, /quiz
  <topic|deck>, "test me", "quiz me on what we did".
argument-hint: "[session | topic | deck name] [number of questions, default 5]"
---

# /quiz

1. **Pick the material.** Default: what was taught or run in this session. Otherwise a topic, or a deck in
   `<hub>/Flashcards/` (read the deck note). Default 5 questions.
2. **Mix the question types:**
   - multiple choice (4 options, plausible wrong answers based on real misconceptions);
   - **write the command** - "How would you ... ?" - the user types it from memory (this is the most
     valuable kind; include at least two when commands were involved);
   - **predict the output** - show a command or code snippet, ask what happens;
   - **why** - one-sentence explanations.
3. **Ask one question at a time** and wait for the answer. Never reveal the answer in the same message as
   the question.
4. **Respond like a patient senior:** correct - say why it is right and add one deeper detail; partly right
   - credit the right part, fix the rest; wrong - explain the misconception, then the right answer with a
   breakdown. For command answers, compare token by token and accept equivalent variations.
5. **Finish with a score and next steps:** list missed items, make sure each has a flashcard (load the
   `flashcards` skill), and offer to save a side quest for any gap that needs real study. A command answered
   correctly here counts toward mastery in `<hub>/Profile.md` (two correct recalls = known).
