import requests             #https://requests.readthedocs.io/en/master/
import os
import re

def download(parameters, address):
    ##send requests to the API until getting a result
    connect = 0
    while True:
        try:
            result = requests.get(address, params = parameters, timeout = 60)
            break
        except requests.exceptions.HTTPError as errh:
            print("Http Error:",errh)
            return(1)

        except requests.exceptions.Timeout as to:
            print(f'Connection Timed out\n{to}')
            continue

        except requests.exceptions.ConnectionError as errc:
            if connect == 1:
                continue
            elif connect == 0:
                connect = 1
                print(f'Connection error (please reconnect)\n ')
                continue

        except requests.exceptions.RequestException as e:
            print(f'An exception occured:\n{e}')
            continue

    return result


def esearchquery(QUERY):
    ##unpack QUERY:
    (query, apikey) = QUERY

    ##build api address
    esearchaddress = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    #parameters
    parameters = {}
    if apikey:
        parameters["api_key"] = str(apikey)
    parameters["db"] = "nucleotide"
    parameters["idtype"] = "acc"
    parameters["retmode"] = "json"
    parameters["retmax"] = "0"
    parameters["usehistory"] = "y"    
    #user's query
    parameters["term"] = query
    
    ###send request to the API
    y = download(parameters, esearchaddress)  

    return (y.json())


