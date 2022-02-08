# functions.py

The following functions are described here:

- [download](#dowload) 
- [esearchquery](#esearchquery)
- [taxids](#taxids)
- [cds_fasta](#cds_fasta)
- [fasta](#fasta)
- [taxo](#taxo)
- [extract](#extract)
- [subextract](#subextract)
- [genbankfields](#genbankfields)
- [search](#search)
- [tsv_file_writer](#tsv_file_writer)



Define some functions that are used in main.py


The intputs **QUERY**, **OPTIONS** and **params** correspond to tuples that contain:

- **QUERY**:
- query(STRING): phrase the user wants to use to search in the nucleotide database from NCBI in text format
example:

```python
'((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))'
```

- apikey(STRING, OPTIONNAL): api key for for the entrez api from NCBI text format
example:

```python
'66af22581a26c4fdc8e74788e8562502a308'
```

- **OPTIONS**:
- args.cds(LIST): the function should writes a text file with the CDS fasta file, elements of the list will be used as regexp for filter the results
- args.TAXIDS(BOOL):if the function should writes a text file with the accession numbers and their TaxIDS table or not
- verb(INT): verbose or quiet options
- classif (INT, or LIST): if LIST correspont to a list of taxonomic levels names entered by the user, if INT [0, infinite[

- **params**:
-querykey(STRING) the query_key returned by a search with the esearch E-utility in history mode, text format. exp: "1".
-webenv(STRING), the webenv returned by a search with the esearch E-utility in history mode, text format. exp: "MCID_5fdaff9d0aee646a05268177"
-count(INTEGER), the number of of matches returned by a search in esearch E-utility and converted to an integer. exp: 86184

## dowload

```python
download(parameters, address)
```

### INPUTS

- *parameters*(DICT) a dictionnary with the name of the parameters as keys and their value as values
- *address*(STRING) host address

### ACTION

- make a call using the get method from the [requests library](https://requests.readthedocs.io/en/master/) to the *address* provided with the *parameters* 
- loop untils getting an answer from the call, returns 1 if an HTTPerror is raised
- handle errors (such as HTTPerror, network error...), see the [errors](https://requests.readthedocs.io/en/master/_modules/requests/exceptions/) for more information

## esearchquery

```python
esearchquery(QUERY)
```

### INPUTS

- *QUERY*(TUPLE): tuple containing the query and apikey variable. esearch query uses the query and apikey from QUERY

### ACTION

Submit the user's request to the [ncbi esearch engine](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch) with the following parameters:

- *usehistory = y* using history mode allow to get the querykey and webenv number to use in other E-utilities 
- *db=nucleotide* look in the nulceotide database
- *idtype=acc* return accession numbers
- *retmax=0* number of idtype that will be displayed
- *retmode=json* data returned in Json format

### OUTPUTS

- Returns the result of the user's request result as a dictionnary

## taxids

```python
taxids(params, path, OPTIONS)
```

### INPUTS

- *params*(TUPLE): taxids uses *querykey*, *webenv* and *count* from params.
- *path*(STRING), path of the folder to store the results (text and fasta files)
- *OPTIONS*(TUPLE): taxids uses verb and args.TAXID from *OPTIONS*.

### ACTION

- Searches the taxonomy database with the esummary E-utility. It sends queries by batches of 100 (or more: see retmax variable). It then finds the accession number and their corresponding TaxIDs
- if args.TAXID is True (option -T selected) it writes the text file with one accession number and its corresponding TaxID per line.

### OUTPUTS

- (optionnal -T) A text file with one accession number and its corresponding TaxID per line separated by a tab. exp:MW080658   436086.
- A dictionnary with the accession numbers as keys and TaxIDs as values.

## cds_fasta

```python
cds_fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None)
```

### INPUTS

- *path*(STRING): the path of the location where the results are written
- *dict_ids*(DICT): output of taxids() function, dictionnary with accession number as keys and TaxIDs as values
- *QUERY*(TUPLE):  uses the *apikey* 
- list_of_ids: list of accession version numbers to be retrieved
- *OPTION*(optionnal): uses *verb*, *genelist* and *args.CDS* from *OPTION*

### ACTION

- Using the efetch E-utility with list_of_ids it looks in the nuccore (=nucleotide) database to retrieve the CDS fasta file for 100 accession numbers (see *retmax* variable) at the time.
- Call the extract function to analyse the results from Entrez API (everytime Entrez returns some results).

### OUTPUTS

It returns the list of the accession number for which a CDS have been found.

## fasta

```python
fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None)
```


### INPUTS

- *path*(STRING): the path of the location where the results are written
- *dict_ids*(DICT): output of taxids() function, dictionnary with accession number as keys and taxids as values
- *QUERY*(TUPLE):  uses the *apikey* 
- *list_of_ids*(LIST): list of accession number for which the fasta files must be retrieved
- *OPTIONS*(optionnal):uses *verb* and *fileoutput* from *OPTIONS*

### ACTION

Using the efetch E-utility with the parameter from params it looks in the nuccore (=nucleotide) database to retrieve the fasta file for 10 accession numbers (see retmax variable) at the time. If fileoutput is True it writes the results in a fasta file. It writes the results in one or more fasta file (depending on the taxonomy option) and add the taxonomy information to information line.

### OUTPUT

It returns the list of the accession number for which a sequence have been found.

## taxo

```python
taxo(path, list_of_ids, dict_ids, QUERY, dict_taxo=None, OPTIONS=None)
```

### INPUTS

- *path*(STRING) see above
- *list_of_ids*(LIST) list of the accession numbers for which no COI have been found 
- *dict_ids*(DICTIONNARY) see above
- *QUERY*(TUPLE): uses the *apikey* from *QUERY*
- *OPTIONS*(TUPLE): uses *verb*, *genelist* and *classif* from *OPTIONS*

### ACTION

- query Entrez API with the efetch tool to search the nucleotide database from NCBI and retreive a genbank file. Send 10 (retmax variable) accession numbers at the time, send some queries until no more accession number are left from the listofid. Use the requests librairy to send get requests to Entrez API.
- split the received text (.gb format) every '\n//' to get a list.
- iterate over the list calling the genbankfields function to get a list of dictionnary and the DNA sequence as a string
- iterate over the list resturned by genbanfields function
- get the information from the dictionnaries and writes the ouput file(s)
- calls the dispatch function with the classif parameters
- makes a list of the accession version number with sequences printed in the output file

### OUTPUT

- a list of the accession version numbers for which one or more sequence s have been written in the output file(s)
- a list of the accession version numbers for which a genbank file have been downloaded
- writes in the output file called **notfound.txt** the accession version numbers for which no sequences has been written in the output file or with no genbank file downloaded.

## extract

```python
extract(path, text, dict_ids, dict_taxo, genelist, verb)
```

### INPUTS

- *path*(STRING): see above
- *text*(STRING): CDS fasta file in text format, results of the call to nuccore database made by the cdsfasta function.
- *dictid*(DICTIONNARY) see above
- *dicttaxo*(DICTIONNARY) see above
- *genelist*(LIST) from *OPTIONS*, see above 
- *verb*(INT) from *OPTIONS*, see above

### ACTION

- Iterates over each gene of the text variable
- for each gene sequence (+ information line) calls the subextract function.

### OUTPUTS

- a list of the accession numbers for which a gene (from genelist) have been found (LIST)

## subextract

```python
subextract(seq, path, dict_ids, dict_taxo, genelist)
```

This function is called by the extract function.

### INPUTS

- *seq*(STRING): the gene sequence with its information line
- *path*(STRING): see above
- *dict_ids*(DICTIONNARY): see above
- *dict_taxo*(DICTIONNARY): see above
- *genelist*(LIST): see above

### ACTION

- extracts the accession number 
- retrieves TaxID from dictid
- retrieves taxonomic informations from dicttaxo, if no information are found in dictaxo (keyerror) it returns (so the accession number will be searched later with the taxo function and these infos will be retrieved from the genbank result)
- check if the gene is in genelist
- if the gene matches, the location information is extracted from the information line.
- else it returns
- the results is appended to the fasta file given as input base on the dispatch values from dicttaxo parameter

### OUTPUT

- returns the accession number(STRING)

## genbankfields

```python
genbankfields(text, genelist)
```

This function is called by the taxo function

### INPUTS

- *text*(STRING) the text of a genbank file
- *genelist*(LIST) a list of regexp to be used as filters

### ACTION

- extract the accession version number, DNA sequence, organism name and lineage from the text then add these in a dict
- split the text every "  gene  " and iterate over the list of result calling the search function and splitting the results every "  CDS  " to iterate over these results calling again the search function
- from the calls to search function it gets two dictionnaries: one for the "  gene  " sequence and one for "  CDS  " sequence. 
- if one or more filter is provided in the genelist: for each CDS sequences, looks for a match between the filters and the "gene", "product", "gene_synonym" and "note" fields from the Genbank file.if no mtach found it compares the start and stop of the location field from the "  gene  " and the "  CDS  " file are the same it looks for a match in the gene sequence fields. If a mtach is found it writes the dictionnary containing the cds sequence informations is appended to the list of dictionnares the function will return.
- if no filter is provided the the dictionnary containing the cds sequence informations is directly appended to the list of dictionnares the function will return.

### OUTPUTS

- list of dictionnaries (LIST)
- DNA sequence (STRING)

## search

```pythhon
search(dna, dictentry, s)
```

This function is called by the genbankfields function

### INPUTS

- *dna* (STRING) the dna sequence from the genbank file
- *dictentry* (DICTIONNARY) a dictionnary containing the information from the genbank file extracted by the genbankfield function.
- *s* (STRING) the part of the genbank file to analyse

### ACTION

- extract the location and the corresponding dna sequence, product, protein_id, gene, note, gene_synonym and locus_tag information form the corresponding fields found in the genbank file
- duplicates the dictentry and append the all the extracted informations to it.

### OUTPUT

- dict1 (DICTIONNARY) a dictionnary containing all the informations extracted from the genabnk file.


## tsv_file_writer
  
```pythhon
search(dna, dictentry, s)
```

### INPUTS

- *path*(STRING): see above
- *data*(tuple): (name(STRING), seqid(STRING), taxid(STRING), lineage(STRING), dna(STRING)) data to be written in the tsv file
- *OPTIONS*(TUPLE): see above
  
### ACTION 
  
Writes or append a  file located at path with the information found in data  
  
### OUTPUT
  
no output
