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

    #list of chosen options to display in the report.txt
    options_report = []

    ##parse options
    if args.tsv:
        options_report.append("--tsv (-t)")
    if args.information:
        options_report.append("--information (-i)")
    if args.taxids:
        options_report.append("--taxids (-T)")
    if args.cds:
        options_report.append(f"--cds (-c) {args.cds[0]}")
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
    QUERY = (args.request, args.apikey)

    ##foldername and path
    starting_time = str(datetime.now())
    starting_time = '_'.join(starting_time.split())[:19]
    starting_time = starting_time.replace(":", "-")
    path = "./NSDPY results/" + starting_time


    ##############################################
    #########  RUN THE RUN!!  ####################
    ##############################################

    # Create the main directory to store the results
    if not os.path.exists(path):
        os.makedirs(path)

    ### esearchquery (call to ESEARCH)
    search_result = esearchquery(QUERY)

    ## Check if the NCBI API returned any error (in case of bad API key, URL, etc..)
    if "error" in search_result.keys():
        errors = search_result["error"]
        sys.exit(errors)

    ## Check that some results have been found by the esearch with the provided query
    count = int(search_result["esearchresult"]["count"])
    if count < 1: 
        sys.exit("No results found")

    ## Get the references of the results to access them in the server history 
    webenv =  str(search_result["esearchresult"]["webenv"])             # refers to WebEnv parameter needed in the URL to call efetch 
    querykey = str(search_result["esearchresult"]["querykey"])          # refers to the query_key parameter needed in the URL to call esummary
    params = (querykey, webenv, count)

    # Comments
    if verb > 0:    
        print(f'Number of results found: {count}')


    ### Taxids (call ESUMMARY to query the taxonomy database)
    dict_ids = taxids(params, path, OPTIONS)

    # accession version numbers found 
    list_of_ids = list(dict_ids.keys())
    # TaxIDs found
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
        found = cds_fasta(params, path, dict_ids, dict_taxo, QUERY, OPTIONS)

    ### List the remaining access ids:
    remaining = set(list_of_ids) - set(found)
    remaining = list(remaining)

    # Comments
    if verb > 0 and args.cds is not None:
        print(f'number of remaining accession numbers with sequence to be found in GenBank files: {len(remaining)}')


    ### taxo (call EFETCH to query the nuccore database to get the .gb files) 
    if args.cds is not None and remaining:
        analyse, sequences = taxo(path, remaining, dict_ids, QUERY, dict_taxo, OPTIONS)


    ### summarise
    # Get the ending time of the run
    ending_time= str(datetime.now())
    ending_time= '_'.join(ending_time.split())[:19]
    ending_time= ending_time.replace(":", "-")        

    ### Comments
    if args.cds is not None:
        genes = found + sequences
        total = list(set(analyse) | set(found)) 
        notfound = list(set(list_of_ids) - (set(sequences) | set(found)))
        if verb > 0:
            print(f'number of results from NCBI:                                                                {count}')
            print(f'number of unique accession version identifiers:                                             {len(list_of_ids)}')
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
            print(f'number of results from NCBI:                                        {count}')
            print(f'number of unique accession version identifiers:                     {len(list_of_ids)}')
            print(f'total number of sequences retrieved:                                {len(found)}')
            print(f'number with more than one sequences:                                {duplicates(found, path)}')
            print(f'ended:                                                              {ending_time}')

    ##write summary
    if args.cds is None:
        filters = ""
        filetype = "fasta"
    else:
        filters = ",".join(args.cds)
        filetype = "cds_fasta"

    options_report = ",".join(options_report)

    try:
        y = open("report.txt")
        y.close()
        with open("report.txt", 'a') as r:
            r.write(f"{args.request}    {options_report}  {starting_time}  {ending_time}   {filetype}  {count}     {filters}     {len(found)}     {len(list_of_TaxIDs)}\n")
    except:
        with open("report.txt", 'a') as r:
            r.write(f"request   options   starting_time   ending_time  results   type    esearch    filter   sequences    TaxIDs\n")
            r.write(f"{args.request}    {options_report}    {starting_time}  {ending_time}   {filetype}  {count}     {filters}     {len(found)}     {len(list_of_TaxIDs)}\n")



## to remove before pushing to production
if __name__ == "__main__":
    main()