def taxids(params, path, OPTIONS=("","","","","")):

    ##unpack parameters
    (querykey, webenv, count) = params
    (verb, _, _, fileoutput, _) = OPTIONS

    ##filename
    filename = "TaxIDs.txt"
    ##path to filename
    path = path + "/" + filename

    #comments
    if verb and verb > 0:
        print("retrieving TaxIds...")

    ##retreive the taxids sending batches of accession numbers to esummary
    retmax = 100
    dictid = {}
    taxid = ''
    seqnb = ''
    for x in range((count//retmax) + 1):
        ##build the API address
        esummaryaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        #parameters 
        parameters = {}
        parameters['db'] = "taxonomy"
        parameters['query_key'] = querykey
        parameters['WebEnv'] = webenv
        parameters['retstart'] = str(x * retmax)
        parameters['retmax'] = str(retmax)
        parameters['rettype'] = "uilist"
        parameters['retmode'] = "text"

        result = download(parameters, esummaryaddress)

        #comments
        if verb and verb > 1:
            ret = parameters['retstart']
            print(f'{round((int(ret)/count)*100, 1)} %  of the TaxIDs downloaded')

        ###extract the TaxIDs and accession numbers (record in text file and in dictid)
        f = result.text.splitlines()
        for line in f:
            if len(line.split('<DocSum>')) > 1:
                taxid = ''
                seqnb = ''
            else: 
                caption = line.split('<Item Name="Caption" Type="String">', 1)
                if len(caption) > 1:
                    seqnb = caption[1].split("<")[0].strip()

                TaxId = line.split('<Item Name="TaxId" Type="Integer">', 1)
                if len(TaxId) > 1:
                    taxid = TaxId[1].split("<")[0].strip()
                
                if seqnb:
                    dictid[seqnb] = taxid 

        if fileoutput:
            with open(path, 'a') as summary:
                [summary.write(f'{key}  {value}\n') for key, value in dictid.items()]
   
    return dictid


def dispatch(lineage, classif):
    ###Phylums
    Plantae = ['Chlorophyta', 'Charophyta', 'Bryophyta', 'Marchantiophyta', 'Lycopodiophyta', 'Ophioglossophyta', 'Pteridophyta',\
    'Cycadophyta', 'Ginkgophyta', 'Gnetophyta', 'Pinophyta', 'Magnoliophyta', 'Equisetidae', 'Psilophyta', 'Bacillariophyta',\
    'Cyanidiophyta', 'Glaucophyta', 'Prasinophyceae','Rhodophyta']
    Fungi = ['Chytridiomycota', 'Zygomycota', 'Ascomycota', 'Basidiomycota', 'Glomeromycota']
    Metazoa = ['Acanthocephala', 'Acoelomorpha', 'Annelida', 'Arthropoda', 'Brachiopoda', 'Ectoprocta', 'Bryozoa', 'Chaetognatha',\
    'Chordata', 'Cnidaria', 'Ctenophora', 'Cycliophora', 'Echinodermata', 'Echiura', 'Entoprocta', 'Gastrotricha', 'Gnathostomulida',\
    'Hemichordata', 'Kinorhyncha', 'Loricifera', 'Micrognathozoa', 'Mollusca', 'Nematoda', 'Nematomorpha', 'Nemertea', 'Onychophora'\
    'Orthonectida', 'Phoronida', 'Placozoa', 'Plathelminthes', 'Porifera', 'Priapulida', 'Rhombozoa', 'Rotifera', 'Sipuncula',\
    'Tardigrada', 'Xenoturbella']

    ##no option selected
    if classif == 2:
        return "results"
    ##user gave list of taxonomic levels
    if isinstance(classif, list):
        try:
            other = [rank for rank in lineage if rank in classif][0]
        except IndexError:
            other = "OTHERS"
        return other
    ##phylums
    if classif == 0:
        try:
            Phylum = [phy for phy in lineage if phy in Metazoa or phy in Fungi or phy in Plantae][0]
        except IndexError:
            Phylum = 'OTHERS'
        return Phylum
    ##kingdoms
    if classif == 1:
        if 'Metazoa' in lineage or len(list(set(lineage) & set(Metazoa))) > 0:
            kingdom = "METAZOA"
        elif "Viridiplantae" in lineage or len(list(set(lineage) & set(Plantae))) > 0:
            kingdom = "PLANTAE" 
        elif "Fungi" in  lineage or len(list(set(lineage) & set(Fungi))) > 0:
            kingdom = "FUNGI" 
        else:
            kingdom = "OTHERS"
        return kingdom
    ##if the users choose to make groupe n rank higher than species (classif >= 3)
    classif = -(int(classif) - 2)
    try:
        rank = lineage[classif]
    except IndexError:
        rank = "OTHERS"
    return rank


#query taxonomy with efetch, returns a dict with taxid as key and info in a dict as value
def completetaxo(idlist, QUERY, OPTIONS):

    ##unpack parameters
    (_, apikey) = QUERY
    (verb, _, classif, _, _) = OPTIONS

    if verb and verb > 0:
        print("retrieving taxonomy...")
    ##dictionnary that will be returned
    data = {}

    ##retreive the taxonomy sending batches of TaxIds to efetch
    #number of TaxIds to be sent to the API at once
    retmax = 100
    count = len(idlist)
    for x in range((count//retmax) + 1):
        ##slice the idlist
        retstart = x * retmax
        idsublist = idlist[retstart:(retstart+retmax)]
        idsublist = ','.join(idsublist)

        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "taxonomy"
        parameters['id'] = idsublist
        if apikey:
            parameters['api_key'] = apikey

        ##loop until download is correct
        result = download(parameters, efetchaddress)

        #comments
        if verb > 1:
            print(f'{round((int(retstart)/count)*100, 1)} % of the taxonomy found')

        ##analyse the results from efetch
        result = result.text.split('</Taxon>\n<Taxon>')
        for seq in result:
            dicttemp = {}
            try:
                TaxId, _ = seq.split('</TaxId>', 1)
                _, TaxId = TaxId.split('<TaxId>', 1)
                TaxId = TaxId.strip()    
            except ValueError:
                TaxId = 'not found'

            #check if the taxonomy for a given TaxId is already in memory
            if TaxId in data.keys():
                continue
            
            try:
                Name , _ = seq.split('</ScientificName>', 1)
                _, Name = Name.split('<ScientificName>', 1)    
            except ValueError:
                Name = 'not found'
            dicttemp['Name'] = Name

            try:
                Lineage , _ = seq.split('</Lineage>', 1)
                _, Lineage = Lineage.split('<Lineage>', 1)    
            except ValueError:
                Lineage = 'not found'
            lineage = Lineage.split('; ')
            dicttemp['Lineage'] = lineage

            ##dispatch
            if classif == 2:
                rank = "results"
            else:
                rank = dispatch(lineage, classif)
            dicttemp['dispatch'] = rank

            data[TaxId] = dicttemp

    #comments
    if verb and verb > 0:
        print(f'number of taxids:{len(data.keys())}')

    return data


##dl the CDS fasta files by batch of 'retmax' for the seq access found by an esearch request returning a querykey and a webenv variable
def cdsfasta(params, path, dictid, dicttaxo, QUERY, OPTIONS=("","","","","")):
    
    ##unpack parameters
    (querykey, webenv, count) = params
    (_, apikey) = QUERY
    (verb, genelist, _, _, fileoutput)= OPTIONS

    #comment:
    if verb and verb > 0:
        print("retrieving the cds fasta files...")
    

    #list of accession number for wich a gene is found or the file has been retrieve if no gene filter:
    found = []
    #number of accession numbers to be sent at each API query
    retmax = 100
    for x in range((count//retmax) + 1):
        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "nuccore"
        parameters['query_key'] = querykey
        parameters['WebEnv'] = webenv
        parameters['retstart'] = str(x * retmax)
        parameters['retmax'] = str(retmax)
        if apikey:
            parameters["api_key"] = apikey
        parameters['rettype'] = "fasta_cds_na"
        parameters['retmode'] = "text"
        ##send requests to the API until getting a result
        result = download(parameters, efetchaddress)
        result = result.text

        ##append the feature table file in a text file (option -F)
        if fileoutput:
            with open(path + "/featuretable.txt", 'a') as dl:
                dl.write(result)

        ##analyse the results     
        sublist = extract(path, result, dictid, dicttaxo, genelist, verb)
        found = found + sublist

        #comments
        if verb > 1:
            start = parameters['retmax']
            print(f'{round(((x * int(start))/count)*100, 1)} %  of the CDS fasta files downloaded')

    return found


def subextract(seq, path, dictid, dicttaxo, genelist):
    ###find coi in a seq and write to ouput file
    ##extract accession number
    try:
        key = seq.split(">lcl|")[1].split(".")[0]
    except IndexError:
        return    

    ##build idline (retreive info)
    try:
        TaxId = dictid[key]
    except KeyError:
        return 
    try:
        Lineage = dicttaxo[TaxId]['Lineage']
        Name = dicttaxo[TaxId]['Name']  
        dispatch = dicttaxo[TaxId]['dispatch']
    except KeyError:
        return

    if not dispatch:
        dispatch = "results"

    if not Lineage or not Name:
        return

    ##check if genes
    
    check = [1 for co in genelist if len(re.split(co, seq, flags=re.IGNORECASE)) > 1]
    if 1 in check or not genelist:
        ##get the Sequence
        description, dna = seq.split('\n', 1)
        try:
            _ ,location = description.split('[location=', 1)
            location, _ = location.split(']',1)
        except ValueError:
            location = 'not found'
        
        Lineage = ", ".join(Lineage)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        idline = '>' + str(key) + ' |' + Name +  '|' + TaxId + '|' + Lineage +\
        '|' + location

        path = path + "/" + dispatch + ".fasta"
        with open(path, 'a') as new:
            new.write('\n' + str(idline) + '\n' + str(dna) +'\n') 
        return key

    else:
        return


def extract(path, text, dictid, dicttaxo, genelist, verb=""):
    #comments
    if verb and verb > 1:
        print('analyzing the results...')
    
    found = []
    genelist = [ "=" + gene + "]" for gene in genelist]        
    seq = ''
    text = text.splitlines()
    if not text:
        return

    for line in text:
        if len(line.split(">lcl|")) > 1:
            if seq:
                try:
                    result = subextract(seq, path, dictid, dicttaxo, genelist)
                    if result:
                        found.append(result)
                except:
                    pass
            seq = str(line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        else:
            seq = seq + '\n' + line

    return (found)


def taxo(path, listofid, dictid, dicttaxo, QUERY, OPTIONS=("","","","","")):
    if len(listofid) < 1:
        return

    ##unpack params
    (verb, genelist, classif, _, _) = OPTIONS
    (_, apikey) = QUERY

    ##build output unique filename
    notfound = path + "/notfound.txt"

    #format the expression to be found in 'gene' (from gene and CDS section of the gb file)
    if genelist:
        genelist = ['gene=' + '"' + gene + '"' for gene in genelist]

    #comments
    if verb and verb > 0:
        print("Looking for the genes for the remaining accession numbers...")

    remain = {}
    analysed = []
    countnotfound = 0
    count = len(listofid)
    retmax = 10
    for x in range((count//retmax) + 1):
        ###################  API CALL  ##################
        ##slice the list of ids passed to the function
        ids = listofid[x * retmax:(x+1) * retmax]
        ##if some ids haven't been dl at the last call add them to this call
        if remain:
            ids = ids + list(remain)
        foundlist = []
        ids1 = ",".join(ids) 
        COI = ''
        retstart = str(x * retmax)

        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "nuccore"
        parameters['id'] = ids1
        parameters['rettype'] = "gb"
        parameters['retmode'] = "text"
        if apikey:
            parameters["api_key"] = apikey
        
        ##loop until dl is correct
        result = download(parameters, efetchaddress)
        result = result.text
        #######################   RESULT ANALYZING   ##########################
        result = result.split('//')

        for i, seq in enumerate(result[:-1]):
            ##EXTRACT THE ACCESSION NUMBER
            try:
                version = seq.split('ACCESSION', 1)[1]
                version = version.split('\n', 1)[0]
                version = version.split()[0]
                version = version.strip()
                foundlist.append(version)
            except IndexError:
                continue

            ###Look for genes in gene
            genes = []
            CDS = [(0,0)]
            
            #option genes
            if genelist:
                genes = seq.split('gene  ')
                try:
                    genes = [(gene.split('\n')[0].strip(), gene.split('\n')[1].strip().split(' ')[0].strip(' /'))\
                        for gene in genes if 1 in [1 for g in genelist if re.findall(g, gene.split('\n')[1].strip().split(' ')[0].strip(' /'), flags=re.IGNORECASE)]]  
                except IndexError:
                    pass

                ###LOOK FOR genes IN cds
                ##get location from the CDS:
                try:
                    CDS1 = seq.split('CDS  ')
                    CDS = [c.split('\n')[0].strip() for c in CDS1 if c.split('\n')[1].strip().split(' ')[0].strip(' /') in genelist]
                    if len(CDS) == 0:
                        try:
                            CDS = [c.split('\n')[0].strip() for c in CDS1[1:] if c.split('/product="')[1].split('"')[0] in genelist]
                            # CDS = [c.split('\n')[0].strip() for c in CDS1[1:] if c.split('/product="')[1].split('"')[0] == "cytochrome c oxidase subunit I"]
                            # if len(CDS) == 0:
                            #     CDS = [c.split('\n')[0].strip() for c in CDS1[1:] if c.split('/product="')[1].split('"')[0] == "cytochrome oxidase subunit I"]
                        except IndexError:
                            pass
                    CDS0 = CDS[0]
                    CDS1 = CDS[0]
                    try:
                        CDS1 = CDS1.split('complement(')[1].strip('()')[0]
                    except IndexError:
                        pass
                    try:
                        CDS1 = CDS1.split('join(')[1].strip('()')
                    except IndexError:
                        pass
                    CDS = CDS1.split(',')
                    CDS = [(c.split('..')[0].strip('<'), c.split('..')[1].strip('>')) for c in CDS]
                except:
                    CDS = [(0,0)]

            ###extract the whole seq of the organism
            try:
                dna = seq.split('ORIGIN', 1)
                dna = dna[1].split('\n')
                dna = [d.strip().strip('1234567890)') for d in dna]
                dna = ''.join(dna)
                dna = ''.join(dna.split())
            except:
                dna = ''

            ###If nothing is found
            if not dna or (len(genes) == 0 and CDS[0] == (0,0)):
                with open(notfound, 'a') as nf:
                    nf.write(f'{version}    No COI found in gb file error#1\n')
                countnotfound += 1                
                continue

            try:
                if len(genes) > 0:
                    ##extract location from gene
                    gene = genes[0][0]
                    try:
                        gene = gene.split('complement(')[1].strip('()')
                    except IndexError:
                        pass
                    try:
                        gene = gene.split('join(')[1].strip('()')
                    except IndexError:
                        pass
                    gene = gene.split(',')
                    gene = [(g.split('..')[0].strip('<'), g.split('..')[1].strip('>')) for g in gene]
                    
                    ##check that the start and stop of gene location correspond to the start and stop of the CDS
                    if (int(gene[0][0]) == int(CDS[0][0]) and int(gene[-1][1]) == int(CDS[-1][1])) or len(gene) == 0:
                        ##extract from the CDS
                        loc1 = CDS0
                        COI = [dna[int(c[0]): int(c[1])] for c in CDS]
                    else:
                        loc1 = genes[0][0]
                        COI = [dna[int(g[0]): int(g[1])] for g in gene]
                elif CDS[0] != (0,0):
                    loc1 = CDS0
                    COI = [dna[int(c[0]): int(c[1])] for c in CDS]

                #no option gene
                elif not genelist:
                    try:
                        loc1 = seq.split('source   ')[1].split('\n')[0].strip()
                    except IndexError:
                        loc1 = "not found"
                    COI = dna

                else:
                    ###should not happen
                    with open(notfound, 'a') as nf:
                        nf.write(f'{version}    No COI found in gb file error#2\n')
                    countnotfound += 1
                    continue
                
                ###COI lists to display 80 char per line
                COI = ''.join(COI)
                COI = [''.join(COI[i:i + 80]) for i, t in enumerate(list(COI)) if i % 80 == 0]
                analysed.append(version)

            except:
                ###should not happen
                with open(notfound, 'a') as nf:
                    nf.write(f'{version}    No COI found in gb file error#3\n')
                countnotfound += 1
                continue
        
            ##build idline
            try:
                TaxId = dictid[version]
                Lineage = dicttaxo[TaxId]['Lineage']
                Name = dicttaxo[TaxId]['Name']
            except KeyError:
                TaxId = "not found"
                Lineage = ""
                Name = ""  

            ##if no name or lineage try to retreive them from the gb file
            if not Lineage:
                try:
                    _, Lineage = seq.split('ORGANISM',1)
                    _, Lineage = Lineage.split('\n',1)
                    Lineage, _ = Lineage.split('REFERENCE', 1)
                    Lineage = Lineage.strip()
                    Lineage = Lineage.split(";")
                except ValueError:
                    Lineage = 'not found'
                    pass
            if not Name:
                try:
                    _ , organism = seq.split('ORGANISM', 1)
                    organism, _ = organism.split('\n', 1)
                except ValueError:
                    Name = 'not found'
                    pass

            Lineage = ",".join(Lineage)
            Lineage = Lineage.split("\n")
            Lineage = [l.strip() for l in Lineage]
            Lineage = " ".join(Lineage)


            idline = '>' + str(version) + ' |' + Name +  '|' + TaxId + '|' + Lineage\
                + '|' + loc1
            
            
            Lineage = Lineage.split(", ")
            if classif == 2:
                #no taxonomy option
                rank = "results"
            else:
                rank = dispatch(Lineage, classif)
            filename = path + "/" + rank + ".fasta"

            coilen = len(''.join(COI))
            ##output the result
            with open(filename, 'a') as dl:
                dl.write(f'{idline}\n')
                [dl.write(c + '\n') for c in COI]
                dl.write("\n")
            analysed.append(version)

        remain = set(ids) - set(foundlist)

        #comments
        if verb > 1:
            print(f'{round((int(retstart)/count)*100, 1)} %  of the remaining  analysis done')

    return analysed, countnotfound


def fasta(path, dictid, dicttaxo, QUERY, listofids, OPTIONS=("","","","","")):
    
    ##unpack parameters
    (_, apikey) = QUERY
    (verb, _, _, _, fileoutput)= OPTIONS

    if verb and verb > 0:
        print("Downloading fasta files...")

    retmax = 10
    keys = []
    count = len(listofids)
    for x in range((count//retmax) + 1):
        ##split the list of ids
        ids = listofids[x*retmax : (x*retmax) + retmax]
        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "nuccore"
        parameters['id'] = ",".join(ids)
        if apikey:
            parameters["api_key"] = apikey
        parameters['rettype'] = "fasta"
        parameters['retmode'] = "text"


        ##send requests to the API until getting a result
        result = download(parameters, efetchaddress)
        result = result.text
        if fileoutput:
            with open(path + "/fastafiles.fasta", "a") as f:
                f.write(result)

        result = result.split('>')
        for seq in result:
            try:
                idline, dna = seq.split('\n', 1)
            except ValueError:
                continue
            try:
                key = idline.split(".")[0]
            except IndexError:
                print('no key found')
                continue
            
            try:
                taxid = dictid[key]
                lineage = dicttaxo[taxid]['Lineage']
                name = dicttaxo[taxid]['Name']
                dispatch = dicttaxo[taxid]['dispatch']
                lineage = ", ".join(lineage)
            except KeyError:
                taxid = 'not found'
                lineage = 'not found'
                name = 'not found'
                if fileoutput:
                    dispatch = 'others'
                else:
                    dispatch = 'results'

            idline = ">" + key + " |" + name + "|" + name + "|" + lineage + "|fasta"
            
            with open(path + "/" + dispatch + ".fasta", 'a') as f:
                f.write(f"{idline}\n")
                f.write(f"{dna}\n")
            keys.append(key)

        if verb > 1:
            start = (x*retmax) + retmax
            print(f'{round((start/count)*100, 1)} %  of the fasta files downloaded')

    
    return keys
            