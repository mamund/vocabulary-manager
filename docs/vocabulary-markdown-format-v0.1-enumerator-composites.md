# Vocabulary Markdown Format v0.1

## Purpose

Define a small, human-readable Markdown format for recording a domain vocabulary before generating the cross-linked HTML vocabulary artifact.

The format is intended to be:

- easy for designers and coaches to author and review;
- deterministic enough for structural validation;
- deterministic enough to generate the HTML vocabulary artifact;
- independent of API representation and interaction design.

The vocabulary defines reusable semantic terms. API Story design determines how those terms are assembled into API resources, actions, inputs, and returns.

---

## 1. Document structure

A vocabulary document MUST contain exactly one level-one heading (`#`) naming the vocabulary.

Example:

```markdown
# Tool Shed Vocabulary
```

The document MUST contain a `Version` value.

```markdown
Version: 0.1.0
```

The document SHOULD contain a `Status` value.

```markdown
Status: draft
```

The document SHOULD contain a general description of the vocabulary.

The document MUST contain these five level-two sections:

```markdown
## Atoms
## Enumerators
## Composites
## Resources
## Affordances
```

Each section MUST occur no more than once.

Terms MUST be declared as level-three headings (`###`) within the appropriate section.

Term names MUST be unique across the entire vocabulary.

Generated date and time MUST NOT be required in the Markdown source. Generation metadata belongs to the generated artifact.

---

## 2. Common term rules

Every vocabulary term MUST:

- have a unique name;
- have a `Kind` declaration;
- have a complete local definition;
- appear in the section corresponding to its kind;
- conform to applicable Project Conventions.

`Kind` MUST be one of:

```text
atom
enumerator
composite
resource
affordance
```

Example:

```markdown
### toolId

Kind: atom

A stable identifier for a tool.
```

The declared `Kind` MUST agree with the section containing the term. For example, a term under `## Atoms` MUST declare `Kind: atom`.

A vocabulary term MAY contain one or more external references. External references MUST supplement rather than replace the local definition.

---

## 3. Atom rules

An atom is a leaf vocabulary term representing an individual semantic concept.

Example:

```markdown
### dueDate

Kind: atom

The date by which an item is expected to be completed.
```

An atom:

- MUST have a complete local definition;
- MUST NOT contain `Values`;
- MUST NOT contain `Composition`;
- MUST NOT contain `Additional`;
- MAY contain external references.

---

## 4. Enumerator rules

An enumerator is a vocabulary term defining a named set of controlled values.

Example:

```markdown
### ToolCondition

Kind: enumerator

The recognized condition values for a tool.

Values:

* available : The tool is available for normal use.
* reserved : The tool is currently reserved.
* maintenance : The tool is unavailable while maintenance is performed.
* retired : The tool is no longer available for use.
```

An enumerator:

- MUST contain `Values`;
- MUST contain at least one value;
- MUST NOT contain `Composition`;
- MUST NOT contain `Additional`.

Each enumerator value:

- MUST have a value identifier;
- MUST have a definition;
- MUST be unique within its enumerator;
- SHOULD conform to applicable Project Conventions.

Enumerator values are NOT vocabulary terms. They MUST NOT receive independent vocabulary term pages in the generated artifact.

The enumerator itself IS a vocabulary term and MUST receive a vocabulary term page.

---

## 5. Composite rules

A composite is a vocabulary term that assembles atoms, enumerators, and/or other composites for a particular domain context.

Example:

```markdown
### Tool

Kind: composite

A contextual description of a tool in the Tool Shed domain.

Composition:

* toolId : MUST
* toolName : MUST
* toolCondition : SHOULD
* Reservation : MAY

Additional: MAY
```

A composite:

- MUST contain `Composition`;
- MUST contain at least one member;
- MUST declare an `Additional` policy;
- MUST NOT contain `Values`.

Each composition member:

- MUST reference an existing vocabulary term;
- MUST reference a term whose kind is `atom`, `enumerator`, or `composite`;
- MUST appear no more than once within the composite;
- MUST declare one requirement level.

The requirement level MUST be one of:

```text
MUST
SHOULD
MAY
```

MUST, SHOULD, and MAY apply to the relationship between the composite and the referenced member. They do not describe an intrinsic property of the referenced term.

Composites MAY reference enumerators and other composites. Composite references allow nested composition, while enumerator references allow controlled value concepts to participate directly in a composite context.

Composition describes semantic membership. It MUST NOT be interpreted as prescribing a JSON, XML, database, programming-language, or other representation structure.

### Additional policy

`Additional` indicates whether terms beyond those explicitly listed in `Composition` may participate in the composite.

For v0.1, the syntax is:

```markdown
Additional: MAY
```

The precise semantics and allowed values for `Additional` remain provisional in v0.1 and MAY be refined in a later version of this format.

---

## 6. Resource rules

