# main.py

## INPUTS

### Help:

**help:** display the help
```bash
-h or --help 
```

### POSITIONNAL ARGUMENTS

#### Query to NCBI:

**query:** The user's query as first command line argument (the query as the user would enter it in the NCBI search engine).

```bash
-r USER`'S QUERY or --request USER`'S QUERY
```

### OPTIONNAL ARGUMENTS

#### API key

**apikey:** The user's NCBI API key. Get an API key by registering to NCBI [here](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/#:~:text=To%20create%20the%20key%2C%20go,and%20copy%20the%20resulting%20key.) and [Register to NCBI](https://www.ncbi.nlm.nih.gov/account/register/)

```bash
-a API KEY or --apikey API KEY
```

#### Verbosity

**Verbose:** display more comments in the terminal

```bash
-v or --verbose 
```

**Quiet:** display less comments in the terminal

```bash
-q or --quiet 
```

#### Download and analyse

**cds:** download the cds_fasta files. Uses  PATTERNS  as filter to filter the sequences in the cds_fasta files. PATTERNS are used as regexp.

```bash
-c PATTERNS or --cds=PATTERNS 
```

**TaxIDs:** writes a text file with all the accession numbers and their corresponding taxids found by the esearch query
    Taxonomy Options

```bash
-T --TAXIDS 
```

#### Sort

If any of the sorting options is selected the taxonomy information (lineage and organism name) will be added to the information lines of the output file(s)

**Informations:** the taxonomy information are added to the information line of the output file. All the sequences are written in the same file.

```bash
-i or --information
```

**Kingdom:** sort the sequences by kingdoms, write one output file per kingdom (METAZOA, PLANTAE, FUNGI, OTHERS)

```bash
-k or --kingdom
```

**Phylum:** sort the sequences by phylums, write one output file per phylum. The phylums are hardcoded in the dispatch function in the functions file

```bash
-p  or --phylum
```

**Levels:** sort the sequences by levels, write one output file per level provided by the user

```bash
-l LEVELS or --levels=LEVELS
```

**Species:** sort the sequences by spcies, write one output file per specie. takes the lowest level in the sequence taxonomy plus n, exp: -sss will select the thrird lowest level in each sequence taxonomy. (it will write as many text files as different levels are found)

```bash
-s or --species
```

#### Summary

**Summary:** summarize the run in the text file located in the working directory. The file keep trace of all the runs with this option

```bash
-S or --SUMMARY
```

## ACTION

### SEARCH

- calls the esearchquery function with the user's query (first command line argument) to use the esearch E-utility from the Entrez API (NCBI)
- esearchquery() returns a dictionnary as response containing the variable webenv, count (number of results) and query_key as keys and their values as values.
The webenv and query_key to send the access numbers of the results directly to efetch and esummary.
- the script extract the variables webenv, querykey and count from the dictionnary

## DOWNLOADS and FILTER

### TaxIDs

- calls the taxids function to retrieve the TaxIDs and extract the accession numbers corresponding to the esearch result with the webenv and query_key variables. The taxids function uses esummary to search the taxonomy database.
The Taxids function prints a text file with, for each line, an accession number and its corresponding TaxID.
This file is used later as a reference as it has the same number of unique accession numbers as the number of results returned by esearch
The function retruns a dictionnary with the accession numbers as keys and the taxids as values.

### Taxonomy

If any of the taxonomy option is selected this step will be run otherwise it will be omitted.

- the script creates a set from the taxids in the dict returned by the taxids function, then cast it to a list
- the completetaxo function is called with the list of unique TaxIDs and the API key (if provided) as INPUTS
- the function use the efetch E-utility to search the taxonomy database, its returns a dictionnary with the TaxIDs as keys and their Lineage, Name and Division listed as values

### cdsfasta

If the option ``` -c ``` or ```--cds``` is selected this function will be run instead of the fasta function.

- the function uses efetch E-utility to search the nuccore (=nucleotide) database and retreive the results as a cds_fasta file in text format, then call the extract function with this result.
- the function outputs a list of the accession number for which the targeted gene(s) has been found if some PATTERNS are provided, if no PATTERNS are provided it returns a list of the accession version number for which a cds_fasta file has been found.

### fasta

If the option ```-c``` or ```--cds``` is not selected the fasta function will be run as default.

- the function uses efetch E-utility to search the nuccore (=nucleotide) database and retreive the results as a fasta file in text format (if fasta option is selected it download the fasta files), then append the results to the fasta file(s)
- the function outputs a list of the accession number for which a file has been found.

### taxo

Only calld it the ```-c --cds``` option is selected.

- the script calls the taxo function with the list of remaining accession version numbers, the dictionnaries with the TaxIDs and taxonomy information and name of the file to append the results
- the taxo function searches the nucleotide database using the efetch e-utility to retreive the GenBank file (.gb), it sends batches of 10 (can be set to more changing the retmax variable value) accession version numbers to efetch.
- split the text results by accession version numbers and send this results to the genbankfields function to get a dictionnary containing the informations to be written in the output file(s).
- the genbankfields function calls the search function, these functions will extract the informations from the genbank file and select the sequences to be written in the output file(s)
- return a list of the accession version number for which a GenBank file has been downloaded and a list of the vesrion accession numbers for which one or more sequences have been written in the output file(s).

### REPORT

If the ```-q``` or  ```--quiet``` option is not selected:

- summarize the results in the terminal
- display the ending time

If the ```-S``` or  ```--SUMMARY``` option is selected:

- writes or appends the information of the run in a text file located in the working directory.
