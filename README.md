# Shift Brief AI CLI

## Overview

In this lab, you will build a Python CLI prototype that uses a reusable AI client to create and revise shift handoff briefs from messy shift notes.

The goal is not only to get an AI response. The goal is to organize your application so each part has a clear responsibility:

- The AI client handles AI service communication.
- The brief builder handles shift-specific prompt construction and response checks.
- The CLI handles commands, user input, and displayed messages.

This lab asks you to apply the same service-integration and reusable-client concepts from the module to a new workplace problem. You will use tests to guide your development and verify that your application is organized, reusable, and reliable.

---

## Scenario

You are a junior Python developer on an internal tools team for a company with several retail locations.

At the end of each day, store leads write shift notes that may be messy, incomplete, or inconsistent. These notes may mention staffing issues, inventory concerns, customer incidents, equipment problems, safety concerns, or tasks that need follow-up.

Example shift notes:

```txt
Register 2 froze twice during closing. Maya restarted it, but it may need IT review tomorrow. Stockroom still has three carts of unsorted returns.
```

Managers want a CLI prototype that turns these notes into a structured shift handoff brief.

The brief should include:

```txt
Shift Summary:
Open Issues:
Action Items:
Follow-Up Questions:
Risk Notes:
```

The application should also support revisions. After receiving a brief, a manager may type feedback such as:

```txt
revise Make the action items more specific and include who should review Register 2.
```

The application should use conversation history in the AI client so the revision can build from the previous brief.

This is a local prototype. You are not building a database, web app, deployed backend, RAG system, or production automation system. Your focus is on clean Python structure, reusable AI service logic, command handling, and reliable response handling.

---

## Learning Goals

By completing this lab, you will:

- Implement a reusable AI client class using OOP principles.
- Separate AI service logic from CLI workflow logic.
- Build domain-specific prompts outside the reusable AI client.
- Validate user input before sending prompts to an AI service.
- Manage conversation history for create-and-revise workflows.
- Handle failed or unusable AI service responses.
- Use tests to verify functionality, edge cases, and architecture decisions.

---

## Project Structure

Your repository contains this structure:

```txt
shift-brief-ai-cli/
├── .gitignore
├── Pipfile
├── README.md
├── pytest.ini
├── requirements.txt
├── lib/
│   ├── __init__.py
│   ├── ai_client.py
│   ├── brief_builder.py
│   └── shift_cli.py
└── tests/
    ├── conftest.py
    ├── test_ai_client.py
    ├── test_brief_builder.py
    └── test_shift_cli.py
```

You will work primarily in:

```txt
lib/ai_client.py
lib/brief_builder.py
lib/shift_cli.py
```

Do not edit the test files. Use them to guide your development.

---

## Required Architecture

Your application should use three main parts.

### 1. `OllamaChatClient`

Defined in:

```txt
lib/ai_client.py
```

This class should stay generic. It should not include shift-specific, handoff-specific, store-specific, or retail-specific instructions.

The AI client should own:

- model name,
- message history,
- prompt validation,
- the call to `ollama.chat()`,
- assistant response extraction,
- service-level errors,
- reset and history-access methods.

Required methods:

```python
__init__(model_name="llama3.2")
send(prompt)
reset()
message_count()
get_transcript()
```

The AI client should not own:

- terminal input,
- terminal menus,
- printed CLI output,
- shift handoff instructions,
- required handoff sections,
- retail or store workflow logic.

---

### 2. `HandoffBriefBuilder`

Defined in:

```txt
lib/brief_builder.py
```

This class owns the shift-handoff workflow.

The brief builder should own:

- required handoff brief sections,
- prompt construction for a new brief,
- prompt construction for revising a previous brief,
- response usability checks,
- user-facing brief formatting,
- calls to the generic AI client through public methods.

Required methods:

```python
build_brief_prompt(notes)
build_revision_prompt(feedback)
is_usable_brief(response_text)
format_brief(response_text)
create_brief(ai_client, notes)
revise_brief(ai_client, feedback)
```

The required handoff sections are:

```txt
Shift Summary:
Open Issues:
Action Items:
Follow-Up Questions:
Risk Notes:
```

---

### 3. `ShiftBriefCLI`

Defined in:

```txt
lib/shift_cli.py
```

This class owns the command-line workflow.

The CLI should own:

- welcome message,
- command guidance,
- command parsing,
- user-facing input errors,
- user-facing service errors,
- displayed output,
- the run loop.

Required commands:

```txt
brief <shift notes>
revise <feedback>
history
reset
help
exit
quit
```

Commands should be case-insensitive. Extra spaces around commands should not break the application.

The CLI should not:

- import `ollama`,
- call `ollama.chat()`,
- directly edit the AI client’s internal history.

