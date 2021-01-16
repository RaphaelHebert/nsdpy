from functions import esearchquery, completetaxo, taxids, feattable, extract, taxo
import sys
import os
import argparse             #parsing command line arguments
from datetime import datetime    


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
group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-g", "--genes", help="search for a given list of gene, exp: COX1 COX2 COX3, accepts regex", nargs="+")
group2.add_argument("-f", "--fasta", help="retrieve the fasta files, adapted to non-coding sequences", action="store_true")
#file output
parser.add_argument("-T", "--TAXIDS", help='write a text file listing all the accession numbers and their related TaxIDs', action="store_true")
parser.add_argument("-F", "--FEATURE", help='write a text file listing the feature tables', action="store_true")
#Taxonomy
group3 = parser.add_mutually_exclusive_group()
group3.add_argument("-k", "--kingdom", help="output three different file text (Plantae and Fungi, Metazoa, Others", action="store_true" )
group3.add_argument("-p", "--phylum", help="output one file text per phylum", action="store_true" )
group3.add_argument("-l", "--levels", help="find only the taxon given by user", nargs="+")
group3.add_argument("-s", "--species",\
    help="classify the results in different text file one for each specie+n level found, exp: -s correspond to lowest levels, -ss 2nd lowest, -sssss 5th lowest and so on",\
    action="count", default=2)

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

#gene selection
if args.genes:
    genelist = args.genes
elif args.fasta:
    genelist = None
else:
    genelist = []

#taxonomy
if args.kingdom:
    classif = 1
elif args.phylum:
    classif = 0
elif args.levels:
    classif = args.levels
elif args.species:
    classif = args.species
else:
    classif = 2

OPTIONS = (verb, genelist, classif, args.TAXIDS, args.FEATURE)
QUERY = (args.request, args.apikey)
##foldername and path
name = str(datetime.now())
name = '_'.join(name.split())
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

##select TaxIDs
reverse = {value for value in dictid.values()}
listofTaxids = list(reverse)

###completetaxo2
dicttaxo = completetaxo(listofTaxids, QUERY, OPTIONS)

###feattable
found = feattable(params, path, dictid, dicttaxo, QUERY, OPTIONS)
    
###list the remaining access id:
remaining = set(listofids) - set(found)
remaining = list(remaining)
if verb > 0 and genelist is not None:
    print(f'number of remaining accession numbers with no sequence found: {len(remaining)}')

###if no fasta option
if genelist is not None:
    analyse, notfound = taxo(path, remaining, dictid, dicttaxo, QUERY, OPTIONS)

    ##check the accession numbers for which no COI have been found
    idk = list(set(listofids) - (set(analyse) | set(found)))

    #comments:
    if verb > 0:
        print(f'number of unique accession numbers:           {len(listofids)}')
        print(f'number of genes found in the feature table:   {len(found)}')
        print(f'number of genes found in gb file:             {len(analyse)}')
        print(f'total number of sequences retrieved:          {len(found) + len(analyse)}')
        print(f'total number of accession number analysed:    {len(set(analyse)) + len(set(found)) + notfound}')
    if len(idk) > 0 and verb > 0:
        print(f"total number of accession number \nfor which no gene has been retrieve:    {len(idk)}")
        print("see the notfound.txt for the detail")

else:
    remaining = list(set(listofids) - set(found))
    with open('notfound.text', 'w') as n:
        [n.write(number) for number in remaining]
    #comments:
    if verb > 0:
        print(f'number of unique accession numbers:                                                   {len(listofids)}')
        print(f'number of accession numbers for which a fasta file has been retreived:                {len(found)}')
        print(f'number of accession number without fasta file:                                        {len(remaining)}')
