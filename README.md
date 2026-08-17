# Vocabulary Manager

Vocabulary Manager is a small, dependency-free toolchain for defining, validating, and publishing domain vocabularies for API design.

Authors maintain vocabulary in a human-readable Markdown format. The validator checks structural correctness and referential integrity. The builder publishes the validated vocabulary as a self-contained, cross-linked, searchable static HTML artifact.

## Repository contents

```text
vocabulary-manager/
├── README.md
├── vocab_validator.py
├── vocab_builder.py
├── docs/
│   ├── vocabulary-markdown-format.md
│   └── vocabulary-html-format.md
├── examples/
│   └── tool-shed-vocabulary.md
├── tests/
│   ├── README.md
│   ├── run_tests.py
│   └── fixtures/
├── LICENSE
└── .gitignore
```

## Requirements

- Python 3.10+
- No third-party packages

## Validate a vocabulary

```bash
python vocab_validator.py examples/tool-shed-vocabulary.md
```

Useful options:

```text
-h, --help
--version
-q, --quiet
-v, --verbose
--json
```

The validator performs deterministic structural and referential-integrity checks.

> Validation identifies structural problems; coaching identifies semantic weaknesses.

## Build the HTML artifact

```bash
python vocab_builder.py examples/tool-shed-vocabulary.md -o ./vocab-html
```

The builder validates first by default, then generates a dependency-free static artifact with:

- top-level vocabulary landing page
- five kind-specific section pages
- one local HTML page per vocabulary term
- composite cross-links
- derived `Used by` backlinks
- local external-reference records
- client-side search
- artifact metadata

The builder supports:

```text
-h, --help
--version
-q, --quiet
-v, --verbose
--json
-o, --output <directory>
--no-validate
```

`--no-validate` is intended only for development/debugging and should not be used in normal publication workflows.

## Vocabulary model

Vocabulary Manager currently recognizes five kinds of vocabulary terms:

- `atom`
- `enumerator`
- `composite`
- `resource`
- `affordance`

Atoms, resources, and affordances are leaf terms. Enumerators contain values. Composites assemble atoms and/or other composites using `MUST`, `SHOULD`, and `MAY` relationships.

See the format specifications in `docs/` for details.

## Run the validator test suite

```bash
python tests/run_tests.py ./vocab_validator.py
```

## Design boundary

The vocabulary defines reusable semantic terms for API design.

The vocabulary does not define API Story relationships such as action inputs, action returns, resource returns, or resource/action relationships.

The HTML artifact is a deterministic projection of the Markdown source. It is not a second independently authored vocabulary.

## Status

This repository is an initial working release of the Vocabulary Manager toolchain. The formats and tools are intentionally versioned below 1.0 while they are exercised against real API design projects.
