# Vocabulary Manager Quick Start

Vocabulary Manager is a small toolchain for defining, validating, and publishing a domain vocabulary for API design.

A vocabulary gives the project a stable language before that language is translated into API stories, interface descriptions, code, and other downstream artifacts.

The basic workflow is:

```text
Define the vocabulary
        |
        v
Validate the Markdown
        |
        v
Generate the HTML vocabulary
```

This guide walks through that process using a small task-management vocabulary.

## 1. Understand the five kinds

Vocabulary Manager organizes terms into five kinds:

| Kind | Represents | Example |
|---|---|---|
| `atom` | An individual semantic concept | `taskId` |
| `enumerator` | A named set of controlled values | `TaskStatus` |
| `composite` | A meaningful grouping of vocabulary terms | `Task` |
| `resource` | A resource concept available for later API design | `task` |
| `affordance` | A meaningful domain behavior available for later API design | `updateTask` |

These kinds describe different roles that terms play in the domain language.

### Atoms

An **atom** represents an individual semantic concept.

For example:

```markdown
### taskId

Kind: atom

A stable identifier for a task.
```

Other atoms might include:

```text
title
dueDate
createdAt
```

Atoms are leaf terms. They do not contain other vocabulary terms.

### Enumerators

An **enumerator** defines a named set of controlled values.

For example:

```markdown
### TaskStatus

Kind: enumerator

The recognized status values for a task.

Values:

* pending : The task has not yet been completed.
* completed : The task has been completed.
```

`TaskStatus` is a vocabulary term.

The values `pending` and `completed` belong to that enumerator. They are not independent vocabulary terms.

### Composites

A **composite** groups existing vocabulary terms into a meaningful domain concept.

For example:

```markdown
### Task

Kind: composite

A contextual description of a task.

Composition:

* taskId : MUST
* title : MUST
* TaskStatus : SHOULD
* dueDate : SHOULD

Additional: MAY
```

This tells us that the concept `Task` includes several other concepts from the vocabulary.

The requirement level describes the relationship between the composite and the member:

```text
MUST
SHOULD
MAY
```

For example:

```text
Task
 ├── taskId       MUST
 ├── title        MUST
 ├── TaskStatus   SHOULD
 └── dueDate      SHOULD
```

Atoms, enumerators, and other composites may participate in a composite.

Composition describes semantic membership. It does not prescribe a JSON object, XML structure, database record, class, or other implementation representation.

### Resources

A **resource** names a resource concept that may later appear in the API design.

For example:

```markdown
### task

Kind: resource

A task managed through the API.
```

A resource is a leaf vocabulary term.

The vocabulary identifies and defines the concept. It does not specify its representation, operations, return type, URI, or HTTP behavior.

### Affordances

An **affordance** names a meaningful behavior available in the domain.

For example:

```markdown
### updateTask

Kind: affordance

Update information about a task.
```

Other affordances might include:

```text
createTask
completeTask
deleteTask
```

Affordances are also leaf terms.

The vocabulary names and defines the behavior. Inputs, outputs, resource relationships, HTTP methods, and other interaction details belong to later API design.

## 2. See the vocabulary as a language

The five kinds work together to establish a reusable language for the domain.

Our small example contains:

```text
Atoms
  taskId
  title
  dueDate

Enumerator
  TaskStatus
    pending
    completed

Composite
  Task
    taskId
    title
    TaskStatus
    dueDate

Resource
  task

Affordances
  readTask
  updateTask
```

At this stage we know what these terms mean.

We deliberately have not decided things such as:

```text
PUT /tasks/123
POST /tasks/123/complete
GET /tasks/123
```

Those are API design decisions.

Vocabulary Manager establishes the language that later design stages can use to express those decisions.

## 3. Create the vocabulary file

Create a file named:

```text
my-vocabulary.md
```

Add the vocabulary:

```markdown
# Sample Vocabulary

Version: 0.1.0
Status: draft

A small vocabulary for a task-management API.

## Atoms

### taskId

Kind: atom

A stable identifier for a task.

### title

Kind: atom

The human-readable title of a task.

### dueDate

Kind: atom

The date by which a task is expected to be completed.

## Enumerators

### TaskStatus

Kind: enumerator

The recognized status values for a task.

Values:

* pending : The task has not yet been completed.
* completed : The task has been completed.

## Composites

### Task

Kind: composite

A contextual description of a task.

Composition:

* taskId : MUST
* title : MUST
* TaskStatus : SHOULD
* dueDate : SHOULD

Additional: MAY

## Resources

### task

Kind: resource

A task managed through the API.

## Affordances

### readTask

Kind: affordance

Retrieve information about a task.

### updateTask

Kind: affordance

Update information about a task.
```

