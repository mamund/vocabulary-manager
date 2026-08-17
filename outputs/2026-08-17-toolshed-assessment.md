# Toolshed Domain Vocabulary Assessment

Version: 0.1.0  
Status: READY WITH QUESTIONS

## Scope

This assessment reviews the Community Tool Shed Domain Vocabulary for semantic quality and readiness for downstream API Story design.

The domain concerns a shared inventory of tools that Members discover, reserve, check out, and return. Tool Supervisors manage inventory and tool lifecycle. The principal concerns are controlled access, borrowing accountability, and lifecycle tracking [2].

The assessment considers:

- domain coverage;
- vocabulary consistency;
- Kind classification;
- definition quality;
- composite quality;
- controlled values;
- behavioral coverage;
- structural validation;
- deferred scope and open questions.

## Assessment Summary

Overall assessment: **READY WITH QUESTIONS**

The vocabulary is sufficiently coherent and complete for API Story design. The outstanding questions concern capabilities deliberately deferred from the current version rather than ambiguities that prevent use of the vocabulary.

Structural validation is complete and successful. Vocabulary Markdown Validator 0.6.1, using Vocabulary Markdown Format 0.1, reports:

- PASS: 415
- WARN: 0
- ERROR: 0
- Valid: true [9]

The vocabulary therefore satisfies the deterministic structural requirements of the supplied Vocabulary Markdown format. The coach specification requires the vocabulary artifact to conform to the Vocabulary Manager format [1].

## Coverage

Assessment: **PASS**

The vocabulary covers the primary concepts needed for the Community Tool Shed domain.

Discovery identified three principal concerns:

- controlled access, including single-reservation and eligibility constraints;
- accountability through checkout, return, and condition reporting;
- lifecycle tracking through repair and retirement [2].

The vocabulary represents the core entities involved in these concerns through Tool, Member, Reservation, and Checkout concepts and their associated behaviors.

The discovered workflow of available Tool → reservation → checkout → return is represented in the vocabulary. The source scenarios establish that an available Tool can be held for a Member, a valid reservation can become a checkout, and a checked-out Tool can subsequently be returned [5].

Inspection is represented as behavior rather than retained inspection history. This is an intentional scope decision for the current version.

Repair exists in the discovered domain [3][4] but detailed repair and maintenance records are intentionally deferred.

## Consistency

Assessment: **PASS**

The vocabulary uses one canonical concept for each accepted domain meaning.

In particular:

- `toolSupervisor` is the canonical supervisory role terminology.
- `inspection` / `inspectTool` represents condition assessment; a separate condition-report concept is not required.
- Tool operational and lifecycle state is expressed through `ToolStatus`.
- Member participation state is expressed through `MemberStatus`.
- Checkout history is represented by retained Checkout records rather than a separate Return record.
- `overdue` is a derived condition of an active Checkout rather than a separate Member status.

This produces a vocabulary with relatively little synonymy or conceptual overlap.

## Kind Classification

Assessment: **PASS**

Terms are classified according to the five Vocabulary Markdown Kinds required by the target artifact: Atom, Enumerator, Composite, Resource, and Affordance [1].

### Atoms

Atoms represent individual domain values such as identifiers, names, email addresses, and significant borrowing timestamps.

Examples include:

- `toolId`
- `toolName`
- `toolDescription`
- `memberId`
- `memberName`
- `memberEmail`
- `reservationId`
- `reservedAt`
- `expiresAt`
- `checkoutId`
- `checkedOutAt`
- `dueDate`
- `returnedAt`

The validator confirms these terms are structurally valid atoms with local definitions and without inappropriate Values or Composition blocks [9].

### Enumerators

Two finite controlled-value concepts are represented as Enumerators:

- `ToolStatus`
- `MemberStatus`

These represent genuine finite domain sets rather than arbitrary implementation constraints.

### Composites

The vocabulary uses Composites for contextual domain structures:

- `Tool`
- `Member`
- `Reservation`
- `Checkout`

Inspection is deliberately not represented as a persisted Composite because inspection history is outside the current scope.

### Resources

