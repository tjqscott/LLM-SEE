# Atlassian Software Server

Atlassian Jira is a proprietary issue tracking product developed by Atlassian that allows bug tracking and agile project management.

1. The agile project manager interacts with the Atlassian Jira Software Server via a web-based graphical interface, specifically utilizing the GreenHopper agile board views.
2. The manager defines project workflows and creates task issues. Issues are visually represented as cards on a planning board. Assume a single board will display a maximum of 1,000 active issues.
3. The system must allow the manager to edit issue details, component assignments, and version release dates directly from the card interface via AJAX, without requiring full page reloads.
4. Developers log execution time against parent issues and subtasks. The core calculation engine must aggregate the logged time across both levels to maintain accurate velocity tracking. Cross-project aggregation or multi-project portfolio reporting is out of scope for this version; calculations are strictly bounded to a single project.
5. The system utilizes the logged time and task state changes to dynamically render a Burndown Chart. The mathematical calculation must be strictly synchronized to prevent duplicate change logs from skewing the velocity statistics.
