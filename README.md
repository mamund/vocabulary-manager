# Vocabulary Manager

Vocabulary Manager is a small toolchain for authoring, validating, and publishing domain vocabularies for API design.

It helps establish a stable project language before that language is translated into API stories, interface descriptions, code, and other downstream artifacts.

The workflow is intentionally simple:

```text id="2psznk"
Vocabulary Markdown
        |
        v
vocab_validator.py
        |
        v
vocab_builder.py
        |
        v
Searchable HTML Vocabulary
```

The Markdown vocabulary is the authored source. The validator checks its structural correctness. The builder turns a valid vocabulary into a self-contained, cross-linked HTML artifact.

## Quick start

New to Vocabulary Manager?

Start with:

**[Vocabulary Manager Quick Start](docs/vocabulary-manager-quick-start.md)**

The Quick Start introduces the five vocabulary kinds, builds a small example vocabulary, validates it, and generates the HTML artifact.

## The five vocabulary kinds

Vocabulary Manager organizes domain terms into five kinds:

| Kind | Represents | Example |
|---|---|---|
| `atom` | An individual semantic concept | `toolId` |
| `enumerator` | A named set of controlled values | `ToolCondition` |
| `composite` | A meaningful grouping of vocabulary terms | `Tool` |
| `resource` | A resource concept available for later API design | `tool` |
| `affordance` | A meaningful domain behavior available for later API design | `reserveTool` |

### Atoms

Atoms are leaf vocabulary terms representing individual semantic concepts.

Examples:

```text id="ff76bd"
toolId
toolName
memberId
reservationDate
```

### Enumerators

Enumerators define named sets of controlled values.

For example:

```text id="z6q8nk"
ToolCondition
  available
  reserved
  maintenance
  retired
```

The enumerator is a vocabulary term. Its individual values are not independent vocabulary terms.

### Composites

Composites group existing vocabulary terms into meaningful domain concepts.

A composite may contain atoms, enumerators, and other composites.

For example:

```text id="e4m8d7"
Tool
 ├── toolId          MUST
 ├── toolName        MUST
 ├── ToolCondition   SHOULD
 └── Reservation     MAY
```

`MUST`, `SHOULD`, and `MAY` describe the relationship between the composite and the member.

Composition describes semantic membership. It does not prescribe a JSON object, XML structure, database record, class, or other implementation representation.

### Resources

Resources are leaf vocabulary terms naming resource concepts that may later participate in API design.

Examples:

```text id="dlzyj9"
tool
member
reservation
```

### Affordances

Affordances are leaf vocabulary terms naming meaningful domain behaviors.

Examples:

```text id="4p3tmr"
reserveTool
returnTool
registerMember
```

The vocabulary names and defines these behaviors. Inputs, outputs, resource relationships, HTTP methods, and other interaction details belong to later API design.

## Vocabulary and API design

Vocabulary Manager is concerned with the language of the domain.

It can establish concepts such as:

```text id="snb25z"
toolId
ToolCondition
Tool
tool
reserveTool
```

and define what those concepts mean.

It does not determine:

```text id="2wafap"
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

This separation allows vocabulary terms to remain stable as the design is translated into different representations and implementation technologies.

## Requirements

- Python 3
- no third-party runtime dependencies

## Validate a vocabulary

Run:

```bash id="f0hjvq"
python vocab_validator.py examples/tool-shed-vocabulary.md
```

A successful validation reports:

```text id="a8iknr"
PASS: ...
WARN: ...
ERROR: 0

VALID
```

Useful options include:

```bash id="fjvy8k"
python vocab_validator.py --verbose examples/tool-shed-vocabulary.md
python vocab_validator.py --json examples/tool-shed-vocabulary.md
python vocab_validator.py --quiet examples/tool-shed-vocabulary.md
```

Exit codes:

```text id="8djj1k"
0  valid
1  validation failed
2  usage or file-read error
```

## Build the HTML vocabulary

Run:

```bash id="uglj4u"
python vocab_builder.py examples/tool-shed-vocabulary.md -o ./vocab-html
```

The builder validates the Markdown before generating the artifact.

The generated vocabulary includes:

- a vocabulary landing page;
- section pages for the five vocabulary kinds;
- one local page for every vocabulary term;
- links between composite members and their term pages;
- derived `Used by` backlinks;
- client-side search;
- artifact metadata.

Open:

```text id="d7x8nd"
vocab-html/index.html
```

in a browser to explore the generated vocabulary.

## Repository structure

```text id="2c97io"
vocabulary-manager/
├── README.md
├── vocab_validator.py
├── vocab_builder.py
├── docs/
│   ├── vocabulary-manager-quick-start.md
│   ├── vocabulary-markdown-format.md
│   └── vocabulary-html-format.md
├── examples/
└── tests/
```

The main documents serve different purposes:

- **README** — project orientation and basic usage
- **Quick Start** — introduction to the vocabulary model and first walkthrough
- **Markdown Format** — normative source-format rules
- **HTML Format** — generated-artifact specification
- **Examples** — working vocabularies and demonstrations

## Documentation

- [Vocabulary Manager Quick Start](docs/vocabulary-manager-quick-start.md)
- [Vocabulary Markdown Format](docs/vocabulary-markdown-format.md)
- [Vocabulary HTML Format](docs/vocabulary-html-format.md)

## Design principles

Vocabulary Manager favors a small, explicit format that is:

- readable and editable by humans;
- suitable for AI-assisted authoring;
- deterministic for validation and generation;
- independent of API representation;
- focused on domain language rather than complete API design.

The Markdown vocabulary remains the source of truth. Generated HTML is a published projection of that source.