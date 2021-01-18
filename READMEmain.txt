script: main.py

    INPUTS: 
    	POSITIONNAL ARGUMENTS
        -r --request	the user's query as first command line argument (the query as the user would enter it in the NCBI search engine)
        
       OPTIONNAL ARGUMENTS
        -a --apikey	the user's NCBI API key
        -h --help	will display the help
        -v --verbose / -q --quiet	will display more (v) or less (q) comments in the terminal
        -g --genes / -f --fasta (exclusive)	choose the gene(s) to be search in CDS fasta files and genbank files, if -f just download and write a text file with the sequences found in the fasta files and their taxonomy information (linaeage and name)
        if no option selected the sequences of the CDS fasta files and genbank files won't be filtered.
        -T --TAXIDS writes a text file with all the accession numbers and their corresponding taxids found by the esearch query
        -C --CDS writes a text file with the retrieved CDS fasta files from the nuccore database.
        -k --kingdom / -p -phylum / -l --levels / -s --species
select how the results must be classified, if no option selected all the results will be appended in one text file.
if -k 3 text files (METAZOA, PLANTAE/FUNGI, OTHERS)
if -p one text file per phylum
if -l takes the taxonomics levels entered by the user, exp:
-l Deuterostomia, Protostomia 
if -ns takes the lowest level in the sequence taxonomy plus n, exp: -sss will select the thrird lowest level in each sequence taxonomy. (it will write as many text files as different levels are found)
       
       
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
the dispatch key depends on the option selected for the classification (-kpls)
            cdsfasta
        -calls the function cdsfasta if the fasta option is not selected
        	-the function uses efetch E-utility to search the nuccore (=nucleotide) database and retreive the results as a CDS fasta file in text format, then call the extract function with this result.
	-calls the fasta function if the fasta fonction is selected
		-the function uses efetch E-utility to search the nuccore (=nucleotide) database and retreive the results as a fasta file in text format (if fasta option is selected it download the fasta files), then append the results to the fasta file(s)
    The function outputs a list of the accession number for which the targeted gene(s) has been found.
    
        Taxo
        (not called if the fasta option is selected)
        -the script calls the taxo function with the list of remaining accession number, the dictionnaries with the TaxIDs and taxonomy information and name of the file to append the results
        -the taxo function searches the nucleotide database using the efetch e-utility to retreive the genbank file, it sends batches of 10 (can be set to more changing the retmax variable value) accession numbers
    from the genbank file the taxo function looks for the COI for each accession numbers and retreive the informations: location, DNA sequences.
    it appends the resluts in a fasta-like format to the filen given as Input.
