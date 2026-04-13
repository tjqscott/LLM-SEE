# DotNetNuke Platform

DNN is a web content management system and web application framework based on the .NET Framework.

1. The web content administrator interacts with the DotNetNuke (DNN) Platform via a web-based administration console to manage multi-tenant websites.
2. The "Host" administrator creates isolated "Portals" (child websites) within a single SQL Server database. The system enforces strict user quotas on each Portal to prevent resource monopolization. Assume a single installation will manage 1 Host and a maximum of 10 Child Portals. Complex e-commerce checkout workflows or billing integrations are out of scope.
3. Portal administrators create page hierarchies and utilize a RadEditor HTML provider to input rich text and upload media assets. 
4. The system must support Content Localization, creating specific mapped content records based on the user's selected language culture without duplicating the entire page hierarchy.
5. At runtime, the IIS web server intercepts incoming requests, determines the target Portal and language context, and dynamically wraps the localized content in the assigned HTML5/CSS skin. The rendering engine must support pane-level skinning, allowing administrators to inject specific CSS classes into individual content blocks.
