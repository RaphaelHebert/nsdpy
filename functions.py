import requests             #https://requests.readthedocs.io/en/master/
import os


########################################################################
####################################    main.py    #####################

def esearchquery(QUERY):

    ##unpack QUERY:
    (query, apikey) = QUERY

    ##build api address
    esearchaddress = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    parameters = {}
    #parameters
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
    try:
        y = requests.get(esearchaddress, params = parameters, timeout = 60)

    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return(1)

    except requests.exceptions.Timeout as to:
        print(f'Connection Timed out\n{to}')
        return(1)
    

    except requests.exceptions.ConnectionError as errc:
        print(f'Connection error (check your connection):\n{errc}')
        return(1)

    except requests.exceptions.RequestException as e:
        print(f'An exception occured:\n{e}')
        return(1)
        
    return (y.json())


def taxids(params, path, OPTIONS=("","","","","")):

    ##unpack parameters
    (querykey, webenv, count) = params
    (verb, _, _, fileoutput, _) = OPTIONS

    ##number of accession number to be sent to the API at once
    retmax = 100

    ##filename
    filename = "TaxIDs.txt"
    ##path to filename
    path = path + "/" + filename


    if verb > 0:
        print("retrieving TaxIds...")

    ##retreive the taxids sending batches of accession numbers to esummary
    dictid = {}
    taxid = ''
    seqnb = ''
    for x in range((count//retmax) + 1):
        ##build the API address
        esummaryaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "taxonomy"
        parameters['query_key'] = querykey
        parameters['WebEnv'] = webenv
        parameters['retstart'] = str(x * retmax)
        parameters['retmax'] = str(retmax)
        parameters['rettype'] = "uilist"
        parameters['retmode'] = "text"

        ##loop until download is correct
        connect = 0
        while True:
            try:
                x = requests.get(esummaryaddress, params = parameters,  timeout = 60)
                break

            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
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
        

        if verb > 1:
            ret = parameters['retstart']
            print(f'{round((int(ret)/count)*100, 1)} %  of the TaxIDs downloaded')

    ###extract the TaxIDs and accession numbers (record in text file and in dictid)
    
        f = x.text.splitlines()
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

    #rewrite the text file with only TaxIds and Accession numbers
        if fileoutput:
            with open(path, 'a') as summary:
                [summary.write(f'{key}  {value}\n') for key, value in dictid.items()]
   

    return dictid

def dispatch(lineage, classif):
    Plantae = ['Chlorophyta', 'Charophyta', 'Bryophyta', 'Marchantiophyta', 'Lycopodiophyta', 'Ophioglossophyta', 'Pteridophyta',\
    'Cycadophyta', 'Ginkgophyta', 'Gnetophyta', 'Pinophyta', 'Magnoliophyta', 'Equisetidae', 'Psilophyta', 'Bacillariophyta',\
    'Cyanidiophyta', 'Glaucophyta', 'Prasinophyceae','Rhodophyta']

    Fungi = ['Chytridiomycota', 'Zygomycota', 'Ascomycota', 'Basidiomycota', 'Glomeromycota']

    Metazoa = ['Acanthocephala', 'Acoelomorpha', 'Annelida', 'Arthropoda', 'Brachiopoda', 'Ectoprocta', 'Bryozoa', 'Chaetognatha',\
    'Chordata', 'Cnidaria', 'Ctenophora', 'Cycliophora', 'Echinodermata', 'Echiura', 'Entoprocta', 'Gastrotricha', 'Gnathostomulida',\
    'Hemichordata', 'Kinorhyncha', 'Loricifera', 'Micrognathozoa', 'Mollusca', 'Nematoda', 'Nematomorpha', 'Nemertea', 'Onychophora'\
    'Orthonectida', 'Phoronida', 'Placozoa', 'Plathelminthes', 'Porifera', 'Priapulida', 'Rhombozoa', 'Rotifera', 'Sipuncula',\
    'Tardigrada', 'Xenoturbella']
    
    if classif == 2:
        return "COI"

    if isinstance(classif, list):
        try:
            other = [rank for rank in lineage if rank in classif][0]
        except IndexError:
            other = "OTHERS"
        return other

    if classif == 0:
        try:
            Phylum = [phy for phy in lineage if phy in Metazoa or phy in Fungi or phy in Plantae][0]
        except IndexError:
            Phylum = 'OTHERS'
        return Phylum

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
    
    ## if the users choose to make groupe n rank higher than species (classif >= 3)
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

    ##number of TaxIds to be sent to the API at once
    retmax = 100
    count = len(idlist)

    if verb > 0:
            print("retrieving taxonomy...")
    ##dictionnary that will be returned
    data = {}

    ##retreive the taxonomy sending batches of TaxIds to efetch
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
        connect = 0
        while True:
            try:
                x = requests.get(efetchaddress, params = parameters, timeout = 60)
                break

            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
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

        if verb > 1:
            print(f'{round((int(retstart)/count)*100, 1)} % of the taxonomy found')

        ##analyse the results from efetch
        x = x.text
        x = x.split('</Taxon>\n<Taxon>')
        for seq in x:
            dicttemp = {}
            try:
                TaxId , _ = seq.split('</TaxId>', 1)
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
                rank = "COI"
            else:
                rank = dispatch(lineage, classif)

            dicttemp['dispatch'] = rank

            try:
                Division , _ = seq.split('</Division>', 1)
                _, Division = Division.split('</Division>', 1)    
            except ValueError:
                Division = 'not found'
            dicttemp['Division'] = Division

            data[TaxId] = dicttemp

    if verb > 0:
        print(f'number of taxids:{len(data.keys())}')

    return data


##the feattable function dl the feat table by batch of 'retmax' for the seq access found by an esearch request returning a querykey and a webenv variable
def feattable(params, path, dictid, dicttaxo, QUERY, OPTIONS=("","","","","")):
    
    ##unpack parameters
    (querykey, webenv, count) = params
    (_, apikey) = QUERY
    (verb, genelist, _, _, fileoutput)= OPTIONS

    if fileoutput:
        ##filename
        filename = "featuretable.txt"
        ##path to filename
        feattablename = path + "/" + filename

    ##number of accession numbers to be sent at each API query
    retmax = 100
    if verb > 0:
            print("retrieving the feature tables...")

    #list of accession number for wich a COI is found:
    found = []

    for x in range((count//retmax) + 1):
        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "nucleotide"
        parameters['query_key'] = querykey
        parameters['WebEnv'] = webenv
        parameters['retstart'] = str(x * retmax)
        parameters['retmax'] = str(retmax)
        parameters['rettype'] = "fasta_cds_na"
        parameters['retmode'] = "text"
        if apikey:
            parameters["api_key"] = apikey
            
        ##send requests to the API until getting a result
        connect = 0
        while True:
            try:
                result = requests.get(efetchaddress, params = parameters, timeout = 60)
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
        
        result = result.text
        ##append the feature table file in a text file
        if fileoutput:
            with open(feattablename, 'a') as dl:
                dl.write(result)

        ##analyse the results     
        sublist = extract(path, result, dictid, dicttaxo, genelist, verb)
        found = found + sublist
        ##output % done in terminal
        if verb > 1:
            start = parameters['retmax']
            print(f'{round(((x * int(start))/count)*100, 1)} %  of the feature tables downloaded')

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
        Division = dicttaxo[TaxId]['Division']
        Name = dicttaxo[TaxId]['Name']  
        dispatch = dicttaxo[TaxId]['dispatch']
    except KeyError:
        return 

    ##check if COI
    #coilist0 = ["=COX1]", "=Cox1]", "=cox1]", "=co1]", "=CO1]", "=Co1]", "=COXI]", "=CoxI]", "=coxI]", "=coi]", "=COI]"]
    ok = [ 1 if len(seq.split(co)) > 1 else 0 for co in genelist]
    if 1 in ok:
        ##get the Sequence
        description, dna = seq.split('\n', 1)

        try:
            _ ,location = description.split('[location=', 1)
            location, _ = location.split(']',1)
        except ValueError:
            print('location')
            location = 'not found'
        
        Lineage = ", ".join(Lineage)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        idline = '> Accession number: ' + str(key) + '|Name:' + Name +  '|TaxId:' + TaxId + '|Lineage:' + Lineage +\
        '|Division:' + Division  + '|Location:' + location

        path = path + "/" + dispatch + ".fasta"
        with open(path, 'a') as new:
            new.write('\n' + str(idline) + '\n' + str(dna) +'\n') 
        return key
    else:
        return 


def extract(path, text, dictid, dicttaxo, genelist, verb):
    if verb > 0:
        print('analyzing the results...')
    
    genelist = [ "=" + gene + "]" for gene in genelist]
    ##extract sequences from input file (seq by seq)
    found = []
    seq = ''
    text = text.splitlines()
    for line in text:
        if len(line.split(">lcl|")) > 1:
            if seq:
                try:
                    x = subextract(seq, path, dictid, dicttaxo, genelist)
                    if x:
                        found.append(x)
                except:
                    pass
            seq = str(line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        else:
            seq = seq + '\n' + line

    return (found)


def taxo(path, listofid, dictid, dicttaxo, QUERY, OPTIONS=""):
    if len(listofid) < 1:
        return

    ##unpack params
    (verb, genelist, classif, _, _) = OPTIONS
    (_, apikey) = QUERY

    ##build output unique filename
    notfound = path + "/notfound.txt"
    countnotfound = 0

    count = len(listofid)
    #number of accession number to be send in each API call:
    retmax = 10
    #format the expression to be found in 'gene' (from gene and CDS section of the gb file)
    genelist = ['gene=' + '"' + gene + '"' for gene in genelist]

    remain = {}
    analysed = []
    if verb > 0:
        print("Looking for the COI for the remaining accession numbers...")

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
        parameters['db'] = "nucleotide"
        parameters['id'] = ids1
        parameters['rettype'] = "gb"
        parameters['retmode'] = "text"
        if apikey:
            parameters["api_key"] = apikey
        
        ##loop until dl is correct
        connect = 0
        while True:
            try:
                x = requests.get(efetchaddress, params = parameters)
                break

            except requests.exceptions.HTTPError as errh:
                print("Http Error:",errh)
                continue

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

        #######################   RESULT ANALYZING   ##########################
        x = x.text
        x = x.split('//')

        for i, seq in enumerate(x[:-1]):
            ##EXTRACT THE ACCESSION NUMBER
            try:
                version = seq.split('ACCESSION', 1)[1]
                version = version.split('\n', 1)[0]
                version = version.split()[0]
                version = version.strip()
                foundlist.append(version)
            except IndexError:
                continue
            ###LOOK FOR COX1 IN gene
            genes = seq.split('gene  ')
            try:
                genes = [(gene.split('\n')[0].strip(), gene.split('\n')[1].strip().split(' ')[0].strip(' /'))\
                    for gene in genes if gene.split('\n')[1].strip().split(' ')[0].strip(' /') in genelist]
            except IndexError:
                pass

            ###LOOK FOR COX1 IN cds
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
            if (len(genes) == 0 and CDS[0] == (0,0)) or not dna:
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
                elif len(CDS) > 0:
                    loc1 = CDS0
                    COI = [dna[int(c[0]): int(c[1])] for c in CDS]
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
                Division = dicttaxo[TaxId]['Division']
                Name = dicttaxo[TaxId]['Name']
            except KeyError:
                TaxId = 'not found'
                Lineage = 'not found'
                Division = 'not found'
                Name = 'not found'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

            ##if no name or lineage try to retreive them from the gb file
            if Lineage == 'not found':
                try:
                    _, Lineage = seq.split('ORGANISM',1)
                    _, Lineage = Lineage.split('\n',1)
                    Lineage, _ = Lineage.split('REFERENCE', 1)
                    Lineage = Lineage.strip()
                    Lineage = Lineage.split("; ")
                except ValueError:
                    pass
            if Name == 'not found':
                try:
                    _ , organism = seq.split('ORGANISM', 1)
                    organism, _ = organism.split('\n', 1)
                except ValueError:
                    pass

            Lineage = ", ".join(Lineage)
            idline = '> Accession number: ' + str(version) + '|Name:' + Name +  '|TaxId:' + TaxId + '|Lineage:' + Lineage\
                + '|Division:' + Division  + '|Location:' + loc1
            
            
            Lineage = Lineage.split(", ")
            if classif == 2:
                rank = "COI"
            else:
                rank = dispatch(Lineage, classif)
            towrite = path + "/" + rank + ".fasta"

            coilen = len(''.join(COI))
            ##output the result
            with open(towrite, 'a') as dl:
                dl.write(f'{idline}\n')
                [dl.write(c + '\n') for c in COI]
            analysed.append(version)

        remain = set(ids) - set(foundlist)

        if verb > 1:
            print(f'{round((int(retstart)/count)*100, 1)} %  of the remaining  analysis done')

    return analysed, countnotfound

