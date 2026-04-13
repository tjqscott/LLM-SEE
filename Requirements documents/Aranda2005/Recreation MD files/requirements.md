# Toronto Foreign Trade Statistics System

## Software Requirements Initial Report


## Table of Contents

- 1. Introduction
   - 1.1 The Project at a Glance
   - 1.2 Definitions, acronyms, and abbreviations.
   - 1.3 Overview.
- 2. Requirements description.
   - 2.1 FTSS and its environment.
   - 2.2 Product functions.
- 3. Other considerations.
   - 3.1 Reliability of reports
   - 3.2 Information volume
   - 3.3 User interface
   - 3.4 User characteristics
   - 3.5 Programming language constraints
   - 3.6 Process requirements


## 1. Introduction

This document describes the requirements of a system to help the Toronto Foreign Trade Agency, a
municipal public office, to analyze and report statistics on foreign trade of Toronto- and GTA-based
companies.

### 1.1 The Project at a Glance

The software to be produced will be named _Foreign Trade Statistics System_ , and will be referred to as
FTSS in the rest of this document.
The main purpose of the FTSS is to receive, store and process federal data about foreign trade
engaged by Toronto- and GTA-based organizations; serving as a statistics generation tool for users
to analyze its information and produce official, municipality level foreign trade reports.
The client organization currently owns and operates a software tool that is used for this purpose;
but its age and its design inadequacies became evident as the database size and query complexity
increased, and it is now obvious that it will be obsolete relatively soon. The FTSS will therefore
phase out the previous system.
The high-level goals of the new system are:
a. To reduce the time it takes for office staff to produce and deliver _standard_ reports; from an
average of 1 hour to an average of 10 minutes. The following subsection has more details on
standard reports.
b. To reduce the time it takes for office staff to produce and deliver _custom_ reports; from an
average of 12 hours to an average of 15 minutes. The following subsection has more details
on custom reports.
c. To increase the confidence of the reports; from the present 97.5% (one faulty report in forty)
to 99.9% (one faulty report in one thousand) or better.
d. To provide a new web service that allows Internet users to post –relatively- simple queries
to the system through the Toronto Foreign Trade Agency website.
e. To reduce system downtime, through proper software design and a robust implementation,
to at most an hour of downtime each three months.
f. To allow the Statistics Staff, through the fulfillment of the previous objectives, to spend
more of their time on statistics analysis and less on statistics production.
Note that the system currently being used has the functionality to produce standard reports.
Although the system is slow, the reasons why it presently takes an average of one hour to produce
them are the need to review them thoroughly because of a history of error-prone reports, and the
need to format them in the way upper management wants them (with neatly arranged and


coloured Excel files). Note as well that the time it takes to deliver custom reports is so long (
hours on average) because the present system does not provide the functionality to produce them at
all. The statistics staff have to plunge into reams of reports and perform calculations by themselves
to obtain the desired information, and then format it the way the Agency requires.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and
the specifications:

- _Custom report_ – A statistical report that is not part of the basic set of _standard_ reports (see
    below) and which links any two or more relevant factors of a statistic. Non-comprehensive
    examples of custom reports are:
       + A list of the top ten countries to which there were exports from Scarborough
          during 2003, with export volumes.
       + Names of the top five companies from the GTA that imported European machinery
          in the last five years.
       + Transaction amount of exports from the GTA grouped by company size categories
          and presented a month per column, from January 2002 to date.
       + A comparison of the volume of imports processed at each official customs port,
          with yearly columns from 1999 to 2003.
       + A matrix showing the amount for the transactions made from every region of the
          world (Europe, Latin America, etc. –defined by user) to each section of the Greater
          Toronto Area for 2002.
       + A list of the 100 most exported and 100 most imported goods (from an official
          federal catalogue), based on number of transactions, during Jan-Apr 2004.
- _Exports_ – Commercial transaction in which goods are transferred from Canada to another
    country.
