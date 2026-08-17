# Minimal Vocabulary

Version: 0.1.0
Status: draft

## Atoms

### toolId

Kind: atom

A stable identifier for a tool.

## Enumerators

### ToolCondition

Kind: enumerator

The recognized conditions of a tool.

Values:

* available : The tool is available.

## Composites

### Tool

Kind: composite

A contextual description of a tool.

Composition:

* toolId : MUST

Additional: MAY

## Resources

### tool

Kind: resource

A tool resource concept.

## Affordances

### readTool

Kind: affordance

Retrieve information about a tool.

Returns: tool
