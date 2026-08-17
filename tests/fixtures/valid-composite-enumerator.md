# Composite Membership Vocabulary

Version: 0.1.0
Status: draft

## Atoms

### toolId

Kind: atom

A stable identifier for a tool.

## Enumerators

### ToolStatus

Kind: enumerator

The recognized lifecycle status of a tool.

Values:

* available : The tool is available for use.
* reserved : The tool is reserved for a member.

## Composites

### Tool

Kind: composite

A contextual description of a tool.

Composition:

* toolId : MUST
* ToolStatus : MUST

Additional: MAY

## Resources

### tool

Kind: resource

A tool resource concept.

## Affordances

### readTool

Kind: affordance

Retrieve information about a tool.
