Script functions.py:
Define some functions that are used in taxonomy.py and feature.py


Function esearchquery(query, apikey):
	
	INPUTS: 
		-query(STRING): phrase the user wants to use to search in the nucleotide database from NCBI in text format
			exp: '((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))' 
		-apikey(STRING, OPTIONNAL): api key for for the entrez api from NCBI text format
		 exp:'66af22581a26c4fdc8e74788e8562502a308'
	
	ACTION:
	Submit the user's request to the ncbi esearch engine (https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch) with the following parameters:
		-usehistory = y	(using history mode allow to get the querykey and webenv number to use in other E-utilities) 
    		-db=nucleotide (look in the nulceotide database)
    		-idtype=acc	(return accession numbers)
		    		-retmax=0	(number of idtype that will be displayed)
    		-retmode=json	(data returned in Json format)
	
	OUTPUTS:
		-Returns the result of the user's request as a dictionnary


Function taxids(querykey, webenv, count):

	INPUTS:
		-querykey(STRING) the query_key returned by a search with the esearch E-utility in history mode, text format. exp: "1".
		-webenv(STRING), the webenv returned by a search with the esearch E-utility in history mode, text format. exp: "MCID_5fdaff9d0aee646a05268177"
		-count(INTEGER), the number of of matches returned by a search in esearch E-utility and converted to an integer. exp: 86184
	
	ACTION:
		Searches the taxonomy database with the esummary E-utility. It sends queries by batches of 100 (or more see retmax variable) accession numbers at once and write the result in a text file.
	It rewrites the text file to leave only one accession number and its corresponding TaxID per line.
	
	OUTPUTS:
		-A text file with one accession number and its corresponding TaxID per line separated by a tab. exp:MW080658   436086.
		-A dictionnary with the accession numbers as keys and TaxIDs as values.
	

Function feattable(querykey, webenv, count, apikey):

	INPUTS:
		apikey is OPTIONNAL
		querykey, webenv and count are retrieved from the esearchquery function
	
	ACTION:
		Using the efetch E-utility it looks in the nuccore (=nucleotide) database to retrieve the feature table for 100 accession numbers (see retmax variable) at the time. It writes the results in a txt file.
		
	OUTPUTS:
		It returns the filename (STRING) of text file containing the results.

		
Function taxo(filename, listofid, dictid, dicttaxo)
	
	INPUTS:
		-filename (STRING) the filename of the fasta file to append the results
		-listofid (LIST) list of the accession number to recover the COI and other information from
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-query Entrez API with the efetch tool to search the nucleotide database from NCBI and retreive a genbank file. Send 10 (retmax variable) accession numbers at the time, send some queries until no more accession number are left from the listofid. Use the requests librairy to send get requests to Entrez API.
		-split the received text (gb format) every '//' to get a list.
		-Iterate over the list, and for each accession number look for a COI (match an elelment from this list:     coilist = ['gene="COX1"', 'gene="Cox1"', 'gene="cox1"', 'gene="co1"', 'gene="CO1"', 'gene="Co1"', 'gene="COXI"', 'gene="CoxI"', 'gene="coxI"', 'gene="coi"', 'gene="COI"']) 
		-tries to find gene corressponding to the above list and extract name and location
		-if no COI is found, the accession number is appended to the notefound.txt file and the next accession number is analysed
		 -tries to find CDS corressponding to the above list and extract name and location
		 -compares the starting and ending positions of the gene location and CDS location, if they corrrespond extract the COI from the DNA sequence based on the location(s) of the exons found in CDS, if not based on the gene location(s).
Takes the location annotation from gene or CDS depending on which one was used to retreive the sequence.
		-get the lineage division and Name from the inputted ditcionnaries.
		-if lineage name or division are not found in the dictionnaries extract them from the genbank format results .
		-appends the result to the file given as input.	
		
	OUTPUT:
		-returns a list of the accession numbers for which a COI has been found (LIST)
		-appends the accession numbers for which no COI has been found in the notefound.txt file
		-appends the results (information line + dna sequence) in a fasta file for the accession for which a COI has been found.
		
		
Function extract(inputfilename, dictid, dicttaxo):
	
	INPUTS:
		-inputfilename (TEXT FILE): the name of the file of the feature table returned by the feattable function
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-Iterates over each gene of the feature table text file
		-for each gene sequence (+information line) calls the subextract function.
	
	OUTPUTS:
		-the name of the fasta file with the COIs (STRING)
		-returns a list of the accession number for which a COI has been found (LIST)
		
		
Function subextract(seq, filename, dictid, dicttaxo):
this function is called by the extract2 function.

	INPUTS:
		-seq(STRING): the gene sequence with its information line
		-the name of the fasta file to append the COIs to(STRING)
		-dictid (DICTIONNARY) dictionnary with the accession number as keys and TaxIDs as values
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
	
	ACTION:
		-extracts the accession number 
		-retreives TaxID from dictid
		-retreives taxonomic informations from dicttaxo, if no information are found in dictaxo (keyerror) it returns (so the accession number will be search later with the taxo function and these infos will be retrieved from the genbank result)
		-check if the gene is a COI looking for the following expression: ("=COX1]", "=COI]", "=CO1]", "=cox1]", "=coi]", "=co1]", "=Cox1]")
		-if the gene corresponds to the COI the location information is extracted from the information line.
		-else it returns
		-the results is appended to the fasta file given as input.
		-returns the accession number (STRING)


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
		




