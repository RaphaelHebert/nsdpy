script: main.py

    INPUTS: 
        -No command line arguments
        -Prompt the user for a query to nulceotide database with the esearch E-utilitie
        -Need an API key for the Entrez API from NCBI
    
    ACTION:

        SEARCH 
            TaxIDs
        -Prompt the user for a phrase to search in the nucledotide database
        -use the esearchquery function to use the esearch E-utiliti from the Entrez API (NCBI)
    esearchquery() return a response in JSON format containing the variable webenv, count (number of results)
    and querykey.
        -the output from the function is converted from the JSON format to a dictionnary
        -the script extract the variables webenv, querykey and count from the dictionnary
        
        DOWNLOADS
            TaxIDs
        -use the taxids function to retreive the taxids from the accession numbers in the taxonomy database using the esummary Esummary E-utilitie
    The Taxids function print a text file with, for each line, an accession number and its corresponding TaxID.
    This file is used later as a reference as it has the same number of unique accession numbers as the number of results returned by esearch
    The function retruns a dictionnary with the accession numbers as keys and the taxids as values
            Taxonomy
        -the script creates a set from the taxids in the dict returned by the taxids function, then cast it to a list
        -the completetaxo2 function is called with the list of unique TaxIDs and the API key as INPUTS
        -the function use the efetch E-utilitie to search the taxonomy database, its returns a dictionnary with the TaxIDs as keys and their Lineage, Name and Division as values
    The function prints a text file containing this dictionnary in JSON format.
            Featuretable
        -call the function feattable with webenv, count, queryid and API key values as INPUTS
        -the function uses efetch E-utilitie to search the nuccore(=nucleotide) database and retreive the results as a Featuretable
    The function prints a text file with the feature table
    The function outputs the file name of the printed text file 

        ANALYSE
            feature table
        -the script calls the function extract2 with the name of the text file containing the feature table, the dictionnary outputed by taxids function and the dictionnary outputed by the completetaxo2 function
        -the function makes a list of the sequences from the feature table and calls the function subextract2
        -the function subextract2 check if the gene is a COI eventually extract it with its location and accession number,
    then from the accession number it retreive the TaxID and the Lineage information from the dictionnaries,
    it finaly appends the COI sequence and a description line in fasta file.
        -the extract2 function returns a list of the accession numbers for which a COI has been found and the name of the text file printed
            remaining accession numbers
        -the script finds the taxids for which no COI has been found by substracting the list of accession number retreived from the dictionnary outputed from the taxids function and the list of accession numbers returned by the extract2 function
        -the script calls the taxo2 function with the list of remaining accession number, the dictionnaries with the TaxIDs and taxonomy information and name of the file to append the results
        -the taxo2 function search the nucleotide database using the efetch e-utilitie to retreive the genbank file (it sends batches of 200 (can be set to more) accession numbers)
    from the genbank file the taxo 2 function look for the coi for each accession numbers and retreive the information: location, DNA sequences..
    it appends the resluts in a fasta-like format to the filen given as Input.
