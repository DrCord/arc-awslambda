# Lambda Deprecation

Functions, utilities and other artifacts in this repository must go through a deprecation review prior to deletion in order to ensure safe removal. The review process consists of:

- Investigation
  - The process begins with identifying a candidate for removal. This is a fairly informal investigation to determine if deprecation is worth pursuing, or even possible. Identification begins with a Jira ticket, where findings are collected.
  
  - If initial investigation determines deprecation is infeasible, the Jira ticket is closed and the process ends.

  - If worth pursuing, the results of this investigation are collected in the Jira ticket for review, the candidate is added to the Proposed list, and is brought to the team for discussion.

- Proposed
  - New proposals are discussed with the team to share findings from the investigation.
  
  - If approved, a deeper investigation into the extent of the changes necessary to deprecate takes place. This includes finding all dependencies, reverse dependencies and other references that will need to be updated in support of the deprecation.
  
  - If the cost of deprecation is too high, this is noted in the Jira ticket, and the item is removed from this list.

  - If cleared to proceed, two new linked Jira ticket are created: One for deprecation and one for removal.

    - The deprecation ticket includes all details necessary to properly document the deprecation and to facilitate proper notification.

    - The removal ticket carries forward all collected details required for removal.

- Deprecated
  - Deprecation covers all documentation and notification processes.

  - A clear deprecation duration should be determined (eg, date based, release based, etc). Depending on the effort required to extricate the item from the repository, the duration of this period will vary. This duration is noted in the removal Jira ticket.

  - When all documentation has been completed and all notifications delivered the deprecation ticket is closed and the item is moved from the Proposed Deprecations list to the Deprecated list.
  
  - The item will remain on this list until the term has elapsed, at which point it will be ready for removal.

- Removed
  
  - Once the deprecation period has elapsed, removal can proceed. The previously created Jira ticket containing removal details is assigned and scheduled.

  - The item is removed from the repository, AWS resources are cleared and any other work identified during the investigation period is performed.
  
  - The function is removed from the Deprecated list, and the Jira ticket is closed.

## Deprecated

- None

## Proposed Deprecations

- None
