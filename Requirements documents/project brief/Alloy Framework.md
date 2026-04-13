# Alloy Framework

Alloy Framework is an Apache-licensed model?view?controller application frame- work built on top of Titanium that provides a simple model for separating the application user interface, business logic and data models.

1. The mobile UI developer interacts with the Alloy Framework via a Node.js command-line compiler script. No graphical layout builder or drag-and-drop UI designer is required for this compiler.
2. The developer provides a project directory containing declarative XML markup for views, CSS styling files, and CommonJS JavaScript files for business logic. 
3. The compiler must only process files located on the local disk; fetching remote stylesheets or scripts over the network during compilation is out of scope.
4. The compiler parses the markup and CSS, utilizing a Sizzle-based engine to resolve DOM element selections. It automatically evaluates platform-specific attributes (e.g., data-ti-platform="iPhone") and wraps the corresponding generated code in conditional logic, dropping non-matching nodes from the AST to save memory. For this iteration, assume the maximum allowed depth for nested UI widgets is 10 levels.
5. The compiler merges classes, IDs, and inline styles into unified rules and translates the entire project into standard, imperative Titanium JavaScript API calls. 
6. All generated files are then forcefully written to a designated "generated" folder within the project's Resources directory. Dynamic runtime compilation or evaluation of CSS files on the mobile device itself is out of scope.