`tool` and `member` are Resources because Tools and Members constitute independently managed system records.

Reservation and Checkout are not currently promoted to independently managed Resources. They remain contextual domain records associated with the borrowing lifecycle.

### Affordances

Affordances represent meaningful domain behaviors rather than generic CRUD operations or protocol-level operations.

The vocabulary includes behaviors for Tool management, Member management, borrowing, inspection, and historical search.

## Definition Quality

Assessment: **PASS**

Definitions generally express domain semantics rather than simply restating term names.

Of particular importance:

- Reservation semantics describe the commitment between a Member and Tool and the conditions under which that commitment ends.
- Checkout semantics describe active borrowing and retained borrowing history.
- Tool status values describe both availability consequences and lifecycle significance.
- Member status describes whether a retained Member can currently participate in borrowing.
- Affordances describe domain intent without prematurely specifying transport or representation details.

The distinction between `outOfCommission` and `retired` is especially important. Out-of-commission Tools are temporarily unavailable and may require work, whereas retirement permanently removes a Tool from service while preserving its record.

## Composition Quality

Assessment: **PASS**

The four principal Composites contain the information required by the current domain scope.

`Tool` provides identity, descriptive information, and status.

`Member` provides identity, contact information, and participation status.

`Reservation` associates a Tool and Member with the timing information necessary to represent an expiring borrowing commitment. Reservation expiration is explicitly present in the discovered event inventory [4].

`Checkout` associates a Tool and Member with checkout, due, and return timing. Retaining `returnedAt` allows completed Checkout records to serve as viewable borrowing history.

The current compositions deliberately avoid speculative implementation metadata and information whose business purpose has not been established.

## Controlled Values

Assessment: **PASS**

### ToolStatus

The accepted Tool statuses are:

- `available`
- `reserved`
- `checkedOut`
- `outOfCommission`
- `retired`

These values describe the complete Tool state model required by the current scope.

The normal borrowing progression is:

`available → reserved → checkedOut → available`

The discovered scenarios support the reservation and checkout portions of this lifecycle [5].

A Tool can become `outOfCommission` when it should not circulate. This can represent a Tool that remains in-house requiring work or one that is externally located for repair.

`retired` is irreversible. A retired Tool remains on file for historical purposes but cannot participate further in borrowing.

### MemberStatus

The accepted Member statuses are:

- `active`
- `inactive`

An active Member may participate in borrowing subject to borrowing constraints. An inactive Member remains on file but cannot reserve or check out a Tool.

Using an Enumerator rather than a boolean leaves the concept capable of accepting additional meaningful Member statuses in a future vocabulary revision without changing its basic semantic role.

## Borrowing Rules

Assessment: **PASS**

The vocabulary supports the agreed borrowing rules for the current system.

An active Member may have at most one active borrowing commitment.

An active Reservation prevents the Member from reserving or checking out an additional Tool. The Member may:

- check out the Tool associated with that Reservation; or
- cancel the Reservation at any time before checkout.

A Reservation may also expire. Reservation expiration is an identified domain event [4].

If a reserved Tool becomes out of commission, its outstanding Reservation is cancelled.

A checked-out Tool prevents the Member from reserving or checking out another Tool until that Tool is returned.

A Checkout becomes overdue when its `dueDate` has passed and the Tool has not been returned. Overdue detection is explicitly represented in discovery [4]. Because the Member is already restricted from borrowing an additional Tool while the Checkout remains active, overdue does not require a separate borrowing-restriction state in the current version.

## Behavioral Coverage

Assessment: **PASS**

The vocabulary includes the following agreed Affordances:

- `addTool`
- `searchAvailableTools`
- `reserveTool`
- `cancelReservation`
- `checkoutTool`
- `returnTool`
- `inspectTool`
- `retireTool`
- `addMember`
- `searchForMember`
- `updateMember`
- `searchCheckoutHistory`

These cover the primary discovered Member journey. The discovery artifacts specifically identify searching available tools, reserving a Tool, confirming checkout, returning a Tool, and completing inspection as potential API Story candidates [7].