A vocabulary document always contains the five sections:

```markdown
## Atoms
## Enumerators
## Composites
## Resources
## Affordances
```

Every term has a unique name, a `Kind`, and a complete local definition.

## 4. Validate the vocabulary

Run:

```bash
python vocab_validator.py my-vocabulary.md
```

A valid vocabulary produces a summary similar to:

```text
PASS: 54
WARN: 0
ERROR: 0

VALID
```

Validation checks structural correctness and referential integrity.

For example, the validator can detect:

- duplicate term names
- invalid kinds
- missing definitions
- invalid composite references
- malformed enumerators
- invalid requirement levels
- fields that are not allowed for a particular kind

Validation does not determine whether your vocabulary is a good description of the domain.

That requires domain review and, where appropriate, semantic coaching.

To see every validation check:

```bash
python vocab_validator.py --verbose my-vocabulary.md
```

For machine-readable results:

```bash
python vocab_validator.py --json my-vocabulary.md
```

For scripts or CI where only the exit code matters:

```bash
python vocab_validator.py --quiet my-vocabulary.md
```

Exit codes are:

```text
0  valid
1  validation failed
2  usage or file-read error
```

## 5. Generate the HTML vocabulary

Once the Markdown validates, build the HTML artifact:

```bash
python vocab_builder.py my-vocabulary.md -o ./vocab-html
```

The builder validates the vocabulary before generating the HTML.

The resulting directory will look roughly like:

```text
vocab-html/
  index.html

  atoms/
    index.html
    taskId.html
    title.html
    dueDate.html

  enumerators/
    index.html
    TaskStatus.html

  composites/
    index.html
    Task.html

  resources/
    index.html
    task.html

  affordances/
    index.html
    readTask.html
    updateTask.html

  assets/
    styles.css
    search-index.js
    search.js
```

The generated artifact includes:

- a vocabulary landing page
- five kind-specific section pages
- one local page for each vocabulary term
- links from composite members to their term pages
- derived `Used by` backlinks
- client-side search
- artifact metadata

Enumerator values remain on the enumerator page because they are values rather than independent vocabulary terms.

## 6. Browse the vocabulary

Open:

```text
vocab-html/index.html
```

in a web browser.

You can browse the vocabulary by kind or search for individual terms.

The generated HTML makes relationships in the vocabulary easier to explore.

For example, the `Task` page links to the vocabulary pages for its members. Those member pages can also show that they are used by `Task`.

## 7. Edit and rebuild

The Markdown vocabulary remains the authored source.

Make changes in:

```text
my-vocabulary.md
```

Then validate:

```bash
python vocab_validator.py my-vocabulary.md
```

and rebuild:

```bash
python vocab_builder.py my-vocabulary.md -o ./vocab-html
```

The generated HTML is a projection of the Markdown source and should not be edited independently.

## 8. Know the design boundary

Vocabulary Manager is intentionally concerned with language rather than complete API design.

The vocabulary can tell us that these concepts exist:

```text
taskId
TaskStatus
Task
task
updateTask
```

It can also tell us what they mean and, for composites, which vocabulary terms participate in them.

It does not determine:

```text
HTTP methods
URI structures
request representations
response representations
affordance inputs
affordance returns
resource/action relationships
status codes
```

Those decisions belong to later API design artifacts.

This boundary keeps the vocabulary reusable.

The same term can survive several translations from domain understanding through design and implementation without requiring the vocabulary itself to encode those later decisions.

## 9. Typical workflow

The complete Vocabulary Manager workflow is:

```text
Identify domain concepts
          |
          v
Classify the terms
          |
          v
Atoms / Enumerators / Composites
Resources / Affordances
          |
          v
Author Vocabulary Markdown
          |
          v
vocab_validator.py
          |
          v
        VALID
          |
          v
 vocab_builder.py
          |
          v
Searchable HTML Vocabulary
```

The Markdown vocabulary is the source.

The validator checks it.

The builder publishes it.

The resulting vocabulary provides a stable domain language for the API design work that follows.