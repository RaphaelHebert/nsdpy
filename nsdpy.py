from functions import esearchquery, completetaxo, taxids, cds_fasta, taxo, fasta, duplicates
import sys
import os
import argparse             #parsing command line arguments
from datetime import datetime    

def main():
############################################
###### CHECK COMMAND LINE ARGUMENTS ########
############################################

    parser = argparse.ArgumentParser()

    ##POSITIONAL ARGUMENTS
    parser.add_argument("-r", "--request", required=True, help="The request to the NCBI database")

    ##OPTIONAL ARGUMENTS
    #api key
    parser.add_argument("-a", "--apikey", default=None, help="API key (register to NCBI to get an API key)")
    #verbose
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="Diplays downloads progress and actions", action="store_true")
    group.add_argument("-q", "--quiet", help="No verbose output", action="store_true")
    #gene selection
    parser.add_argument("-c", "--cds", help="search for a given list of gene, exp: COX1 COX2 COX3, accepts regex", nargs="*")
    #file input
    parser.add_argument("-L", "--list", help='input one or more .txt file as an external list of taxa: path/to/file.txt', nargs="*")
    #file output
    parser.add_argument("-T", "--taxids", help='write a text file listing all the accession numbers and their related TaxIDs', action="store_true")
    parser.add_argument("-t", "--tsv", default=None, help="create a tsv file based on fasta file output", action="store_true")
    #Taxonomy
    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument("-k", "--kingdom", help="output four different text files file: Plantae and Fungi, Metazoa and  Others", action="store_true" )
    group3.add_argument("-p", "--phylum", help="output one file text per phylum", action="store_true" )
    group3.add_argument("-l", "--levels", help="find only the taxon given by user", nargs="+")
    group3.add_argument("-s", "--species",\
        help="classify the results in different text file one for each specie+n level found, exp: -s correspond to lowest levels, -ss 2nd lowest, -sssss 5th lowest and so on",\
        action="count", default=3)

    #information line
    parser.add_argument("-i", "--information", help="just add the taxonomic information in the information line of the output file(s)", action="store_true" )

    args = parser.parse_args()

    #################################################
    #############   GLOBAL VARIABLES    #############
    #################################################

    # list the selected option to make it appear in report.txt
    options_report = []

    #taxa list
    if args.list:
        input_files = ' '.join(args.list)
        options_report.append(f" -list (-L) {input_files}")
        # Check that a file is provided
        if len(args.list) == 0:
            sys.exit("The --list (-L) requires at list one .txt file")

        # Check if files exists
        for file in args.list:
            if not os.path.exists(file):
                sys.exit(f"The file {file} cannot be found")
            if file[-4:] != ".txt":
                sys.exit(f"The list of taxa {file} must be a .txt file")

    #list of chosen options to display in the report.tsv
    ##parse options
    if args.tsv:
        options_report.append("--tsv (-t)")
    if args.information:
        options_report.append("--information (-i)")
    if args.taxids:
        options_report.append("--taxids (-T)")
    if args.cds is not None:
        options_report.append(f"--cds (-c) {' '.join(args.cds)}")
    if args.apikey:
        options_report.append(f"--apikey (-a) {args.apikey[0]}")

    #verbose
    if args.verbose:
        verb = 2
        options_report.append("--verbose (-v)")
    elif args.quiet:
        verb = 0
        options_report.append("--quiet (-q)")
    else:
        verb = 1

    #taxonomy
    if args.kingdom:
        classif = 1
        options_report.append("--kingdom (-k)")
    elif args.phylum:
        classif = 0
        options_report.append("--phylum (-p)")
    elif args.levels:
        classif = args.levels
        options_report.append(f"--levels (-l) {args.levels[0]}")
    elif args.species:
        classif = args.species
        if args.species != 3:
            options_report.append("--species (-", + "s" * ( args.species - 3 ) + ")")
    else:
        classif = 3

    OPTIONS = (verb, args.cds, classif, args.taxids, args.tsv, args.information)

    ##foldername and path
    starting_time = str(datetime.now())
    starting_time = '_'.join(starting_time.split())[:19]
    starting_time = starting_time.replace(":", "-")
    path = "./NSDPY results/" + starting_time


    ##############################################
    #########  RUN THE RUN!!  ####################
    ##############################################
    
    # Create the directory to store the results
    if not os.path.exists(path):
        os.makedirs(path)

    # Read the taxa list files 
    if args.list:
        taxa_list = []
        for file in args.list:
            with open(file, "r") as data:
                taxa_list = taxa_list + data.read().splitlines()
        
        # Add the taxa to the query
        taxa_list = [ taxon + "[ORGN] OR " for taxon in taxa_list]

        # Base URL with params
        esearch_address = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        base_URL_length = len(esearch_address) + 100 # Keep 100 chars for params

        # Base query
        base_query = args.request + " AND ("
        
        # Remaining space for the taxa list 
        taxa_max_length = 2048 - ( len(base_query) + base_URL_length )
        ##see these threads;
        #https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers?noredirect=1&lq=1
        #https://stackoverflow.com/questions/812925/what-is-the-maximum-possible-length-of-a-query-string

        # Include taxa in the QUERY and make a list of queries <= 2048 chars
        remaining_space = taxa_max_length
        queries_list = []
        new_query = base_query

        #TODO: a bit of cleanup in this for loop...
        for taxon in taxa_list:
            if (remaining_space - len(taxon) + 4) <= 0:
                # Delete the last "[ORGN] OR " and close parenthesis
                queries_list.append(new_query[:-8] + ')')
                # Start another query
                new_query = base_query
                remaining_space = taxa_max_length
            else:
                remaining_space = remaining_space - len(taxon)
                new_query = new_query + taxon
                if queries_list:
                    queries_list[-1] = new_query
                else:
                    queries_list.append(new_query)
        queries_list[-1] = queries_list[-1][:-4] + ')'
    else:
        queries_list = [args.request]    

    ### Retrieving results from esearch and the related TaxIDs
    dict_ids = {}

    total_number_of_results = 0
    for query in queries_list:
        query = query.rstrip('0').rstrip(' OR ') + ')'
        QUERY = (query, args.apikey)
        if verb != 0:
            print(f"retrieving results for {query} ....")        

        ## esearchquery
        y = esearchquery(QUERY)

        ##check errors (if bad API key etc) errors returned by the Entrez API
        if "error" in y.keys():
            errors = y["error"]
            sys.exit(errors)

        count = int(y["esearchresult"]["count"])
        #comments
        if verb > 0:    
            print(f'Number of results found: {count}')

        if count < 1:
            continue
        webenv =  str(y["esearchresult"]["webenv"])
        querykey = str(y["esearchresult"]["querykey"])
        params = (querykey, webenv, count)

        ###Taxids
        if verb != 0:
            print("retreiving the corresponding TaxIDs...")
   
        subdictids = taxids(params, path, OPTIONS)
        dict_ids = {**dict_ids, **subdictids}

        total_number_of_results = len(set(dict_ids.keys()))

    if total_number_of_results < 1: 
        sys.exit("No results found")

    if verb != 0:
        print(f"Total number of results: {total_number_of_results}")

    #make a set of TaxIDs
    list_of_ids = list(dict_ids.keys())
    reverse = set(dict_ids.values())
    list_of_TaxIDs = list(reverse)


    ### completetaxo (call EFETCH to query the taxonomy database)
    # Check that an option that requires the taxonomic information has been selected
    dict_taxo = {}
    if classif != 3 or args.information:
        dict_taxo = completetaxo(list_of_TaxIDs, QUERY, OPTIONS)


    ### Download the sequences (call to EFETCH to query the nuccore database)
    if args.cds is None:
        found = fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS)
    else:
        found = cds_fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS)

    ### List the remaining access ids:
    remaining = set(list_of_ids) - set(found)
    remaining = list(remaining)

    # Comments
    if verb > 0 and args.cds is not None:
        print(f'number of remaining accession numbers with sequence to be found in GenBank files: {len(remaining)}')


    ### taxo (call EFETCH to query the nuccore database to get the .gb files) 
    analyse, sequences = taxo(path, remaining, dict_ids, QUERY, dict_taxo, OPTIONS)


    ### summarise
    # Get the ending time of the run
    ending_time= str(datetime.now())
    ending_time= '_'.join(ending_time.split())[:19]
    ending_time= ending_time.replace(":", "-")        

    ### Comments
    genes = found + sequences
    total = list(set(analyse) | set(found)) 
    notfound = list(set(list_of_ids) - (set(sequences) | set(found)))
    if args.cds is not None:
        if verb > 0:
            print(f'number of unique results from NCBI:                                                          {count}')
            print(f'number of genes found in the cds_fasta file:                                                {len(found)}')
            print(f'number of genes found in the genbank file:                                                  {len(sequences)}')
            print(f'total number of sequences retrieved:                                                        {len(genes)}')
            print(f'number with more than one sequences:                                                        {duplicates(genes, path)}')
            print(f'total number of accession version identifiers analysed:                                     {len(total)}')
            print(f'ended:                                                                                      {ending_time}')
        if notfound and verb > 0:
            print(f"total number of accession version identifiers \nfor which no gene has been retrieved:                                                  {len(notfound)}")
            print("see the notfound.txt for the detail")

    else:
        if verb > 0:
            print(f'number of unique results from NCBI:                                  {total_number_of_results}')
            print(f'total number of sequences retrieved:                                {len(genes)}')
            print(f'number with more than one sequences:                                {duplicates(genes, path)}')
            print(f'total number of accession version identifiers analysed:             {len(total)}')
            print(f'ended:                                                              {ending_time}')
            print(f'number of accession version identifiers analysed with no sequences downloaded:             {len(notfound)}')
            if len(notfound) > 0:
                print(f'see "notfound.txt"')

    ##write summary
    if args.cds is None:
        filters = ""
        filetype = "fasta"
    else:
        filters = ",".join(args.cds)
        filetype = "cds_fasta"

    options_report = ",".join(options_report)

    try:
        y = open("report.tsv")
        y.close()
        with open("report.tsv", 'a') as r:
            r.write(f"{args.request}\t{options_report}\t{starting_time}\t{ending_time}\t{filetype}\t{count}\t{filters}\t{len(found)}\t{len(list_of_TaxIDs)}\n")
    except:
        with open("report.tsv", 'a') as r:
            r.write(f"request\toptions\tstarting_time\tending_time\tresults type\tesearch\tGene filters\tsequences\tTaxIDs\n")
            r.write(f"{args.request}\t{options_report}\t{starting_time}\t{ending_time}\t{filetype}\t{count}\t{filters}\t{len(found)}\t{len(list_of_TaxIDs)}\n")
            