A resource is a leaf vocabulary term naming a resource concept available for later API design.

Example:

```markdown
### tool

Kind: resource

A tool managed by the Tool Shed.
```

A resource:

- MUST have a complete local definition;
- MUST NOT contain `Values`;
- MUST NOT contain `Composition`;
- MUST NOT contain `Additional`;
- MUST NOT specify `returns`;
- MUST NOT specify actions or affordances associated with the resource.

Resource relationships belong to the API Story rather than the vocabulary.

---

## 7. Affordance rules

An affordance is a leaf vocabulary term naming a meaningful domain behavior available for later API design.

Example:

```markdown
### reserveTool

Kind: affordance

Reserve a tool for a member.
```

An affordance:

- MUST have a complete local definition;
- MUST NOT contain `Values`;
- MUST NOT contain `Composition`;
- MUST NOT contain `Additional`;
- MUST NOT specify inputs;
- MUST NOT specify returns;
- MUST NOT associate itself with a resource.

Inputs, returns, and resource/action relationships belong to the API Story rather than the vocabulary.

---

## 8. External reference rules

A vocabulary term MAY identify one or more external semantic references.

Example:

```markdown
### toolName

Kind: atom

The human-readable name of a tool.

External:

* Source: Schema.org
  URI: https://schema.org/name
```

Each external reference:

- MUST identify a `Source`;
- MUST provide a valid `URI`;
- MUST NOT replace the local term definition.

A term MAY contain multiple external references.

Failure to retrieve or resolve an external URI MUST NOT invalidate the local vocabulary definition or generated HTML artifact.

The generated vocabulary artifact MUST retain a complete local page for every vocabulary term, including terms reconciled with external vocabularies.

---

## 9. Vocabulary and API design boundary

Vocabulary terms MUST describe semantic meaning without prescribing API representation or interaction structure.

The vocabulary MUST NOT define:

- resource return types;
- actions associated with resources;
- affordance inputs;
- affordance returns;
- HTTP methods or status codes;
- URI structures;
- JSON, XML, or other representation shapes.

These relationships and representation decisions belong to later design artifacts, beginning with the API Story.

---

## 10. Validation severity

A validator SHOULD distinguish structural errors from advisory warnings.

### Errors

An error indicates that the document does not conform to Vocabulary Markdown Format v0.1.

Examples:

```text
ERROR  Tool references undefined term "toolName".
ERROR  Tool member "toolId" has invalid requirement "REQUIRED".
ERROR  reserveTool (affordance) declares Inputs.
ERROR  ToolCondition has no Values.
ERROR  Duplicate vocabulary term "memberId".
```

Structural errors SHOULD cause validation to fail.

### Warnings

A warning identifies a structurally valid condition that may deserve review.

Examples:

```text
WARN  ToolCondition contains only one value.
WARN  Customer contains a large number of members.
WARN  status is defined but is not referenced by any composite.
```

Warnings SHOULD NOT cause structural validation to fail.

---

## 11. Validation and coaching

Structural validation and semantic coaching serve different purposes.

Validation SHOULD identify objectively detectable problems such as:

- missing required elements;
- duplicate terms;
- invalid kinds;
- invalid composition references;
- invalid requirement levels;
- malformed enumerators;
- prohibited fields for a term kind;
- broken local references.

Coaching SHOULD address semantic questions such as:

- vague or weak definitions;
- overloaded terminology;
- likely synonyms;
- questionable distinctions between terms;
- inappropriate composite membership;
- questionable MUST/SHOULD/MAY choices;
- opportunities to reconcile terms with existing organizational or external vocabularies.

**Validation identifies structural problems; coaching identifies semantic weaknesses.**

---

## 12. Generated HTML artifact requirements

A conforming vocabulary source SHOULD be suitable for deterministic generation of a self-contained HTML vocabulary artifact.

The generated artifact SHOULD provide:

- a vocabulary home page;
- section pages for atoms, enumerators, composites, resources, and affordances;
- one complete local page for every vocabulary term;
- cross-links from composite members to their vocabulary pages;
- lightweight backlinks showing composite membership where useful;
- client-side vocabulary search without an external runtime dependency;
- artifact metadata on the home page, including domain, version, status, and generated date/time;
- stable local term URIs suitable for downstream semantic references such as ALPS `def`.

Enumerator values MUST remain on their enumerator page and MUST NOT receive independent term pages.

External references MUST remain supplemental. The generated artifact MUST remain useful without access to external vocabulary sites.

---

## 13. v0.1 design principles

Vocabulary Markdown Format v0.1 intentionally favors a small number of explicit rules.

The format SHOULD remain:

- readable and editable by humans;
- straightforward for AI coaches to produce;
- deterministic for validators and generators;
- focused on vocabulary rather than API design;
- independent of any particular representation format.

New syntax SHOULD be added only when experience with real domain vocabularies demonstrates a recurring need.
