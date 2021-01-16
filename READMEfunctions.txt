Script functions.py:
Define some functions that are used in taxonomy.py and feature.py


The intputs QUERY, OPTIONS and params correspond to tuples that contain:
QUERY:
	-query(STRING): phrase the user wants to use to search in the nucleotide database from NCBI in text format
			exp: '((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))' 
	-apikey(STRING, OPTIONNAL): api key for for the entrez api from NCBI text format
		 exp:'66af22581a26c4fdc8e74788e8562502a308'

OPTIONS:
	-args.FEATURE(BOOL):if the function should writes a text file with the feature table or not
	-args.TAXIDS(BOOL):if the function should writes a text file with the accession numbers and their TaxIDS table or not
	-verb(INT): verbose or quiet options
	-genelist(list): list of genes to be found
	-classif (INT, or LIST): if LIST correspont to a list of taxonomic levels names entered by the user, if INT [0, infinite[
	
-params: 
	-querykey(STRING) the query_key returned by a search with the esearch E-utility in history mode, text format. exp: "1".
	-webenv(STRING), the webenv returned by a search with the esearch E-utility in history mode, text format. exp: "MCID_5fdaff9d0aee646a05268177"
	-count(INTEGER), the number of of matches returned by a search in esearch E-utility and converted to an integer. exp: 86184

Function dowload(parameters, address):

	INPUTS:
		-parameters(DICT) a dictionnary with the name of the parameters as keys and their value as values
	ACTION:
		-make a call using the get method from the request library to the address provided with the parameters as parameters
		-loop untils getting an answer from the call
		-handle errors (sush as HTTPerror, network error...)
		

Function esearchquery(QUERY):

	INPUTS: 
		-QUERY (TUPLE): tuple containing the query and apikey variable. esearch query uses the query and apikey from QUERY
		
	ACTION:
	Submit the user's request to the ncbi esearch engine (https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch) with the following parameters:
		-usehistory = y	(using history mode allow to get the querykey and webenv number to use in other E-utilities) 
    		-db=nucleotide (look in the nulceotide database)
    		-idtype=acc	(return accession numbers)
		    		-retmax=0	(number of idtype that will be displayed)
    		-retmode=json	(data returned in Json format)
	
	OUTPUTS:
		-Returns the result of the user's request result as a dictionnary


Function taxids(params, path, OPTIONS):

	INPUTS:
		-params(TUPLE): taxids uses querykey, webenv and count from params.
		-path(STRING), path of the folder to store the results (text and fasta files)
		-OPTIONS(TUPLE): taxids uses verb and args.TAXID from OPTIONS.
			
	ACTION:
		Searches the taxonomy database with the esummary E-utility. It sends queries by batches of 100 (or more: see retmax variable). It then finds the accession number and their corresponding TaxIDs
	if args.TAXID is True (option -T selected)
		It writes the text file with one accession number and its corresponding TaxID per line.
	
	OUTPUTS:
		-(optionnal -T) A text file with one accession number and its corresponding TaxID per line separated by a tab. exp:MW080658   436086.
		-A dictionnary with the accession numbers as keys and TaxIDs as values.
	

Function feattable(params, path, dictid, dicttaxo, QUERY, OPTION):

	INPUTS:
		params(TUPLE): uses querykey, webenv, count from params
		path(STRING): the path of the location where the results are written
		dictid(DICT): output of taxids() function, dictionnary with accession number as keys and taxids as values
		QUERY(TUPLE): uses apikey from QUERY
		OPTION(optionnal):uses verb, genelist and args.FEATURE from OPTION
	
	ACTION:
		Using the efetch E-utility with the parameter from params it looks in the nuccore (=nucleotide) database to retrieve the feature table for 100 accession numbers (see retmax variable) at the time.
		If the arge.FEATURE is True, writes the results in a txt file.
Call the extract function to analyse the results from Entrez API (everytime Entrez returns some results).
		
	OUTPUTS:
		It returns the list of the accession number for which a COI and its taxonomy have been found.

		
Function taxo(path, listofid, dictid, dicttaxo, QUERY, OPTION)
	
	INPUTS:
		-path(STRING) see above
		-listofid (LIST) list of the accession numbers for which no COI have been found 
		-dictid (DICTIONNARY) see above
		-dicttaxo (DICTIONNARY) dictionnary with the TaxIDs as keys and the taxonomic information as values
		-QUERY(TUPLE): uses the apikey from QUERY
		-OPTIONS(TUPLE): uses verb, genelist and classif from OPTIONS
	
	ACTION:
		-query Entrez API with the efetch tool to search the nucleotide database from NCBI and retreive a genbank file. Send 10 (retmax variable) accession numbers at the time, send some queries until no more accession number are left from the listofid. Use the requests librairy to send get requests to Entrez API.
		-split the received text (gb format) every '//' to get a list.
		-Iterate over the list, and for each accession number look for the strings from genelist
		-tries to find gene corressponding to genelist and extract name and location
		-if no match is found, the accession number is appended to the notefound.txt file and the next accession number is analysed
		 -tries to find CDS corressponding to the above list and extract name and location
		 -compares the starting and ending positions of the gene location and CDS location, if they corrrespond extract the gene from the DNA sequence based on the location(s) of the exons found in CDS, if not based on the gene location(s).
Takes the location annotation from gene or CDS depending on which one was used to retreive the sequence.
		-get the lineage division and Name from the inputted ditcionnaries.
		-if lineage name or division are not found in the dictionnaries extract them from the genbank format results .
		-calls the dispatch function with the classif parameters
		-append the gene and its taxonomy to a textfile corresponding to path and the results from the dispatch funtion
		
	OUTPUT:
		-returns a list of the accession numbers for which a COI has been found (LIST)
		-appends the accession numbers for which no COI has been found in the notefound.txt file
		-appends the results (information line + dna sequence) in a fasta file for the accession for which a gene has been found.
		
		
Function extract(path, text, dictid, dicttaxo, genelist, verb):
	
	INPUTS:
		-path(STRING): see above
		-text(STRING): featuretable in text format, results of the call to nuccore database made by feattable function.
		-dictid (DICTIONNARY) see above
		-dicttaxo (DICTIONNARY) see above
		-genelist(LIST) from OPTIONS, see above 
		-verb(INT) from OPTIONS, see above
	
	ACTION:
		-Iterates over each gene of the text variable
		-for each gene sequence (+ information line) calls the subextract function.
	
	OUTPUTS:
		-a list of the accession numbers for which a gene (from genelist) have been found (LIST)
		
		
Function subextract(seq, path, dictid, dicttaxo, genelist):
this function is called by the extract2 function.

	INPUTS:
		-seq(STRING): the gene sequence with its information line
		-path(STRING) see above
		-dictid (DICTIONNARY) see above
		-dicttaxo (DICTIONNARY) see above
		-genelist(LIST) see above
	
	ACTION:
		-extracts the accession number 
		-retrieves TaxID from dictid
		-retrieves taxonomic informations from dicttaxo, if no information are found in dictaxo (keyerror) it returns (so the accession number will be searched later with the taxo function and these infos will be retrieved from the genbank result)
		-check if the gene is in genelist
		-if the gene matches, the location information is extracted from the information line.
		-else it returns
		-the results is appended to the fasta file given as input base on the dispatch values from dicttaxo parameter
		-returns the accession number(STRING)



