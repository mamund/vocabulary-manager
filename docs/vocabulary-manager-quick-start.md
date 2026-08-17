# Vocabulary Manager Quick Start

This guide shows how to author a simple vocabulary, validate it, and generate the cross-linked HTML artifact.

## 1. Create a vocabulary file

Create a file named:

```text
my-vocabulary.md
```

Add a small vocabulary:

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

Vocabulary Manager recognizes five term kinds:

```text
atom
enumerator
composite
resource
affordance
```

Atoms, resources, and affordances are leaf terms. Enumerators contain values. Composites assemble atoms and/or other composites.

## 2. Validate the vocabulary

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

To see every validation check, including successful checks:

```bash
python vocab_validator.py --verbose my-vocabulary.md
```

For machine-readable output:

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

## 3. Generate the HTML vocabulary

Once the Markdown validates, build the HTML artifact:

```bash
python vocab_builder.py my-vocabulary.md -o ./vocab-html
```

The builder validates the source before generating HTML.

The output will look roughly like:

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
- five section landing pages
- one local HTML page per vocabulary term
- cross-links from composite members to their term pages
- derived `Used by` backlinks
- client-side search
- artifact metadata
- no external runtime dependencies

## 4. Open the vocabulary

Open:

```text
vocab-html/index.html
```

in a web browser.

You can browse by vocabulary kind or use the client-side search box to find terms.

## 5. Edit and rebuild

The Markdown file remains the authored source.

Make changes in:

```text
my-vocabulary.md
```

Then validate again:

```bash
python vocab_validator.py my-vocabulary.md
```

and rebuild:

```bash
python vocab_builder.py my-vocabulary.md -o ./vocab-html
```

The HTML artifact is generated from the Markdown source and should not be edited independently.

## Common authoring rules

Every term MUST have:

- a unique name
- a valid `Kind`
- a complete local definition

Composite members MUST reference existing atoms or composites:

```markdown
Composition:

* taskId : MUST
* title : MUST
* dueDate : SHOULD

Additional: MAY
```

Enumerator values stay inside the enumerator and do not become vocabulary terms:

```markdown
Values:

* pending : The task has not yet been completed.
* completed : The task has been completed.
```

Resources and affordances remain leaf terms. Inputs, returns, resource relationships, and other API design details belong later in the API Story.

## Typical workflow

```text
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

The Markdown vocabulary is the source. The validator checks it. The builder publishes it.