---

## Setup

Install dependencies before running the tests.

### Option 1: Pipenv (Recommended)

From the project root, run:

```bash
pipenv install --dev
pipenv shell
```

### Option 2: pip

From the project root, run:

```bash
python -m pip install -r requirements.txt
```

---

## Running the Tests

Run the test suite from the project root:

```bash
pytest
```

At first, many tests will fail. That is expected. The tests are designed to guide your development.

As you implement each feature, run the tests again. More tests should pass as your code becomes more complete.

The test suite checks that your application can:

- initialize the AI client correctly,
- validate blank prompts,
- call the AI service through the reusable client,
- extract assistant responses,
- manage message history,
- reset conversation history,
- protect internal history from outside mutation,
- build shift-specific prompts outside the AI client,
- verify required handoff sections,
- route CLI commands,
- show readable input and service errors,
- and keep service logic separate from CLI logic.

You do not need Ollama running to pass the tests. The tests mock the AI service call.

---

## Manual Run

After your tests pass, your CLI should have full functionality.

To try it out, from the project root, run:

```bash
python lib/shift_cli
```

Generated AI responses may vary because the model creates the output.

---

## Example CLI Session

When you start the application, you should see command guidance similar to this:

```txt
Shift Handoff Brief CLI
Create and revise AI-assisted shift handoff briefs.

Commands:
- brief <shift notes>     Create a new handoff brief.
- revise <feedback>      Revise the previous brief using feedback.
- history                Show the current conversation message count.
- reset                  Clear conversation history.
- help                   Show this command list.
- exit or quit           Stop the program.
```

Create a new brief:

```txt
> brief Register 2 froze twice during closing. Maya restarted it, but it may need IT review tomorrow. Stockroom still has three carts of unsorted returns.
```

Example output:

```txt
Shift Handoff Brief
Shift Summary:
Register 2 froze twice during closing and may need IT review. The stockroom still has three carts of unsorted returns.

Open Issues:
Register 2 may still need IT review. Three carts of returns remain unsorted.

Action Items:
Ask IT to inspect Register 2. Assign staff to sort the remaining returns.

Follow-Up Questions:
Did Register 2 display an error code? Are the returns time-sensitive?

Risk Notes:
A frozen register may slow checkout if the issue continues. Unsorted returns may affect the next shift’s workflow.
```

Revise the previous brief:

```txt
> revise Make the action items more specific and include who should review Register 2.
```

Example output:

```txt
Revised Shift Handoff Brief
Shift Summary:
Register 2 froze twice during closing and may need IT review. The stockroom still has three carts of unsorted returns.

Open Issues:
Register 2 may continue to freeze during checkout. Three carts of returns remain unsorted.

Action Items:
Ask the IT team to inspect Register 2 before the next busy checkout period. Ask the opening manager to assign staff to sort the remaining returns.

Follow-Up Questions:
Did Register 2 display an error code? Is there a backup register available if the problem happens again?

Risk Notes:
A frozen register may slow checkout. Unsorted returns may delay restocking or create extra work for the next shift.
```

Check conversation history:

```txt
> history
```

Example output:

```txt
Conversation messages: 4
```

Reset conversation history:

```txt
> reset
```

Example output:

```txt
Conversation history reset.
```

Exit the application:

```txt
> exit
```

Example output:

```txt
Goodbye!
```

---

## Conversation History Note

The `history` command shows how many messages are currently stored in the AI client’s conversation history.

Each AI interaction usually adds two messages:

1. the user prompt sent to the model,
2. the assistant response returned by the model.

For example:

- Before creating a brief: `Conversation messages: 0`
- After one `brief` command: `Conversation messages: 2`
- After one `revise` command: `Conversation messages: 4`
- After `reset`: `Conversation messages: 0`

The `history` command itself does not add a message. It only reports the current count.

---

## Implementation Instructions

Use the steps below to complete the lab.

---

### Step 1: Identify the Responsibility Boundaries

Before writing code, review the three required files and decide what each part of the application should own.

Use this responsibility map:

| File | Main Responsibility |
|---|---|
| `lib/ai_client.py` | Generic AI service communication |
| `lib/brief_builder.py` | Shift-handoff prompt building and response checks |
| `lib/shift_cli.py` | CLI commands, user input, and displayed output |

The AI client should stay reusable. It should not know about shift summaries, action items, risk notes, or retail store workflows.

The brief builder should know about shift handoff requirements. It should build prompts and check whether returned briefs include the required sections.

The CLI should manage the user experience. It should route commands and display messages, but it should not call the AI service directly.

---

### Step 2: Run the Tests Before Implementing

Run:

```bash
pytest
```

The starter code is incomplete, so the tests should fail at first.

Read the test names and failure messages. They are your development checklist.

