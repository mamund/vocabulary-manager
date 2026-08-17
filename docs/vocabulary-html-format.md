# Vocabulary HTML Artifact Format v0.1

## Purpose

This document defines the generated HTML artifact format for API vocabularies.

The HTML artifact is a deterministic projection of a validated Vocabulary Markdown source document. It is intended to provide a stable, self-contained, human-readable, cross-linked vocabulary that can also serve as a semantic reference target for downstream artifacts such as ALPS.

The HTML artifact MUST NOT become an independently authored source of vocabulary semantics.

---

## 1. Artifact Principles

The generated vocabulary artifact MUST:

- Be self-contained.
- Be usable without access to external vocabulary sites.
- Provide one stable local HTML page for every vocabulary term.
- Provide cross-links between related vocabulary terms.
- Provide a top-level landing page.
- Provide one section landing page for each vocabulary kind.
- Preserve all definitions and semantic relationships from the validated Markdown source.
- Keep vocabulary semantics separate from API representation and interaction design.
- Avoid requiring server-side processing for normal browsing.
- Support static hosting.

The generated artifact SHOULD:

- Support client-side search.
- Provide lightweight backlinks where they improve navigation.
- Remain usable when JavaScript is unavailable, except for optional search behavior.
- Use predictable and stable relative paths.
- Be readable on desktop and mobile devices.

---

## 2. Directory Structure

The artifact MUST contain a top-level `index.html`.

It MUST contain one directory for each vocabulary kind:

```text
/
  index.html

  atoms/
    index.html

  enumerators/
    index.html

  composites/
    index.html

  resources/
    index.html

  affordances/
    index.html
```

Each vocabulary term MUST have one HTML page within the directory corresponding to its kind.

Example:

```text
/
  atoms/
    toolId.html
    toolName.html

  enumerators/
    ToolCondition.html

  composites/
    Tool.html
    Reservation.html

  resources/
    tool.html

  affordances/
    reserveTool.html
```

The artifact MAY contain an `assets/` directory for local CSS, JavaScript, search indexes, icons, or other generated support files.

---

## 3. Top-Level Landing Page

The top-level `index.html` MUST identify the vocabulary and provide navigation into the artifact.

The page MUST contain:

- Vocabulary title.
- General vocabulary description.
- Links to the five section landing pages.

The page SHOULD contain:

- Client-side search.
- A short description of the five vocabulary kinds.
- Artifact metadata.

Artifact metadata SHOULD appear after the primary descriptive and navigational content so that it does not dominate the page.

Recommended artifact metadata:

```text
Domain
Version
Status
Generated
```

Example:

```text
Domain: Tool Shed
Version: 0.1.0
Status: Draft
Generated: 2026-08-16T18:00:00-04:00
```

The generated timestamp MUST be supplied by the generator and MUST NOT be required in the Markdown source.

---

## 4. Section Landing Pages

The artifact MUST provide one landing page for each vocabulary kind:

```text
atoms/index.html
enumerators/index.html
composites/index.html
resources/index.html
affordances/index.html
```

Each section page MUST:

- Identify the vocabulary kind.
- Provide a short description of the kind.
- List every vocabulary term of that kind.
- Link each listed term to its local HTML term page.

Section pages MAY provide additional descriptive or instructional text.

Section pages SHOULD NOT duplicate the full definitions of every listed term unless doing so materially improves usability.

---

## 5. Term Pages

Every vocabulary term MUST have exactly one complete local HTML page.

A term page MUST contain:

- Term name.
- Vocabulary kind.
- Complete local definition.

A term page MAY contain:

- External references.
- Kind-specific content.
- Lightweight backlinks.
- Local navigation.

A term page MUST NOT depend on an external site for its primary definition.

External references MUST supplement the local definition rather than replace it.

---

## 6. Atom Pages

An atom page MUST contain:

- Atom name.
- Kind: `Atom`.
- Complete local definition.

An atom page MUST NOT contain:

- Composition.
- Enumerator values.
- API Story relationships such as inputs or returns.

An atom page MAY contain:

- External references.
- `Used by` backlinks to composites that reference the atom.

Example conceptual rendering:

```text
toolId

Kind: Atom

A stable identifier for a tool.

Used by
- Tool [Composite]
```

---

## 7. Enumerator Pages

An enumerator page MUST contain:

- Enumerator name.
- Kind: `Enumerator`.
- Complete local definition.
- All values defined by the enumerator.
- A definition for each value.

Enumerator values MUST remain on the enumerator page.

