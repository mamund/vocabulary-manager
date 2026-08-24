# Tool Shed Domain Vocabulary

Version: 0.1.0
Status: draft

Vocabulary for a community Tool Shed system in which Members reserve,
check out, and return shared Tools, while Tool Supervisors manage the
inventory and Tool lifecycle.

## Atoms

### toolId

Kind: atom

A stable identifier for a Tool.

### toolName

Kind: atom

The name used to identify a Tool to Members and Tool Supervisors.

### toolDescription

Kind: atom

A description of a Tool and its intended use.

### memberId

Kind: atom

A stable identifier for a Member.

### memberName

Kind: atom

The name of a Member.

### memberEmail

Kind: atom

The email address associated with a Member.

### reservationId

Kind: atom

A stable identifier for a Reservation.

### reservedAt

Kind: atom

The date and time at which a Reservation was established.

### expiresAt

Kind: atom

The date and time at which an unfulfilled Reservation expires.

### checkoutId

Kind: atom

A stable identifier for a Checkout.

### checkedOutAt

Kind: atom

The date and time at which a Tool was checked out by a Member.

### dueDate

Kind: atom

The date and time by which a checked-out Tool is expected to be returned.

### returnedAt

Kind: atom

The date and time at which a checked-out Tool was returned.

## Enumerators

### ToolStatus

Kind: enumerator

The recognized lifecycle statuses of a Tool.

Values:

* available : The Tool is in service and available to be reserved.
* reserved : The Tool is held for a specific Member and unavailable to other Members.
* checkedOut : The Tool is currently borrowed by a Member.
* outOfCommission : The Tool is temporarily unavailable for borrowing because it requires or is undergoing work, either internally or externally.
* retired : The Tool has been permanently removed from service but remains on file for historical purposes. Retirement is irreversible.

### MemberStatus

Kind: enumerator

The recognized participation statuses of a Member.

Values:

* active : The Member may participate in borrowing, subject to borrowing rules.
* inactive : The Member remains on file but cannot reserve or check out Tools.

## Composites

### Tool

Kind: composite

The contextual description of a Tool maintained by the system.

Composition:

* toolId : MUST
* toolName : MUST
* toolDescription : MUST
* ToolStatus : MUST

Additional: MAY

### Member

Kind: composite

The contextual description of a Member maintained by the system.

Composition:

* memberId : MUST
* memberName : MUST
* memberEmail : MUST
* MemberStatus : MUST

Additional: MAY

### Reservation

Kind: composite

A temporary commitment that holds one Tool for one Member.

An active Reservation prevents that Member from reserving or checking
out an additional Tool. The Member may check out the reserved Tool or
cancel the Reservation at any time before checkout. A Reservation can
also expire or be cancelled when its Tool becomes unavailable.

Composition:

* reservationId : MUST
* reservedAt : MUST
* expiresAt : MUST
* memberId : MUST
* toolId : MUST

Additional: MAY

### Checkout

Kind: composite

The record of a Member borrowing a Tool.

A Member may have only one active Checkout. A Checkout becomes overdue
when its dueDate has passed and the Tool has not been returned. Completed
Checkout records remain available as borrowing history.

Composition:

* checkoutId : MUST
* memberId : MUST
* toolId : MUST
* checkedOutAt : MUST
* dueDate : MUST
* returnedAt : MAY

Additional: MAY

## Resources

### tool

Kind: resource

A Tool managed through the planned API.

### member

Kind: resource

A Member managed through the planned API.

## Affordances

### addTool

Kind: affordance

Add a Tool to the managed inventory.

### searchAvailableTools

Kind: affordance

Search for Tools that are available for borrowing.

### reserveTool

Kind: affordance

Reserve an available Tool for an active Member who has no other active
Reservation or Checkout.

### cancelReservation

Kind: affordance

Cancel an active Reservation before its Tool is checked out.

### checkoutTool

Kind: affordance

Acknowledge that a Member has taken possession of the Tool reserved for
that Member.

### returnTool

Kind: affordance

Acknowledge the return of a checked-out Tool.

A returned Tool normally becomes available. It may instead become
outOfCommission when its condition indicates that it should not
continue circulating.

### inspectTool

Kind: affordance

Assess a Tool's condition and determine whether it should remain in
circulation or become outOfCommission.

Inspection history is not retained in this version.

### retireTool

Kind: affordance

Permanently remove a Tool from service while retaining its record for
historical purposes.

Retirement is irreversible.

### addMember

Kind: affordance

Add a Member to the system.

### searchForMember

Kind: affordance

Search for a Member maintained by the system.

### updateMember

Kind: affordance

Update information maintained about a Member, including membership
status.

### searchCheckoutHistory

Kind: affordance

Search retained Checkout records representing Tool borrowing and return
history.
