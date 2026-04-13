As a consequence of RFC-345, this ticket adds the {{verify}} and {{verify_metrics}} packages to {{lsst_distrib}}.
As a pre-processing step before extracting other LaTeX commands, metasrc should filter the latex source:    - remove comments  - add input/included tex files.  - replace simple macros (those made with {{\def}} and {{\newcommand}}).
As a self-contained module within {{ap_verify}}, {{ingestion}} should have unit tests of its functions. It may be possible to implement a unit test by specifically ingesting only 1-2 files of each type.
As an author, provide feedback on the SPIE 2018 paper.
As a result of DM-15553, we will now require {{cffi}} in order to build GalSim in the stack.  This should be added to the list of required conda packages in lsstsw.
As an invited speaker, I've accidentally signed up to write a 10-page paper, and that needs to get through the LSST publication process by Nov. 9.  Might as well write (most of) the talk at the same time.    This issue captures the first draft of that, up through submission to the LSST Pub. Board.
As a first step to getting spatial queries to work, we should enable end users to use the qserv functions through the TAP interface.  This means adding a list of functions to the parser, and getting the plumbing right.  Once we do this, then we can rewrite ADQL spatial functions to use the qserv functions.
As all releases, also the 17.0.1 patch release shall have a corresponding document. However, having a full detailed release note like a major release, it is excessive, since we are just fixing one issue.    My suggestion is to create a subsection inside the major 17.0 release note page.
As a user, I need to know how to:  * Install EUPS itself * Install new packages * Setup packages * Selectively override a package being setup-ed
As an initial setup towards Gen3-ification of the {{pipe_analysis}} scripts, audit all usage of {{butler.get()}} to get a feeling for how easy it will be to convert them to Gen3-land.