---

### Step 3: Implement the Generic AI Client

Open:

```txt
lib/ai_client.py
```

Implement `OllamaChatClient`.

Your client should:

- initialize with a default model name of `llama3.2`,
- accept a custom model name,
- store message history as an instance attribute,
- reject `None`, empty, or whitespace-only prompts,
- strip prompts before storing them,
- append a user message before calling the AI service,
- call `ollama.chat()` with the model name and message history,
- extract usable assistant response content,
- reject missing, non-string, or blank assistant content,
- append assistant content to history after a successful response,
- return the assistant response text,
- remove the failed user message if the service call or response extraction fails,
- raise `RuntimeError` for service-level failures,
- reset conversation history,
- return the number of stored messages,
- and return a safe copy of the transcript.

Run the tests again:

```bash
pytest
```

Focus on getting the AI client tests passing before moving on.

---

### Step 4: Implement the Handoff Brief Builder

Open:

```txt
lib/brief_builder.py
```

Implement `HandoffBriefBuilder`.

Your builder should:

- define the required handoff sections,
- reject blank shift notes,
- reject blank revision feedback,
- build a prompt for creating a new shift handoff brief,
- build a prompt for revising a previous brief,
- include all required section labels in prompts,
- include the original notes or revision feedback,
- tell the model not to invent unsupported details,
- tell the model to use `Unknown` when details are missing,
- check whether an AI response includes the required sections,
- format a created brief with a clear heading,
- format a revised brief with a clear heading,
- and raise `RuntimeError` when the AI response does not include the required structure.

Run the tests again:

```bash
pytest
```

Focus on getting the brief-builder tests passing.

---

### Step 5: Implement the CLI Workflow

Open:

```txt
lib/shift_cli.py
```

Implement `ShiftBriefCLI`.

Your CLI should:

- initialize with an injected AI client,
- use a `HandoffBriefBuilder`,
- display a welcome message,
- return command help,
- support `brief <shift notes>`,
- support `revise <feedback>`,
- support `history`,
- support `reset`,
- support `help`,
- support `exit` and `quit`,
- handle commands case-insensitively,
- return readable errors for blank input,
- return readable errors for unknown commands,
- return readable errors for missing shift notes or revision feedback,
- return readable service errors when the builder or AI client raises a runtime error,
- and stop the run loop when the user exits.

Run the tests again:

```bash
pytest
```

Focus on getting the CLI tests passing.

---

### Step 6: Verify the Full Application

When your implementation is complete, run the full test suite:

```bash
pytest
```

All tests should pass.

Then review your code and check the responsibility boundaries:

- Does the AI client stay generic?
- Does the brief builder own the shift-specific workflow?
- Does the CLI handle commands and display?
- Does the CLI avoid calling `ollama.chat()` directly?
- Does the CLI avoid directly editing the AI client’s internal history?
- Are user-facing errors clear?
- Is conversation history managed through the AI client?

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'ollama'`

Install dependencies and enter the virtual environment:

```bash
pipenv install --dev
pipenv shell
```

or:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
pytest
```

---

### Tests fail at first

That is expected. The starter code is incomplete.

Use the tests as a checklist. Implement one feature at a time and rerun the tests often.

---

### Manual run gives a service error

The tests do not require Ollama to be running, but manual use does.

For manual testing, make sure:

```bash
ollama pull llama3.2
```

has been run, and then start the app again:

```bash
python lib/shift_cli
```

---

### AI output varies

That is normal. AI-generated output may vary between runs.

Your code should not depend on the model returning the exact wording shown in the examples. Instead, your builder should ask for the required sections and check that those section labels are present.

---

## Reflection

After completing the lab, answer these questions for yourself:

1. What responsibility belongs to the AI client?
2. What responsibility belongs to the brief builder?
3. What responsibility belongs to the CLI?
4. Why should the AI client stay generic instead of including shift-handoff-specific language?
5. How did the tests help guide your implementation?
6. How could this reusable client pattern transfer later into a Flask API, RAG workflow, or full-stack AI application?
# Completed lab: Module 7 — Shift Brief AI CLI

Run `python -m lib.shift_cli` or `python lib/shift_cli.py`. Install `requirements.txt`. The generic client handles history and rollback, the builder owns brief prompts and structure checks, and the CLI owns commands. Real generation requires a running Ollama service and the `llama3.2` model. Live generation is not verified; the local endpoint was unavailable.

Validation: 80 mocked-service tests passed. Run `python -m pytest --assert=plain -q` from the repository root after installing test dependencies. The plain-assertion option supports the pinned pytest on Python 3.14.

![Verified test results](docs/test-results.png)

The image shows captured test output rendered for documentation. Canvas accepts this repository URL for submission.