Tool inventory management is also supported. Discovery assigns responsibility for adding and retiring inventory to the supervisory role [6], and the event inventory contains both Tool addition and Tool retirement [4].

Member-management affordances support the system's maintained list of active and inactive Members.

`searchCheckoutHistory` supports the decision to retain checkout/return records for accountability and historical viewing. Accountability through checkout and return is a principal domain concern [2].

## Inspection

Assessment: **PASS WITH INTENTIONAL SCOPE LIMITATION**

Inspection is behavior in the current vocabulary rather than a persistent historical record.

`inspectTool` represents assessment of a Tool's condition and can result in the Tool being considered `outOfCommission`.

Following return, a Tool normally becomes `available`. Inspection by a Member or Tool Supervisor can instead identify that the Tool should be `outOfCommission`.

No `Inspection` Composite, inspection identifier, inspection timestamp, or inspection-history capability is required in the current version.

This is an intentional scope decision rather than a missing vocabulary concept.

## Checkout History

Assessment: **PASS**

Checkout and return records are retained as viewable history.

Accordingly, `Checkout` contains both checkout and return timing, and `searchCheckoutHistory` provides the domain behavior for finding historical Checkout records.

The affordance intentionally does not yet define whether history is searched by Member, Tool, date, or another criterion. Those interaction details belong to downstream API Story design rather than the Domain Vocabulary.

## Structural Validation

Assessment: **PASS**

The supplied validator report identifies the vocabulary as valid.

Vocabulary Markdown Validator:

- Validator version: 0.6.1
- Format version: 0.1
- PASS: 415
- WARN: 0
- ERROR: 0
- Valid: true [9]

The report confirms the presence of the required document metadata and all five vocabulary sections, including Atoms, Enumerators, Composites, Resources, and Affordances [9].

It also verifies Kind/section consistency, local definitions, uniqueness, and structural rules for individual vocabulary terms [9].

No structural remediation is required before proceeding.

## Deferred Scope

The following capabilities are deliberately outside the current vocabulary scope.

### Repair and Maintenance History

Repair is part of the discovered domain. The source material includes Tools being shipped for repair and returned from repair [4], and lifecycle tracking includes repair [2].

The current version does not model:

- repair records;
- repair history;
- repair shipments;
- external repair organizations;
- detailed maintenance workflows.

These concepts should be revisited if a future API version manages repair activity rather than simply representing a Tool as `outOfCommission`.

### Inspection History

Inspection history is not retained in the current version.

A future version may introduce an Inspection Composite and corresponding historical behavior if condition history becomes a system requirement.

### Notifications

Notifications are deferred.

In particular, the current version can identify an overdue Checkout but does not require notification behavior. Future versions may add overdue, reservation-expiration, repair, or other lifecycle notifications.

## Open Questions

The remaining questions are future-scope questions rather than blockers for the current vocabulary:

1. Will a future version manage repair and maintenance as first-class records and behaviors?
2. Will a future version retain inspection history?
3. What notification behaviors should be introduced when notifications enter scope?

None of these questions prevents the current vocabulary from supporting the agreed API scope.

## Readiness Determination

**READY WITH QUESTIONS**

The Domain Vocabulary is structurally valid and semantically suitable for downstream API Story design.

Its core domain concepts are covered, canonical terminology is sufficiently consistent, controlled values capture the required Tool and Member states, Composites support the required information, and Affordances cover the agreed Tool, Member, borrowing, inspection, and historical-search behaviors.

The Vocabulary Markdown artifact also satisfies deterministic structural validation with no warnings or errors [9].

The outstanding questions concern functionality deliberately deferred to later versions rather than unresolved semantics in the current API scope.

## Recommended Next Step

Proceed to **API Story design** using this vocabulary as the shared domain language.

API Story work can now establish the interaction-specific details intentionally excluded from vocabulary design, including affordance inputs, results, resource relationships, search criteria, and other behavior-specific contracts.

If API Story design exposes a genuinely missing domain concept, that concept should return to vocabulary refinement rather than being introduced silently downstream. The vocabulary coaching guidance explicitly requires returning to refinement when artifact or downstream work exposes a missing term or structural problem [1].
