# Tool Shed Domain Vocabulary

Version: 0.2.0
Status: draft

This vocabulary defines the local semantic terms used to design the Tool Shed API. It is a design vocabulary, not a representation schema.

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

### toolCondition

Kind: atom

The current physical condition of a tool.

### memberId

Kind: atom

A stable identifier for a Tool Shed member.

### reservationDueDate

Kind: atom

The date by which a reserved tool is expected to be returned.

## Enumerators

### ToolCondition

Kind: enumerator

The recognized condition values for a tool.

Values:

* available : The tool is available for normal use.
* reserved : The tool is currently reserved.
* maintenance : The tool is unavailable while maintenance is performed.
* retired : The tool is no longer available for use.

## Composites

### Tool

Kind: composite

A contextual description of a tool used within the Tool Shed domain.

Composition:

* toolId : MUST
* toolName : MUST
* toolCondition : SHOULD
* Reservation : MAY

Additional: MAY

### Reservation

Kind: composite

A contextual description of a reservation for a tool.

Composition:

* memberId : MUST
* reservationDueDate : SHOULD

Additional: MAY

## Resources

### tool

Kind: resource

A named API resource concept representing a tool managed by the Tool Shed.

### reservation

Kind: resource

A named API resource concept representing a tool reservation.

## Affordances

### readTool

Kind: affordance

Retrieve information about a tool.

### reserveTool

Kind: affordance

Reserve a tool for a member.

### returnTool

Kind: affordance

Return a previously reserved tool.

### setToolCondition

Kind: affordance

Change the recorded condition of a tool.
