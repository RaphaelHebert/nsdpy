from functions import esearchquery, completetaxo, taxids, feattable, extract, taxo
import sys
import os
import argparse             #parsing command line arguments
from datetime import datetime    


##############################################
########### DEFAULT DATA #####################
##############################################

##for the taxo function keep the "" around the coi exp:'gene="CO1"'
COIs = ["COX1", "Cox1", "cox1", "co1", "CO1", "Co1", "COXI", "CoxI", "coxI", "coi", "COI", "MTCO1", "cytochrome c oxidase subunit I", "cytochrome oxidase subunit I"]
RBCLs = []
#rbcL, MatK etc


############################################
########## CHECK ARGUMENTS #################
############################################

parser = argparse.ArgumentParser()
##POSITIONAL ARGUMENTS
parser.add_argument("query", help="The query to the NCBI database")
parser.add_argument("key", default=None, nargs='?', help="API key (register to NCBI to get an API key)")
##OPTIONAL ARGUMENTS
#verbose
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="Diplays downloads progress and actions", action="store_true")
group.add_argument("-q", "--quiet", help="No verbose output", action="store_true")
#gene selection
group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-C", "--COI", help="Search for the cytochrome oxydase subunit I gene, default option", action="store_true" )
group2.add_argument("-R", "--RIBULOSE",help="search for the rbcL gene", action="store_true")
group2.add_argument("-O", "--OTHER", help="search for a given list of gene, exp: COX1 COX2 COX3", nargs="+")
#file output
parser.add_argument("-T", "--TAXIDS", help='write a text file listing all the accession numbers and their related TaxIDs', action="store_true")
parser.add_argument("-F", "--FEATURE", help='write a text file listing the feature tables', action="store_true")
#Taxonomy
group3 = parser.add_mutually_exclusive_group()
group3.add_argument("-k", "--kingdom", help="output three different file text (Plantae and Fungi, Metazoa, Others", action="store_true" )
group3.add_argument("-p", "--phylum", help="output one file text per phylum", action="store_true" )
group3.add_argument("-l", "--levels", help="find only the taxon given by user", nargs="+")
group3.add_argument("-s", "--species", help="classify the results in different text file one for each specie+n level found, exp: -s correspond to lowest levels, -ss 2nd lowest, -sssss 5th lowest and so on", action="count", default=2)

args = parser.parse_args()



#################################################
#############   GLOBAL VARIABLES    #############
#################################################
    ##for testing only
    #apikey = '66ab22581a26c4fdc8e74788e8562502a308'
    #query = '((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))'
 
#verbose
if args.verbose:
    verb = 2
elif args.quiet:
    verb = 0
else:
    verb = 1

#gene selection
if args.RIBULOSE:
    genelist = RBCLs
elif args.OTHER:
    genelist = args.OTHER
else:
    genelist = COIs

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
QUERY = (args.query, args.key)
##foldername and path
#create the name
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
if y == 1:
    sys.exit("Program terminated.")
    
##check errors (if bad API key etc) errors returned by the Entrez API
if "error" in y.keys():
    errors = y["error"]
    sys.exit(errors)

count = int(y["esearchresult"]["count"])
webenv =  str(y["esearchresult"]["webenv"])
querykey = str(y["esearchresult"]["querykey"])
##for testing purpose
#count = 500

params = (querykey, webenv, count)

if verb > 0:    
    print(f'Number of results found: {count}')

###Taxids
dictid = taxids(params, path, OPTIONS)
if dictid == 1:
    sys.exit("Program terminated.")

listofids = list(dictid.keys())

##select TaxIDs
reverse = {value for value in dictid.values()}
listofTaxids = list(reverse)

###completetaxo2
dicttaxo = completetaxo(listofTaxids, QUERY, OPTIONS)
if dicttaxo == 1:
    sys.exit("Program terminated.")

###feattable
found = feattable(params, path, dictid, dicttaxo, QUERY, OPTIONS)
if found == 1:
    sys.exit("Program terminated.")
    
# ###extract
# found = extract(path, dictid, dicttaxo, genelist, args.FEATURE, verb)

###list the remaining access id:
remaining = set(listofids) - set(found)
remaining = list(remaining)
if verb > 0:
    print(f'number of remaining accession numbers with no COI found: {len(remaining)}')

###analyse
analyse = taxo(path, remaining, dictid, dicttaxo, QUERY, OPTIONS)

if verb > 0:
    print(f'number of unique accession numbers:{len(listofids)}')
    print(f'number of COI found in the feature table: {len(found)}')
    print(f'number of COI found in gb file: {len(analyse)}')
    print(f'total number of accession number analysed: {len(set(analyse)) + len(set(found))}')

allaccess = dictid.keys()
idk = set(allaccess) - (set(analyse) | set(found))

if len(list(idk)) > 0 and verb > 0:
    print(f"These accession numbers were not analyzed; {idk}")
