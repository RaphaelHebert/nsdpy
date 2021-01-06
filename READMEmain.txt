script: main.py

    INPUTS: 
        -takes the user's query as first command line argument (the query as the user would enter it in the NCBI search engine)
        -optionnaly takes API key as second command line argument
       
       
    ACTION:

        SEARCH 
            
        -calls the esearchquery function with the user's query (first command line argument) to use the esearch E-utility from the Entrez API (NCBI)
    	-esearchquery() returns a dictionnary as response containing the variable webenv, count (number of results) and query_key as keys and their values as values.
The webenv and query_key to send the access numbers of the results directly to efetch and esummary.
        -the script extract the variables webenv, querykey and count from the dictionnary
        
        DOWNLOADS
            TaxIDs
        -calls the taxids function to retrieve the TaxIDs and extract the accession numbers corresponding to the esearch result with the webenv and query_key variables. The taxids function uses esummary to search the taxonomy database.
    The Taxids function prints a text file with, for each line, an accession number and its corresponding TaxID.
    This file is used later as a reference as it has the same number of unique accession numbers as the number of results returned by esearch
    The function retruns a dictionnary with the accession numbers as keys and the taxids as values
            Taxonomy
        -the script creates a set from the taxids in the dict returned by the taxids function, then cast it to a list
        -the completetaxo function is called with the list of unique TaxIDs and the API key (if provided) as INPUTS
        -the function use the efetch E-utility to search the taxonomy database, its returns a dictionnary with the TaxIDs as keys and their Lineage, Name and Division listed as values
            Featuretable
        -call the function feattable with webenv, count, query_key and API key (if provided) values as INPUTS
        -the function uses efetch E-utility to search the nuccore (=nucleotide) database and retreive the results as a Featuretable
    The function prints a text file with the feature table
    The function outputs the file name of the printed text file 
        ANALYSE
            feature table
        -the script calls the function extract with the name of the text file containing the feature table, the dictionnary outputed by taxids function and the dictionnary outputed by the completetaxo function as INPUTS
        -the function makes a list of the sequences from the feature table and calls the function subextract
        -the function subextract checks if the gene is a COI eventually extracts it with its location and accession number,
    then from the accession number it retreive the TaxID and the Lineage information from the dictionnaries,
    it finaly appends the COI sequence and a description line in a fasta file.
        -the extract function returns a list of the accession numbers for which a COI has been found and the name of the text file printed
            remaining accession numbers
        -the script finds the taxids for which no COI has been found by substracting the list of accession number retreived from the dictionnary outputed from the taxids function and the list of accession numbers returned by the extract2 function
        -the script calls the taxo function with the list of remaining accession number, the dictionnaries with the TaxIDs and taxonomy information and name of the file to append the results
        -the taxo function searches the nucleotide database using the efetch e-utility to retreive the genbank file, it sends batches of 10 (can be set to more changing the retmax variable value) accession numbers
    from the genbank file the taxo function looks for the COI for each accession numbers and retreive the informations: location, DNA sequences.
    it appends the resluts in a fasta-like format to the filen given as Input.
