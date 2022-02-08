import requests             #https://requests.readthedocs.io/en/master/
import os
import re
import csv
from collections import Counter


def download(parameters, address):
    ##send requests to the API until getting a result
    connect = 0
    while True:
        try:
            result = requests.get(address, params = parameters, timeout = 60)
            break
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            return(1)

        except requests.exceptions.Timeout as to:
            print(f'Connection Timed out\n{to}')
            continue

        except requests.exceptions.ConnectionError as _:
            if connect == 1:
                continue
            elif connect == 0:
                connect = 1
                print(f'Connection error (please reconnect)\n ')
                continue

        except requests.exceptions.RequestException as e:
            print(f'An exception occurred:\n{e}')
            continue

    return result


def esearchquery(QUERY):
    ##unpack QUERY:
    (query, api_key) = QUERY

    ##build api address
    esearchaddress = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    #parameters
    parameters = {}
    if api_key:
        parameters["api_key"] = str(api_key)
    parameters["db"] = "nucleotide"
    parameters["idtype"] = "acc"
    parameters["retmode"] = "json"
    parameters["retmax"] = "0"
    parameters["usehistory"] = "y"    
    #user's query
    parameters["term"] = query
    
    ###send request to the API
    y = download(parameters, esearchaddress)
    if y == 1:
        return ({"error": "wrong address for esearch"})  
    return (y.json())


