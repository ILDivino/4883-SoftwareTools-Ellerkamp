## Project A06 - Software Tool Presentation
#### Name: Michael Ellerkamp
#### Description: OpenRefine presentation

|   #   |    File     |      Description                           |
| :---: | ----------- | -------------------------------------------|
|   1   |   [Airport_codes.json](Airport_codes.json)   | Familiar data file to mess with.   |
|   2   |   [Mockaroo_family_tree_2.csv](Mockaroo_family_tree_2.csv) | Better data for custom facets examples |
|   3   | [Periodic Table of Elements.csv](Periodic-Table-of-Elements.csv) | for reconcile data showcase |
Major topic: OpenRefine
Relevance: Processing large amounts of data.

1. facets: 
    airport codes for these examples
    //make sure to edit cells with numbers to be numerical cells.

    text facets like country and city (easily see airports per country in the data)

    numerical facets like lat and long (see all airports within a grid area)

    Scatterplot facets for identifying groups of data.

    Custom facets:
    Uses Jython so imports will have to be done through jython pip installation.
    use family tree data.
    Edit columns on first and last name with a " " separator to mess up data
    example facet: return value.split(" ")[1] //this will have issues with 2 word last names.
    regex version of facet: value.find(/[ ].*/) grel
        Jython can be used as well which allows the import of re and using return function calls.
    People with 2 word last names now properly split.

    standard checking for duplicate data.
    true = duplicates

    Filter with regular expressions as well.
    ([a-zA-Z0-9_\-\.\+]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z0-9\-]{2,15})
    would be a filter for properly formatted email addresses.
    Invert to find all improper emails.
    In last name column a simple [ ] will find the ones with 2 word last names.
2.
    Pulling from web.
    put "Q1125633" into a column, then spawn a web column from that column.
    "https://www.wikidata.org/wiki/Special:EntityData/" + data + ".json"
    value.parseJson().Results.county[0].fips

    https://libjohn.github.io/openrefine/hands-on-web-scraping.html#api-1
3.
    reconcile data:
    periodic table of elements
    reconcile with either name or atomic number then add columns via the reconciled data.
1. clustering
    https://openrefine.org/docs/technical-reference/clustering-in-depth