Enumerator values MUST NOT receive independent HTML pages.

Example conceptual rendering:

```text
ToolCondition

Kind: Enumerator

The recognized condition values for a tool.

Values

available
  The tool is available for normal use.

reserved
  The tool is currently reserved.

maintenance
  The tool is unavailable while maintenance is performed.
```

The generator MAY render values as a table, definition list, or other compact readable structure.

---

## 8. Composite Pages

A composite page MUST contain:

- Composite name.
- Kind: `Composite`.
- Complete local definition.
- Composition members.
- Requirement level for each member.
- Additional-member policy.

Every composition member MUST be rendered as a link to its local vocabulary term page.

Composite members MUST be atoms or composites.

Requirement levels MUST preserve the source values:

```text
MUST
SHOULD
MAY
```

Example conceptual rendering:

```text
Tool

Kind: Composite

A contextual description of a tool in the Tool Shed domain.

Composition

toolId          MUST
toolName        MUST
toolCondition   SHOULD
Reservation     MAY

Additional terms: MAY
```

The generator SHOULD visually distinguish the requirement level from the term name.

The page SHOULD include a short explanatory note that normative membership describes semantic expectations and does not prescribe API representation structure.

---

## 9. Resource Pages

A resource page MUST contain:

- Resource name.
- Kind: `Resource`.
- Complete local definition.

A resource page MUST NOT specify:

- Returned composites.
- Actions.
- Inputs.
- API Story relationships.

Resource remains a leaf vocabulary kind.

API Story design establishes resource relationships later.

---

## 10. Affordance Pages

An affordance page MUST contain:

- Affordance name.
- Kind: `Affordance`.
- Complete local definition.

An affordance page MUST NOT specify:

- Inputs.
- Returns.
- Associated resources.
- API Story action structure.

Affordance remains a leaf vocabulary kind.

API Story design determines how an affordance becomes an action in a particular API design.

---

## 11. Cross-Linking

The generator MUST create local links between vocabulary terms where the source vocabulary contains explicit semantic relationships.

At minimum:

- Composite members MUST link to their atom or composite term pages.

Links SHOULD use relative local paths so that the artifact remains portable and usable from static hosting or a local filesystem.

The generator MUST NOT require external links for internal vocabulary navigation.

---

## 12. Backlinks

The generator SHOULD derive lightweight backlinks from the validated source vocabulary.

Backlinks SHOULD initially be limited to relationships that are deterministic and useful.

For v0.1, recommended backlinks are:

```text
Composite membership
```

Example:

```text
toolId

Used by
- Tool [Composite]
```

Backlinks MUST NOT be authored separately in the source Markdown.

They MUST be derived by the generator.

Backlinks SHOULD appear below the primary term definition and SHOULD NOT visually dominate the page.

The artifact MAY omit backlinks when none exist.

Future versions MAY support additional derived relationships, but such additions SHOULD NOT degrade term-page readability.

---

## 13. External References

A term page MAY contain one or more external references derived from the Markdown source.

Example:

```text
External reference

Schema.org
https://schema.org/name
```

The local term page MUST remain complete when the external reference:

- Is unavailable.
- Changes.
- Is removed.
- Requires network access.

External references MUST NOT replace the local term definition.

External links SHOULD clearly identify the referenced source.

The artifact SHOULD preserve any source names and URIs recorded in the Markdown vocabulary.

---

## 14. Search

The artifact SHOULD provide client-side vocabulary search.

Search MUST NOT require a server-side application.

Search SHOULD operate entirely from files included in the generated artifact.

The search index SHOULD include:

- Term name.
- Vocabulary kind.
- Local definition.
- Local page path.

Search MAY include additional locally derived fields.

Search results SHOULD:

- Display the matching term name.
- Display the vocabulary kind.
- Provide a direct link to the term page.
- Optionally display a short definition excerpt.

Search MUST NOT require access to external vocabulary services.

The artifact SHOULD remain fully navigable when search is unavailable.

---

## 15. Navigation

Every generated page SHOULD provide consistent navigation.

Recommended navigation includes links to:

- Vocabulary home.
- Atoms.
- Enumerators.
- Composites.
- Resources.
- Affordances.

Term pages MAY additionally provide contextual navigation such as:

```text
Used by
External references
```

Navigation MUST NOT depend on JavaScript.

---

## 16. Stable Local URIs

Every vocabulary term MUST have a stable local path within the generated artifact.

Example:

```text
/vocab/atoms/dueDate.html
/vocab/composites/Customer.html
/vocab/resources/customer.html
/vocab/affordances/updateCustomer.html
```

