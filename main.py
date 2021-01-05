from functions import esearchquery, completetaxo, taxids, feattable, extract, taxo
import sys


###check if filename is given as an argument
if len(sys.argv) < 2:
    sys.exit("!usage: python3 main.py request [API key]")

###get the search phrase to the esearch API
query = sys.argv[1]

##if more arguments are provided..
if len(sys.argv) > 2:
    apikey = sys.argv[2]
else:
    apikey = ""

#query = input('Enter your query:\n')
#apikey = '66ab22581a26c4fdc8e74788e8562502a308'
query = '((mitochondrion[Title]) AND (complete[Title]) AND ("CO*" OR "COX1"))'

###esearchquery
y = esearchquery(query, apikey)
if y == 1:
    sys.exit("Program terminated.")
    
##check errors (if bad API key etc) errors returned by the Entrez API
if "error" in y.keys():
    errors = y["error"]
    sys.exit(errors)

count = int(y["esearchresult"]["count"])
webenv =  str(y["esearchresult"]["webenv"])
querykey = str(y["esearchresult"]["querykey"]) 
print(f'Number of results found: {count}')

###Taxids
dictid = taxids(querykey, webenv, count)
if dictid == 1:
    sys.exit("Program terminated.")

listofids = list(dictid.keys())

##select TaxIDs
reverse = {value for value in dictid.values()}
listofTaxids = list(reverse)

###completetaxo2
dicttaxo = completetaxo(listofTaxids, apikey)
if dicttaxo == 1:
    sys.exit("Program terminated.")
    
###feattable
feattablename = feattable(querykey, webenv, count, apikey)
if feattablename == 1:
    sys.exit("Program terminated.")
    
###extract
found, COIfasta = extract(feattablename, dictid, dicttaxo)

###list the remaining access id:
remaining = set(listofids) - set(found)
remaining = list(remaining)
print(f'number of accession number to send to analyse: {len(remaining)}')

###analyse
analyse = taxo(COIfasta, remaining, dictid, dicttaxo, apikey)

print(f'number of unique accession numbers:{len(listofids)}')
print(f'number of COI found in the feature table: {len(found)}')
print(f'number of COI found in gb file: {len(analyse)}')


print(f'total number of accession number analysed: {len(set(analyse)) + len(set(found))}')

allaccess = dictid.keys()

idk = set(allaccess) - (set(analyse) | set(found))

print(idk)