def taxids(params, path, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")

    ##unpack parameters
    (querykey, webenv, count) = params
    (verb, _, _, fileoutput, _, _) = OPTIONS

    ##retreive the taxids sending batches of accession numbers to esummary
    retmax = 100
    dict_ids = {}
    taxid = ''
    seqnb = ''

    if count % retmax == 0:
        nb = count//retmax
    else: 
        nb = (count//retmax) + 1
    for x in range(nb):
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
            print(f'{round(((int(ret) + 100)/count)*100, 1)} %  of the TaxIDs downloaded')

        ###extract the TaxIDs and accession numbers (record in text file and in dict_ids)
        f = result.text.splitlines()
        for line in f:
            if len(line.split('<DocSum>')) > 1:
                taxid = ''
                seqnb = ''
            else:
                try:
                    version = line.split('<Item Name="AccessionVersion" Type="String">', 1)[1]
                    seqnb = version.split("<")[0].strip()
                except IndexError:
                    pass

                TaxId = line.split('<Item Name="TaxId" Type="Integer">', 1)
                if len(TaxId) > 1:
                    taxid = TaxId[1].split("<")[0].strip()
                
                if seqnb:
                    dict_ids[seqnb] = taxid 

    if fileoutput:
        ##filename
        filename = "TaxIDs.txt"
        ##path to filename
        path = path + "/" + filename
        with open(path, 'a') as summary:
            [summary.write(f'{key}  {value}\n') for key, value in dict_ids.items()]

    return dict_ids


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
    if classif == 3 or classif == 2:
        return "sequences"
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
    (_, api_key) = QUERY
    (verb, _, classif, _, _, _) = OPTIONS

    if verb and verb > 0:
        print("retrieving taxonomy...")

    ##dictionnary that will be returned
    data = {}
    idlist = [i.split(".")[0] for i in idlist]
    ##retreive the taxonomy sending batches of TaxIds to efetch
    #number of TaxIds to be sent to the API at once
    retmax = 100
    count = len(idlist)
    if count % retmax == 0:                                    
        nb = count//retmax
    else: 
        nb = (count//retmax) + 1

    for x in range(nb):
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
        if api_key:
            parameters['api_key'] = api_key

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
            dicttemp['dispatch'] = dispatch(lineage, classif)

            data[TaxId] = dicttemp

    #comments
    if verb and verb > 0:
        print(f'number of taxids:\t{len(data.keys())}')

    return data


## Download the CDS fasta files by batch of 'retmax' for the seq access found by an esearch request returning a querykey and a webenv variable
def cds_fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")
    
    ## Unpack parameters
    (_, api_key) = QUERY
    (verb, genelist, classif, _, tsv, information)= OPTIONS

    # Comment:
    if verb and verb > 0:
        print("Downloading the CDS fasta files...")

    # Number of accession numbers to be sent at each API query
    retmax = 200    
    # List of accession number for wich a gene is found or the file has been retrieve if no gene filter:
    found = []
    count = len(list_of_ids)

    if count % retmax == 0:
        nb = count//retmax
    else: 
        nb = (count//retmax) + 1

    for x in range(nb):
        ## Split the list of ids
        ids = list_of_ids[x * retmax : (x * retmax) + retmax]
        ## Check that id parameters is not empty
        ids = [i for i in ids if i]
        ## Build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        # Parameters 
        parameters['id'] = ",".join(ids)
        parameters['db'] = "nuccore"
        if api_key:
            parameters["api_key"] = api_key
        parameters['rettype'] = "fasta_cds_na"
        parameters['retmode'] = "text"

        ## Download
        raw_result = download(parameters, efetchaddress)
        raw_result = raw_result.text

        ## Extract available information
        if not information and not genelist and classif == 3:
            result_fasta = raw_result.split(">lcl|")[1:]
            sublist = [r.split("_cds")[0] for r in result_fasta]
  
        ##analyse the results     
        sublist = extract(path, raw_result, dict_ids, dict_taxo, genelist, OPTIONS, verb)

        found = found + sublist
        #comments
        if verb > 1:
            start = parameters['retmax']
            print(f'{round(((x * int(start) + 100)/count)*100, 1)} %  of the CDS fasta files downloaded')

    return found


def subextract(seq, path, dict_ids, dict_taxo, genelist, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")

    (_, _, classif, _, tsv, information) = OPTIONS


    ###find gene in a seq and write to ouput file
    ##extract accession number
    try:
        key = seq.split(">lcl|")[1].split("_cds")[0]
    except IndexError:
        return

    ##extract SeqID
    try: 
        SeqID = seq.split(">lcl|")[1].split(" [")[0]
    except IndexError:
        return

    ##build id_line (retrieve info)
    try:
        TaxId = dict_ids[key]
    except KeyError:
        return 

    ## Extract info
    #Lineage
    try:                                                       
        Lineage = dict_taxo[TaxId]['Lineage']
    except KeyError:
        Lineage = "no info"

    #Name
    try:
        Name = dict_taxo[TaxId]['Name']  
    except KeyError:
        Name = "no info"

    #dispatch
    try:
        dispatch = dict_taxo[TaxId]['dispatch']
    except KeyError:
        dispatch = "others"
    if classif == 3:
        dispatch = "sequences"

    ##check if genes
    check = [1 for reg_exp in genelist if len(re.split(reg_exp, seq, flags=re.IGNORECASE)) > 1]
    if 1 in check or not genelist:
        ##get the Sequence
        _, dna = seq.split('\n', 1)
        
        # if dict_taxo and information:
        if information:
            Lineage = ", ".join(Lineage)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            info_line = Name + '-' + SeqID + ' | ' + TaxId + ' | ' + Lineage 
        else:
            info_line = seq.split('\n', 1)[0]

        # Make only one > and \n
        info_line = '>' + info_line.lstrip(">")
        info_line = info_line.rstrip("\n") + "\n"

        ## Create folders is tsv is selected
        if tsv:
            if not os.path.exists(path + "/fasta"):
                os.makedirs(path + "/fasta")
            if not os.path.exists(path + "/tsv"):
                os.makedirs(path + "/tsv")
            # Create paths
            fasta_file = path + "/fasta/" + dispatch + ".fasta"
            tsv_file = path + "/tsv/" + dispatch + ".tsv"
        else:
            fasta_file = path + "/" + dispatch + ".fasta"
            tsv_file = path + "/" + dispatch + ".tsv"

        # write fasta file
        with open(fasta_file, 'a') as new:
            new.write(str(info_line))
            new.write(str(dna).rstrip("\n") + "\n") 

        # write tsv file
        if tsv:
            # Format dna sequence 
            dna = "".join(dna.split("\n"))

            # write .tsv file
            data = (Name, SeqID, TaxId, Lineage, dna)
            tsv_file_writer(tsv_file, data, OPTIONS)

        return key

    else:
        return


def extract(path, text, dict_ids, dict_taxo, genelist, OPTIONS=None, verb=""):

    # Comments
    if verb and verb > 1:
        print('analyzing the results...')
    
    found = []

    # Extract genes to filter
    genelist = [ "=" + gene + "]" for gene in genelist]  

    seq = ''
    text = text.splitlines()

    if not text:
        return

    for line in text:
        if len(line.split(">lcl|")) > 1:
            if seq:
                try:
                    result = subextract(seq, path, dict_ids, dict_taxo, genelist, OPTIONS)
                    if result:
                        found.append(result)
                except:
                    pass
            seq = str(line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        else:
            seq = seq + '\n' + line

    return found


def fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")
    
    ## Unpack parameters
    (_, api_key) = QUERY
    (verb, _, classif, _, tsv, information)= OPTIONS

    if verb and verb > 0:
        print("Downloading the fasta files...")

    retmax = 200    ## Number of sequences per request to the API
    keys = []
    count = len(list_of_ids)

    if count % retmax == 0:
        nb = count//retmax
    else: 
        nb = (count//retmax) + 1

    for x in range(nb):
        ## Split the list of ids
        ids = list_of_ids[x * retmax : (x * retmax) + retmax]
        ## Check that id parameters is not empty
        ids = [i for i in ids if i]
        ## Build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        # Parameters 
        parameters['db'] = "nuccore"
        parameters['id'] = ",".join(ids)
        if api_key:
            parameters["api_key"] = api_key
        parameters['rettype'] = "fasta"
        parameters['retmode'] = "text"

        ## Download
        raw_result = download(parameters, efetchaddress)
        raw_result = raw_result.text

        ## Extract available informations
        result = raw_result.split('>')

        ## Store analyzed Accession version numbers
        for seq in result:
            try:
                id_line, dna = seq.split('\n', 1)
            except ValueError:
                continue

            try:
                key = id_line.split()[0]
            except IndexError:
                continue
            
            #from dict_ids
            try:
                taxid = dict_ids[key]
            except KeyError:
                taxid = 'not found'
            
            # from dict_taxo
            try:
                lineage = dict_taxo[taxid]['Lineage']
                lineage = ", ".join(lineage)
            except KeyError:
                lineage = 'not found'
            
            try:
                name = dict_taxo[taxid]['Name']
            except KeyError:
                name = 'not found'
            
            try:
                dispatch = dict_taxo[taxid]['dispatch']
            except KeyError:
                name = 'others'
            
            if classif == 3:
                dispatch = "sequences"
            
            data = (name, key, taxid, lineage, dna)

            # Create folders for .tsv files and .fasta files
            if tsv:
                if not os.path.exists(path + "/fasta"):
                    os.makedirs(path + "/fasta")
                if not os.path.exists(path + "/tsv"):
                    os.makedirs(path + "/tsv")
                # Create paths
                fasta_file = path + "/fasta/" + dispatch + ".fasta"
                tsv_file = path + "/tsv/" + dispatch + ".tsv"
            else:
                fasta_file = path + "/" + dispatch + ".fasta"
                tsv_file = path + "/" + dispatch + ".tsv"


            # Write fasta file
            if information: 
                id_line = name + "-" + key + " | " + taxid + " | " + lineage + " | " + id_line
            with open(fasta_file, 'a') as f:
                f.write(f">{id_line}\n")
                f.write(f"{dna}\n")

            if tsv:
                tsv_file_writer(tsv_file, data, OPTIONS)

            keys.append(key)

        if verb > 1:
            start = (x * retmax) + retmax
            print(f'{round((start / count) * 100, 1)} %  of the fasta files downloaded')

    return keys


def duplicates(listofaccess, path):
    filename = path + "/duplicates.txt"
    count = Counter(listofaccess)
    count = dict(count)
    nb = 0
    for key, value in count.items():
        if value > 1:
            nb += 1
            with open(filename, "a") as f:
                f.write(f"{key}   {value}\n")
    return(nb)


def taxo(path, list_of_ids, dict_ids, QUERY, dict_taxo=None, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")

    if len(list_of_ids) < 1:
        return ([],[])

    ##unpack params
    (verb, genelist, classif, _, tsv, information) = OPTIONS
    (_, api_key) = QUERY

    ##build output unique filename
    notfound = path + "/notfound.txt"

    #format the expression to be found in 'gene' (from gene and CDS section of the gb file)
    if genelist:
        genelist = ['[; "()]+' + gene + '["; ()]+' for gene in genelist]

    #comments
    if verb and verb > 0:
        print("Downloading the GenBank files...")

    remain = []         #accessions not downloaded from previous iteration
    analysed = []       #accessions successfully donwnloaded and found in the gb file
    genefound = []      ##accessions with some cds found or matching the filter if filter(s)
    count = len(list_of_ids)
    retmax = 10
    if count % retmax == 0:
        nb = count//retmax
    else: 
        nb = (count//retmax) + 1

    for x in range(nb):
        ###################  API CALL  ##################
        ##slice the list of ids passed to the function
        ids = list_of_ids[x * retmax:(x+1) * retmax]
        ##if some ids haven't been dl at the last call add them to this call
        if remain:
            ids = ids + remain
        ids1 = ",".join(ids)
        retstart = str(x * retmax)

        ##build API address
        efetchaddress = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {}
        #parameters 
        parameters['db'] = "nuccore"
        parameters['id'] = ids1
        parameters['rettype'] = "gb"
        parameters['retmode'] = "text"
        if api_key:
            parameters["api_key"] = api_key
        
        ##loop until dl is correct
        result = download(parameters, efetchaddress)
        result = result.text


        ########################################################################
        #######################   ANALYZING RESULTS   ##########################
        ########################################################################

        result = result.split('\n//')
        ###extract the CDS for each asscession version number
        accessionlist = []
        for i, seq in enumerate(result[:-1]):
            ##search in CDS
            listCDS, dna = genbankfields(seq, genelist)

            for dictCDS in listCDS:
                if dictCDS:
                    accessionlist.append(dictCDS["version"])
                    #select the gene if genes to select
                    if "gene" in dictCDS.keys():
                        ##genefound
                        genefound.append(dictCDS["version"])
                        ###path
                        taxo = dictCDS["taxo"]
                        filename = dispatch(taxo, classif)
                        if tsv:
                            fasta_file = path + "/fasta/" + filename + ".fasta"
                        else:
                            fasta_file = path + "/" + filename + ".fasta"
                        
                        ##information line 
                        taxo = ', '.join(taxo)
                        
                        try:
                            taxid = dict_ids[dictCDS["version"]]
                        except IndexError:
                            taxid = ""

                        if information:
                            try:
                                name = dict_taxo[taxid]['Name']
                            except:
                                name = "not found"
                            info_line = ">" + name + "-" + dictCDS["version"] + "_cds_" + dictCDS["proteinid"].strip('"') + " | " + taxid + " | " +  "".join(taxo).rstrip(".")
                     
                        else:
                            info_line = ">" + dictCDS["version"] + "_cds_" + dictCDS["proteinid"].strip('"') + " [gene=" + dictCDS["gene"] + "] " + "[protein=" + dictCDS["proteinid"] + "] " + \
                                "[location=" + dictCDS["loc"].strip() + "] " + "[gbkey=CDS] " + "[definition=" + " ".join(dictCDS["definition"].split(" " * 12)).rstrip(".") + "]"

                        ## append to file
                        with open(fasta_file, 'a') as a:
                            a.write(f"{info_line}\n")
                            [a.write(f'{"".join(list(dictCDS["sequence"])[i: i + 70]).upper()}\n') for i in range(0, len(dictCDS["sequence"]), 70)]

        remain = list(set(accessionlist) - set(ids))
        analysed = analysed + accessionlist

        #comments
        if verb > 1:
            print(f'{round(((int(retstart))/count)*100, 1)} %  of the remaining  analysis done')

    if remain:
        for number in remain:
            with open(notfound, 'a') as nf:
                nf.write(f'{number}    Accession number not found in gb files\n')

    #accessions found in bg file wihtout matching gene
    nogene = list(set(analysed) - set(genefound))
    for number in nogene:
        with open(notfound, 'a') as nf:
            nf.write(f'{number}    No matching gene found in gb file\n')

    return analysed, genefound
            


def genbankfields(text, genelist):
    ###extract the CDS for each asscession version number
    dictfield = {}
    listofdict = []
    dna = []
    ##ACCESSION VERSION NUMBER
    try:
        version = text.split('VERSION', 1)[1]
        version = version.split('\n', 1)[0]
        version = version.split()[0]
        version = version.strip()
        dictfield["version"] = version
    except IndexError:
        return listofdict, dna

    ##ORGANISM And TAXO
    try:
        taxo = text.split('ORGANISM', 1)[1]
        taxo = taxo.split('REFERENCE')[0]
        organism = taxo.splitlines()[0].strip()
        taxo = ''.join(taxo.splitlines()[1:]).split("; ")
        taxo = [t.strip() for t in taxo]
    except IndexError:
        taxo, organism = "not found", "not found"
    dictfield["taxo"] = taxo
    dictfield["organism"] = organism    

    ###Definition line (to use if information option is not selected)
    try:
        definition = text.split('DEFINITION', 1)[1]
        definition = definition.split('ACCESSION', 1)[0]
    except IndexError:
        definition = "not found"
    dictfield["definition"] = "".join(definition.split("\n"))

    ###DNA sequence
    try:
        dna = text.split("ORIGIN")[1].splitlines()
        dna = [d.strip().strip('1234567890') for d in dna]
        dna = "".join("".join(dna).split())
    except IndexError:
        dna = []
    dictfield["dna"] = dna

    ###look for all the CDS, their gene names or product names (== protein) and locations and sequences
    ##and protein_id, frame
    seqgene = text.split("  gene  ")
    for seq in seqgene:
        dictgene = {}
        dictgene = search(dna, dictgene, seq)
        seqcds = seq.split("  CDS  ")[1:]
        for seq1 in seqcds:
            dictcds = search(dna, dictfield, seq1)
            if genelist:
                ##check if target is found
                check = [1 for reg in genelist if re.findall(reg, dictcds["product"], flags=re.IGNORECASE) or re.findall(reg, dictcds["gene"], flags=re.IGNORECASE)\
                or re.findall(reg, dictcds["note"], flags=re.IGNORECASE) or re.findall(reg, dictcds["genesynonym"], flags=re.IGNORECASE)]
                try:
                    if not check:
                        if dictgene["location"][0][0] ==  dictcds["location"][0][0] and dictgene["location"][-1][1] ==  dictcds["location"][-1][1]:
                            check = [1 for reg in genelist if re.findall(reg, dictgene["product"], flags=re.IGNORECASE) or re.findall(reg, dictgene["gene"], flags=re.IGNORECASE)\
                            or re.findall(reg, dictgene["note"], flags=re.IGNORECASE) or re.findall(reg, dictgene["genesynonym"], flags=re.IGNORECASE)]
                except IndexError:
                    pass
                if check:
                    listofdict.append(dictcds)
            else:
                listofdict.append(dictcds)
        
    if listofdict:
        return listofdict, dna 
    else:
        listofdict.append(dictfield)
        return listofdict, dna
    

def search(dna ,dictentry, s):
    dict1 = dict(dictentry)
    s = s.split("RNA   ")[0].split("  misc_feature  ")[0].split("  gene  ")[0].split("repeat_region")[0]\
        .split("transit_peptide")[0].split("mat_peptide")[0].split("3'UTR")[0].split("5'UTR")[0]
    #Location and sequence
    if dna:
    ##if join or complement:
        try:
            loc = s.split("/")[0]
            loc1 = loc.split(',')
            loc1 = [(int(i.split('..')[0].strip("cmpletjoin(><) \n")), int(i.split('..')[1].strip("cmpletjoin(><) \n"))) for i in loc1]
            sequence = "".join([dna[i[0]:i[1]] for i in loc1])
        #else
        except IndexError:
            sequence = ""
            loc = "not found"
            loc1 = "not found"
        except ValueError:
            sequence = ""
            loc = "not found"
            loc1 = "not found"
    else:
        sequence = ""
        loc = "not found"
        loc1 = "not found"
    dict1["sequence"] = sequence
    dict1["location"] = loc1
    dict1["loc"] = "".join(loc.split("\n"))

    
    #Product
    try:
        product = s.split('product="')[1].split('"')[0]
    except IndexError:
        product = "not found"
    dict1["product"] = product

    #protein_id
    try: 
        proteinid = s.split("protein_id=")[1].split()[0]
    except IndexError:
        proteinid = "not found"
    dict1["proteinid"] = proteinid

    #note
    try:
        note = s.split("note=")[1].split("/")[0]
        note = "".join(note.split("\n"))
    except IndexError:
        note = ""
    dict1["note"] = note

    #gene
    try:
        gene = s.split("gene=")[1].split("\n")[0]
    except IndexError:
        gene = "not found"
    dict1["gene"] = gene

    #gene_synonym
    try:
        genesynonym = s.split("gene_synonym=")[1].split("/")[0].strip("\n")
    except IndexError:
        genesynonym = "not found"
    dict1["genesynonym"] = genesynonym

    #locus_tag
    try:
        locustag = s.split("locus_tag=")[1].split()[0]
    except IndexError:
        locustag = "not found"
    dict1["locustag"] = locustag

    return dict1



def tsv_file_writer(path, data, OPTIONS=None):

    if OPTIONS is None:
        OPTIONS = ("","","","","","")

    (_, _, _, _, _, information) = OPTIONS   

        
    # check if the file already exists
    if not os.path.exists(path):
        with open(path, "a") as tsv_to_write:
            writer = csv.writer(tsv_to_write, delimiter="\t")
            if information:
                writer.writerow(['Name', 'SeqID', 'TaxID', 'Lineage', 'sequence length', 'sequence'])
            else:
                writer.writerow(['SeqID', 'TaxID', 'sequence length', 'sequence'])

    
    # unpack data
    (name, seqid, taxid, lineage, dna) = data

    dna = "".join(dna.split("\n"))

    # write data
    with open(path, "a") as outtsv:
        writer = csv.writer(outtsv, delimiter='\t')
        if information:
            writer.writerow([name, seqid, taxid, lineage, len(dna), dna])
        else:
            writer.writerow([seqid, taxid, len(dna), dna])

    return
