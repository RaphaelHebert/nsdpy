Script functions.py:
Define some functions that are used in taxonomy.py and feature.py


Function esearchquery(query, apikey):
	
	INPUTS: 
		-query(STRING): phrase the user want to use to search in the nucleotide database from NCBI in text format
			exp: '((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))' 
		-apikey(STRING): api key for for the entrez api from NCBI text format
		 exp:'66af22581a26c4fdc8e74788e8562502a308'
	
	ACTION:
	Submit the user's request to the ncbi esearch engine (https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch) with the following parameters:
		-usehistory = y	(using history mode allow to get the querykey and webenv number to use in other E-utilities) 
    		-db=nucleotide (look in the nulceotide database)
    		-idtype=acc	(return accession numbers)
		    		-retmax=0	(number of idtype that will be displayed)
    		-retmode=json	(data returned in Json format)
	
	OUTPUTS:
		-Return the result of the user's request as a 'requests.models.Response' (see the requests library)

	COMMENTS: Use the text method to see the result as text, exp: responseobject.text . The text can then be load as JSON format with the json librairie to extract the webenv and querykey parameter for further analyse with the E-Utilities from the Entrez API.


Function taxids(querykey, webenv, count):

	INPUTS:
		-querykey(STRING) the query key returned by a search with the esearch E-utilitie in history mode, text format. exp: "1".
		-webenv(STRING), the webenv returned by a search with the esearch E-utilitie in history mode, text format. exp: "MCID_5fdaff9d0aee646a05268177"
		-count(INTEGER), the count result returned by a search in esearch E-utilitie and converted to an integer. exp: 86184
	
	ACTION:
		Query the taxonomy database with the esummary E-utilisties from the NCBI Entrez API. It sends queries for batch of 100 (or more see retmax variable) idtype at once and write the result in a .txt file.
	It rewrites the text file to leave only one accession number and its corresponding TaxID per line.
	
	OUTPUTS:
		-A text file with one accession number and its corresponding TaxID per line. exp:MW080658   436086.
		-A dictionnary with the accession numbers as keys and TaxIDs as values.
	

Function feattable(querykey, webenv, count, apikey):

	INPUTS:
		Take the same arguments as taxids and the API key as in esearch query.
	
	ACTION:
		Using the efetch E-utilitie it looks in the nuccore (=nucleotide) database to retrieve the feature table for 100 (see retmax variable) at the time. It writes the results in a txt file.
		
	OUTPUTS:
		It return the filename (STRING) of text file written.

		
Function taxo2(filename, listofid, dictid, dicttaxo)
	
	INPUTS:
		-filename (STRING) the filename of the fasta file to append the results
		-listofid (LIST) list of the accession number to recover the COI and other information from
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-query Entrez API with the efetch tool to search the nucleotide database from NCBI and retreive a genbank file. Send 200 (retmax variable) accession numbers at the time, send some query until no more accession number are left from the listofid. Use the requests librairy to send a get request to the API.
		-split the received text (gb format) every '//' to get a list.
		-Iterate over the list, and for each accession number look for a COI (match an elelment from this list:     coilist = ['gene="COX1"', 'gene="Cox1"', 'gene="cox1"', 'gene="co1"', 'gene="CO1"', 'gene="Co1"', 'gene="COXI"', 'gene="CoxI"', 'gene="coxI"', 'gene="coi"', 'gene="COI"']) 
		-try to find gene corressponding to the above list and extract name and location
		-if no COI is found, the accession number is appended to the notefound.txt file and the next accession number is analysed
		 -try to find CDS corressponding to the above list and extract name and location
		 -compare the starting and ending positions of the gene location and CDS location, if they corrrespond extract the COI from the dna sequence based on the locations of the exons found in CDS, if not based on the gene location.
Take the location annotation from gene or CDS depending on which one was used to retreive the sequence.
		-get the lineage division and Name from the inputted ditcionnaries.
		-if lineage name or division are found in the dictionnaries extract them from the gb text.
		-append the result to the file given as input.
		-if no COI has been found the COI sequence is noted as 'location error'.
		
	OUTPUT:
		-return a list of the accession number for which a COI has been found (LIST)
		-append the accession numbers for which no COI has been found in the notefound.txt file
		-append the result (information line + dna sequence) in a fasta file for the accession for which a COi has been found.
		
		
Function extract2(inputfilename, dictid, dicttaxo):
	
	INPUTS:
		-inputfilename (TEXT FILE): the name of the file of the feature table returned by the feattable function
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-Iterate over each gene of the feature table text file
		-for each gene sequence (+information line) call the subextract2 function.
	
	OUTPUTS:
		-the name of the fasta file with the COIs (STRING)
		-return a list of the accession number for which a COI has been found (LIST)
		
		
Function subextract2(seq, filename, dictid, dicttaxo):
this function is called by the extract2 function.

	INPUTS:
		-seq(STRING): the gene sequence with its information line
		-the name of the fasta file to append the COIs to(STRING)
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-extract the accession number 
		-retreive TaxID from dictid
		-retreive taxonomic informations from dicttaxo, if no information are found in dictaxo (keyerror) return (so the accession number will be search later with the taxo2 function and retreive these info from the gb file)
		-check if the gene is a coi looking for the following regexp: ("=COX1]", "=COI]", "=CO1]", "=cox1]", "=coi]", "=co1]", "=Cox1]")
		-if the gene correspond to the COI the location information is extracted from the information line.
		-else it returns
		-the results is appended to the fasta file given as input.
		-return the accession number (STRING)


Function table(inputfile, outputfile):

	INPUTS:
		-inputfile(STRING): name of the file to analyse (fasta format)
		-outputfile(STRING): name of the file to append the results (if the file doesn't exists the script will create it)
	
	ACTION:
		-read the content of the input file
		-split the content to make a list of sequences (information line + DNA sequence)
		-extract the information (i.e accession number, TaxID, Phylum, number of introns, length of the COI
		-add the accession number to a list to check the number of gene found for each accession number
		-open or create the output file to append the result as a line containing the extracted informations separated by coma (CSV style)
		
	OUTPUTS:
		-append the results to the output file
		-if the ouput file doesn't exist it creates it
		

Function duplicates(inputfilename):
	INPUTS:
		-inputfilename (STRING): name of the file to analyse

	ACTION:
		-look for the accession number with more than one sequence
		-write the sequences of these accession number in a text file
		-rewrite the input file wihtout the duplicates.
	
	OUTPUTS
		-prints the number of accession number with more than one sequence and the number of sequences in the duplicate text file
		