Published deployments MAY omit `.html` through server configuration, but the generated static artifact SHOULD remain directly usable without such configuration.

Stable local term URIs SHOULD be suitable for downstream semantic references such as ALPS `def`.

Downstream artifacts SHOULD prefer the local vocabulary URI rather than an external vocabulary URI when referencing terms defined for the project.

---

## 17. Generated Versus Authored Information

The HTML generator MUST distinguish authored vocabulary semantics from generated artifact information.

Authored information includes:

- Vocabulary title.
- Vocabulary description.
- Vocabulary version.
- Vocabulary status.
- Term names.
- Term kinds.
- Term definitions.
- Enumerator values.
- Composite membership.
- Normative requirements.
- Additional-member policy.
- External references.

Generated information includes:

- Generated timestamp.
- Directory and page structure.
- Navigation.
- Internal hyperlinks.
- Backlinks.
- Search indexes.
- Search interface.
- Presentation and layout.

Generated information MUST NOT change the semantic meaning of the source vocabulary.

---

## 18. Self-Containment

The generated artifact MUST remain useful when disconnected from the network.

Local definitions, navigation, composition relationships, enumerator values, and other vocabulary semantics MUST remain available locally.

The artifact SHOULD NOT depend on:

- External JavaScript libraries.
- External CSS frameworks.
- External font services.
- External search services.
- External vocabulary sites for primary content.

External references MAY be clickable when network access is available.

---

## 19. Accessibility and Usability

Generated pages SHOULD use semantic HTML.

The artifact SHOULD:

- Use headings in logical order.
- Provide descriptive link text.
- Use sufficient text contrast.
- Support keyboard navigation.
- Adapt to narrow screens.
- Avoid unnecessarily dense layouts.
- Keep secondary information such as backlinks and metadata visually subordinate.

Search input SHOULD have an accessible label.

Tables, when used, SHOULD include proper header cells.

---

## 20. Deterministic Generation

Given the same validated Markdown source and generator version, the generator SHOULD produce semantically equivalent HTML artifacts.

Generation MUST NOT:

- Invent vocabulary terms.
- Change term definitions.
- Add API Story relationships.
- Infer new composite membership.
- Alter normative requirement levels.

The generator MAY derive:

- Internal links.
- Backlinks.
- Search indexes.
- Navigation.
- Presentation markup.

---

## 21. Validation Before Generation

HTML generation MUST operate on a vocabulary that has passed Vocabulary Markdown Format validation.

The generator SHOULD fail rather than silently repair invalid source structures such as:

- Undefined composite members.
- Duplicate vocabulary terms.
- Invalid vocabulary kinds.
- Invalid normative requirement values.
- Missing required definitions.

Semantic coaching observations SHOULD NOT prevent HTML generation unless they correspond to a structural validation failure.

---

## 22. Relationship to the Vocabulary Markdown Format

The Markdown vocabulary is the authored source.

The HTML vocabulary is the generated published artifact.

Conceptually:

```text
Vocabulary Markdown
       |
       +---- validation
       |
       +---- HTML generation
                 |
                 +-- landing page
                 +-- section pages
                 +-- term pages
                 +-- cross-links
                 +-- backlinks
                 +-- search index
                 +-- generated metadata
```

The HTML artifact MUST NOT become a second independent source of vocabulary truth.

---

## 23. Relationship to API Stories

The vocabulary artifact defines the reusable semantic terms available to API design.

It MUST NOT encode API Story design relationships.

The intended downstream mapping is:

```text
Vocabulary        API Story

Atom              Property / action input
Enumerator        Recognized values
Composite         Resource return / action input
Resource          Resource / action return
Affordance        Action
```

Inputs, returns, resource/action relationships, and rules belong to the API Story.

---

## 24. v0.1 Scope

Vocabulary HTML Artifact Format v0.1 intentionally remains small.

It defines:

- Static HTML publication.
- Five vocabulary sections.
- One local page per vocabulary term.
- Enumerator values embedded on enumerator pages.
- Composite cross-linking.
- Lightweight derived backlinks.
- Local external-reference records.
- Client-side search.
- Stable local term URIs.
- Artifact-level metadata.
- Self-contained operation.

Future versions MAY add capabilities such as richer backlink analysis, API usage references, alternate serializations, or additional navigation aids.

Such additions SHOULD preserve the core principle:

> The HTML artifact is a stable, self-contained, navigable projection of the vocabulary source, not a separate modeling language.
