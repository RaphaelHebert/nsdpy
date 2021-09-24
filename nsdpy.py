from functions import esearchquery, completetaxo, taxids, cdsfasta, extract, taxo, fasta, duplicates
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
    parser.add_argument("-S", "--summary", help='summarize the process in a table', action="store_true")
    #Taxonomy
    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument("-i", "--information", help="just add the taxonomic information in the information line of the output file(s)", action="store_true" )
    group3.add_argument("-k", "--kingdom", help="output three different file text (Plantae and Fungi, Metazoa, Others", action="store_true" )
    group3.add_argument("-p", "--phylum", help="output one file text per phylum", action="store_true" )
    group3.add_argument("-l", "--levels", help="find only the taxon given by user", nargs="+")
    group3.add_argument("-s", "--species",\
        help="classify the results in different text file one for each specie+n level found, exp: -s correspond to lowest levels, -ss 2nd lowest, -sssss 5th lowest and so on",\
        action="count", default=3)

    args = parser.parse_args()

    #################################################
    #############   GLOBAL VARIABLES    #############
    #################################################
    #verbose
    if args.verbose:
        verb = 2
    elif args.quiet:
        verb = 0
    else:
        verb = 1

    #taxonomy
    if args.kingdom:
        classif = 1
    elif args.phylum:
        classif = 0
    elif args.levels:
        classif = args.levels
    elif args.information:
        classif = 2
    elif args.species:
        classif = args.species
    else:
        classif = 3

    OPTIONS = (verb, args.cds, classif, args.taxids)
    QUERY = (args.request, args.apikey)

    ##foldername and path
    name = str(datetime.now())
    name = '_'.join(name.split())[:19]
    name = name.replace(":", "-")
    path = "./results/" + name


    ##############################################
    ###########RUN THE RUN!!######################
    ##############################################

    #create the directory to store the results
    if not os.path.exists(path):
        os.makedirs(path)

    ###esearchquery
    y = esearchquery(QUERY)
    ##check errors (if bad API key etc) errors returned by the Entrez API
    if "error" in y.keys():
        errors = y["error"]
        sys.exit(errors)

    count = int(y["esearchresult"]["count"])
    if count < 1: 
        sys.exit("No results found")
    webenv =  str(y["esearchresult"]["webenv"])
    querykey = str(y["esearchresult"]["querykey"])
    params = (querykey, webenv, count)

    #comments
    if verb > 0:    
        print(f'Number of results found: {count}')

    ###Taxids
    dictid = taxids(params, path, OPTIONS)
    listofids = list(dictid.keys())
    reverse = {value for value in dictid.values()}
    listofTaxids = list(reverse)

    ###completetaxo2
    if classif != 3:
        dicttaxo = completetaxo(listofTaxids, QUERY, OPTIONS)
    else:
        dicttaxo = {}

    ###CDS fasta file
    if args.cds is None:
        found = fasta(path, dictid, dicttaxo, QUERY, listofids, OPTIONS)
    else:
        found = cdsfasta(params, path, dictid, dicttaxo, QUERY, OPTIONS)

    ###list the remaining access id:
    remaining = set(listofids) - set(found)
    remaining = list(remaining)
    if verb > 0 and args.cds is not None:
        print(f'number of remaining accession numbers with no sequence found: {len(remaining)}')

    ###if filter 
    if args.cds is not None and remaining:
        analyse, sequences = taxo(path, remaining, dictid, QUERY, OPTIONS)
    else:
        analyse, sequences = [], []
    end = str(datetime.now())
    end = '_'.join(end.split())[:19]
    end = end.replace(":", "-")

    genes = found + sequences
    total = list(set(analyse) | set(found)) 
    notfound = list(set(listofids) - (set(sequences) | set(found)))

    ###comments
    if args.cds is not None:
        if verb > 0:
            print(f'number of results from NCBI:                                                                {count}')
            print(f'number of unique accession version identifiers:                                             {len(listofids)}')
            print(f'number of genes found in the cds_fasta file:                                                {len(found)}')
            print(f'number of genes found in the genbank file:                                                  {len(sequences)}')
            print(f'total number of sequences retrieved:                                                        {len(genes)}')
            print(f'number with more than one sequences:                                                        {duplicates(genes, path)}')
            print(f'total number of accession version identifiers analysed:                                     {len(total)}')
            print(f'ended:                                                                                      {end}')
        if notfound and verb > 0:
            print(f"total number of accession version identifiers \nfor which no gene has been retrieved:                                                  {len(notfound)}")
            print("see the notfound.txt for the detail")

    else:
        if verb > 0:
            print(f'number of results from NCBI:                                        {count}')
            print(f'number of unique accession version identifiers:                     {len(listofids)}')
            print(f'total number of sequences retrieved:                                {len(genes)}')
            print(f'number with more than one sequences:                                {duplicates(genes, path)}')
            print(f'total number of accession version identifiers analysed:             {len(total)}')
            print(f'ended:                                                              {end}')
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


    if args.summary:
        try:
            y = open("report.txt")
            y.close()
            with open("report.txt", 'a') as r:
                r.write(f"{args.request}    {name}  {end}   {filetype}  {count}     {filters}     {len(found)}     {len(listofTaxids)}\n")
        except:
            with open("report.txt", 'a') as r:
                r.write(f"request   start   end   results   type    esearch    filter   sequences    TaxIDs\n")
                r.write(f"{args.request}    {name}  {end}   {filetype}  {count}     {filters}     {len(found)}     {len(listofTaxids)}\n")