- _Foreign Trade_ – An interchange of goods and money between two companies based on
    different countries. We will be only concerned with the foreign trade between GTA-based
    companies and foreign companies.
- _FTSS_ – Foreign Trade Statistics System; the software product this document is concerned
    with.
- _Imports_ – Commercial transaction in which goods are transferred to Canada from another
    country.


- _Standard report_ – A statistical report that is typically produced each month with the new
    information available. It is delivered as a neatly formatted MS Excel file, and it is sent to the
    media and compiled in regional statistics books. There are 32 standard monthly reports,
    and 18 more standard annual reports. Examples of standard reports are:
       + A list of total exports grouped by country, from the beginning of this year to date,
          compared to the same period of last year.
       + A list of total imports grouped by type of goods (predefined, standard) for each
          month of the present year.
- _Toronto Foreign Trade Agency –_ The client organization.

### 1.3 Overview.

The rest of this document contains the required specification for the software. Section 2 presents the
requirements of the system, and Section 3 mentions other necessary considerations.


## 2. Requirements description.

The description of the intended product is detailed in the following subsections.

### 2.1 FTSS and its environment.

The following description outlines the intended relationship between the FTSS and its surrounding environment:

- Companies data flows from Human Resources Canada to the FTSS.
- Foreign trade data (monthly) flows from International Trade Canada to the FTSS.
- The FTSS provides Toronto’s foreign trade information to the general public (direct inquiry or website).
- The FTSS provides foreign trade information for internal usage within the Toronto Foreign Trade Agency.



**Figure 1 – FTSS Product Perspective**
The main inputs to the FTSS come from two federal agencies. One of them, Human Resources
Canada, provides company data regarding every organization registered in Toronto and the GTA.
The other, International Trade Canada, provides monthly foreign trade data of Toronto and GTA-
based companies. It is the job of the system and its users to analyze and process the data, generate
reports based on them, and deliver the reports to the general public or for internal usage.
The following items are relevant to this perspective of the system:
a. Both the companies data and the foreign trade data are received by courier, on a CD with
predefined format files.
b. The companies data is received whenever it is requested; typically once every two months.
c. The foreign trade data is received monthly.
d. The Trade Agency generates standard official reports each month (see section 1.3). These
reports are used by other staff at the Agency, and are available through the Agency website
and in print.
e. The Agency generates custom reports as well (see section 1.3), both for the general public
and (more commonly) for internal usage.
f. The Statistics Office, which produces these reports, is only one of several departments of
the Agency. Other foreign trade related departments within the Agency include: GTA


```
Promotion, Foreign Trade Training and Federal Link offices. These departments need the
information generated by the Statistics Office, and often request custom reports from it.
```
### 2.2 Product functions.

The main functional requirements of the system are:
a. The FTSS shall provide an interface to receive Companies Data from a CD, detect and filter
out inconsistencies in the CD file (which are known to happen) and update its own
companies information. Company data include names, addresses, telephone and fax
numbers, e-mails, company size and main businesses. This interface shall be as easy to use
as executing a menu option.
b. The FTSS shall provide an interface to receive Foreign Trade Data from a CD, which shall
work in the same way as the Companies Data interface. Foreign Trade Data consist of one
record per transaction, and each transaction has the fields: Date of transaction, type of
transaction (import/export), GTA company in charge of the transaction, type of goods
traded (from a catalogue), units and quantity, transportation method, country of
origin/destination, customs office that dealt with the merchandise and monetary value of
the transaction. Sometimes International Trade Canada sends transaction information that
does not correspond to GTA companies. These records should be filtered out of the
database.
c. The FTSS shall provide the capability of obtaining standard reports in 2 minutes in average
(without including user revision of the report, which will take about 8 more minutes
approximately). Standard reports shall be formatted in a MS Excel file format by the
system. Please see Section 1.3 for more details. This function should work the following
way: The user will be presented a choice of all possible standard reports (50 options in
total), will choose one of them, and select the time period for which (s)he wants the
information. The software should obtain the necessary information and prepare a MS Excel
file with all proper format, ready to be revised and submitted.
d. The FTSS shall provide the capability of obtaining custom reports in 5 minutes in average
(without including user revision of the information, which will take about 10 more minutes,
approximately). Custom reports are presented in MS Excel files, but they do not need the
fancy formatting that standard reports feature. Please see Section 1.3 for more details. This
function should work the following way: The user chooses a type of report (list, cross table,
etc), chooses the grouping of information (s)he is interested in, the time periods which
should be included and any relevant constraints. Choices for information grouping are


