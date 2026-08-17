# Tool Shed Vocabulary

Version: 0.2.0
Status: draft

A comprehensive vocabulary fixture.

## Atoms

### toolId

Kind: atom

A stable identifier for a tool.

### toolName

Kind: atom

The human-readable name of a tool.

External:

* Source: Schema.org
  URI: https://schema.org/name

### memberId

Kind: atom

A stable identifier for a member.

### dueDate

Kind: atom

The date by which a reservation is due.

## Enumerators

### ToolCondition

Kind: enumerator

The recognized condition values for a tool.

Values:

* available : The tool is available.
* reserved : The tool is reserved.
* maintenance : The tool is undergoing maintenance.

## Composites

### Reservation

Kind: composite

A reservation of a tool by a member.

Composition:

* memberId : MUST
* dueDate : SHOULD

Additional: MAY

### Tool

Kind: composite

A contextual description of a tool.

Composition:

* toolId : MUST
* toolName : SHOULD
* Reservation : MAY

Additional: MAY

## Resources

### tool

Kind: resource

A tool resource concept.

### reservation

Kind: resource

A reservation resource concept.

## Affordances

### readTool

Kind: affordance

Retrieve information about a tool.

### reserveTool

Kind: affordance

Reserve a tool for a member.