countries, world areas, GTA sections, types of goods, company size, customs offices,
method of transportation, company name and postal code. Examples of constraints are:
[Types of goods: Food]; [Company size: Not small]; [Method of transportation: Train or
ship]; and [Postal code: {list of codes}]. Furthermore, the user should be given the option to
save the settings of the custom report (s)he created, so that (s)he can go back to it later,
regenerate or reprint it, or change some of the constraints to produce a different report.
e. The FTSS shall provide a web service that allows Internet users to post queries, similar to
those prepared by standard reports, and obtain official information on foreign trade.
f. The FTSS shall provide database backup and restoration features.
g. The FTSS shall provide means to update the basic information it needs to work. This
information shall be available to users to add new elements, update existing elements or
delete no longer needed elements. The types of elements to be considered are:
+ Countries
+ World areas,
+ GTA sections
+ General types of goods
+ Detailed catalogue of types of goods (with more than 50,000 entries)
+ Valid trading units (kilograms, pounds, etc.)
+ Recognized customs offices
+ Means of transportation.
h. The FTSS shall provide detailed company data. In some situations, the Agency finds that a
company handles part of its foreign trade transactions from the GTA and part from other
regions. If this is the case, the user should be able to update the company information, and
to specify to the system that only (a) a percentage of the total transactions of the company,
or (b) a list of detailed types of goods, should be considered when producing foreign trade
information from that company.
i. The FTSS shall provide user access control and permissions management, since the
information it handles is confidential and delicate. As to this moment it has not been
defined if the data will have to be encrypted to protect it.


## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system
and on characteristics of its environment

### 3.1 Reliability of reports

Reliability of reports has a high priority. The system should guarantee total accuracy in at least
99.9% of the reports it generates. Consider that the information that the Agency receives is
sporadically inconsistent. If that is the case, the system should detect the inconsistencies and notify
the users about them.

### 3.2 Information volume

The system should be able to handle at least 15 years of information without failing the time
constraints expressed in the objectives section of this document. It is important to consider that 15
years of information may easily extend to several tens of gigabytes of memory.

### 3.3 User interface

The client organization expressed repeatedly that the user interface of the system should also be a
priority, and that it should not only be friendly and agile, but elegant and adherent to the color
code of the Agency. The software should be usable by an average user with two two-hours training
sessions up to 95% of its functionality. The system should also provide clear and detailed online
help so that a user that has had only two training sessions can find his way on the system by
himself.

### 3.4 User characteristics

The intended users of the FTSS are a subset of the staff of the Agency, and the general public
through the Agency website. The expected characteristics of the users are:
+ Familiar with the Windows operating system, which presently is the only one used in
the Statistics Office
+ College or university educational level
+ Not familiar with any database system nor programming language


It is expected that about 3 persons will use the software concurrently. However, the software
should be designed to support at least 10 simultaneous users.

### 3.5 Programming language constraints

The programming language to be used has been already selected to be Visual C++ .NET, as a
contract condition pushed by the IT staff of the Agency. As a similar condition the backend for the
database will be SQL Server 2000. The IT staff did not express an opinion on the choices for script
languages for the web services required.

### 3.6 Process requirements

Once that the Agency and the development team agree on time and cost figures for the software,
the project leader will need to present weekly progress reports to the statistics office manager, both
in writing and in person.


