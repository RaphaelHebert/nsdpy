# import from standard library
import os
import re
import csv
from collections import Counter

# third party imports
import requests  # https://requests.readthedocs.io/en/master/

# local imports
from constants import (
    ESEARCH_URL,
    ESUMMARY_URL,
    EFETCH_URL,
    PLANTAE,
    METAZOA,
    FUNGI,
    BASE_PARAMETERS,
    EMAIL,
    TOOL,
    NCBI_URL,
)


def countDown(iteration, total, message=""):
    """
    Take the number of iteration, the range of a forloop and a message and output a message with the percent of job done

    INPUTS: countDown(iteration, total, message='')
    iteration:  positive INT
    total: positive INT
    message: STRING

    OUTPUT: STRING

    """

    if message:
        message = message + ": "

    if iteration < 0:
        raise ValueError("iteration must be a positive integer")

    if total < 0:
        raise ValueError("total must be a positive integer")

    if total < 1:
        return f"{message}no job to be done"

    iteration = iteration + 1
    left = round((iteration / total) * 100, 1)
    if left > 100:
        left = 100
    return f"{message}{left}%"


def download(parameters, address):
    """
    Sends requests to the API until getting a result

    INPUTS: download(parameters, address)
        parameters: DICT, parameters of the get request to the API
        Address: STRING, API base URL

    OUTPUT: object, <class 'requests.models.Response'>
        if an exceptions.HTTPError is triggered: returns 1
    """
    connect = 0
    parameters = {**BASE_PARAMETERS, **parameters}

    while True:
        try:
            result = requests.get(address, params=parameters, timeout=60)
            break
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            return 1

        except requests.exceptions.Timeout as to:
            print(f"Connection Timed out\n{to}")
            continue

        except requests.exceptions.ConnectionError as _:
            if connect == 1:
                continue
            elif connect == 0:
                connect = 1
                print(f"Connection error (please reconnect)\n ")
                continue

        except requests.exceptions.RequestException as e:
            print(f"An exception occurred:\n{e}")
            continue

    return result


def esearchquery(QUERY):
    """

    Sends a query to ncbi esearch engine

    INPUTS: esearchquery(QUERY)
        query: (TUPLE) (query: STRING, apikey: STRING)

    OUTPUTS: dict
        the result of the submitted query

    """

    ## unpack QUERY:
    (query, api_key) = QUERY

    # parameters
    parameters = {
        **BASE_PARAMETERS,
        **({"api_key": str(api_key)} if api_key else {}),
        "db": "nucleotide",
        "idtype": "acc",
        "retmode": "json",
        "retmax": "0",
        "usehistory": "y",
        "term": query,
    }

    ### send request to the API
    y = download(parameters, ESEARCH_URL)
    if y == 1:
        return {"error": "wrong address for esearch"}
    return y.json()


def taxids(params, path, QUERY, OPTIONS=None):
    """
    sends queries by batches to esummary E-utility
    parse the response to map taxids to accession numbers
    if -T writes a textfile

    INPUTS: taxids(params, path, OPTIONS)
        params: (TUPLE) (querykey, webenv, count)
        path: (STRING) output folder path
        query: (TUPLE) (query: STRING, apikey: STRING)
        OPTIONS: (TUPLE) (verb, _, _, args.taxids, _, _)

    OUTPUTS: dict { accession_number: TaxIDs }
        if -T textfile

    """
    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    ## unpack QUERY:
    (_, api_key) = QUERY

    ## unpack parameters
    (querykey, webenv, count) = params
    (verb, _, _, fileoutput, _, _) = OPTIONS

    dict_ids = {}
    taxid = ""
    seqnb = ""

    ## retreive the taxids sending batches of accession numbers to esummary
    retmax = 100
    if count < retmax:
        retmax = count

    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    x = 0
    while x < nb:
        # parameters
        parameters = {
            **({"api_key": str(api_key)} if api_key else {}),
            "db": "taxonomy",
            "query_key": querykey,
            "WebEnv": webenv,
            "retstart": str(x * retmax),
            "retmax": str(retmax),
            "rettype": "uilist",
            "retmode": "text",
        }
        result = download(parameters, ESUMMARY_URL)

        # comments
        if verb and verb > 1:
            print(countDown(x, nb, "Downloading TaxIDs"))

        ### extract the TaxIDs and accession numbers (record in text file and in dict_ids)
        f = result.text.splitlines()
        for line in f:
            if len(line.split("<DocSum>")) > 1:
                taxid = ""
                seqnb = ""
            else:
                try:
                    version = line.split(
                        '<Item Name="AccessionVersion" Type="String">', 1
                    )[1]
                    """
                        AccessionVersion is made of accession number plus versions number.
                        Accession numbers pattern: [alphabetical prefix][series of digits]
                        see: https://www.ncbi.nlm.nih.gov/books/NBK470040/#:~:text=The%20accession%20number%20is%20a,the%20accession%20munumber%2C%20an%20Accession.
                    """
                    seqnb = version.split("<")[0].strip()
                except IndexError:
                    pass

                TaxId = line.split('<Item Name="TaxId" Type="Integer">', 1)
                if len(TaxId) > 1:
                    taxid = TaxId[1].split("<")[0].strip()

                if seqnb:
                    dict_ids[seqnb] = taxid

        if count - (retmax * x) > 100:
            if len(dict_ids.keys()) != (retmax * (x + 1)):
                x -= 1
        else:
            if len(dict_ids.keys()) != count:
                x -= 1
        x += 1

    if fileoutput:
        ## filename
        filename = "TaxIDs.txt"
        ## path to filename
        path = path + "/" + filename
        with open(path, "a") as summary:
            [summary.write(f"{key}  {value}\n") for key, value in dict_ids.items()]

    return dict_ids


def dispatch(lineage, classif):
    """
    take the lineage of a sequence and the classification option and return the base name of the file to store
    the sequence.

    INPUTS: dispatch(lineage, classif)
        lineage: LIST
        classif: INT or LIST

    OUTPUTS:
        (STRING) rank

    """

    ##no option selected
    if classif == 2:
        return "sequences"

    ## user gave list of taxonomic levels (option -l --levels)
    if isinstance(classif, str):
        ## type checking
        if not isinstance(lineage, dict):
            return "OTHERS"

    ## user gave list of taxonomic levels (option -l --levels)
    if isinstance(classif, list):
        try:
            other = [rank for rank in lineage if rank in classif][0]
        except IndexError:
            other = "OTHERS"
        return other
    ##phylums
    if classif == 0:
        try:
            Phylum = [
                phy
                for phy in lineage
                if phy in METAZOA or phy in FUNGI or phy in PLANTAE
            ][0]
        except IndexError:
            Phylum = "OTHERS"
        return Phylum
    ##kingdoms
    if classif == 1:
        if "METAZOA" in lineage or len(list(set(lineage) & set(METAZOA))) > 0:
            kingdom = "METAZOA"
        elif "ViridiPLANTAE" in lineage or len(list(set(lineage) & set(PLANTAE))) > 0:
            kingdom = "PLANTAE"
        elif "FUNGI" in lineage or len(list(set(lineage) & set(FUNGI))) > 0:
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


# query taxonomy with efetch, returns a dict with taxid as key and info in a dict as value
def completetaxo(idlist, QUERY, OPTIONS):
    """
    Query efetch with the given list of taxIds

    INPUTS: completetaxo(list_of_TaxIDs, QUERY, OPTIONS)
        list_of_TaxIDs: (LIST) [STRING,]
        QUERY: (TUPLE) (_, api_key)
        OPTIONS: (TUPLE) (verb, _, classif, _, _, _)

    OUTPUTS: (DICT) { tadId: dicttemp }
        taxId: (STRING) taxId
        dicttemp: (DICT) { Name: (STRING), Lineage: (STRING), dispatch: (STRING) }

    """

    ## unpack parameters
    (_, api_key) = QUERY
    (verb, _, classif, _, _, _) = OPTIONS

    if verb and verb > 0:
        print("retrieving taxonomy...")

    ## dictionnary that will be returned
    data = {}
    idlist = [i.split(".")[0] for i in idlist]
    ## retreive the taxonomy sending batches of TaxIds to efetch
    # number of TaxIds to be sent to the API at once
    # above 60 make the parsing of the file more difficult see https://github.com/RaphaelHebert/nsdpy/pull/39
    retmax = 50

    count = len(idlist)
    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    for x in range(nb):
        ## slice the idlist
        retstart = x * retmax
        idsublist = idlist[retstart : (retstart + retmax)]
        idsublist = ",".join(idsublist)
        # parameters
        parameters = {
            "db": "taxonomy",
            "id": idsublist,
            **({"api_key": api_key} if api_key else {}),
        }

        ## oop until download is correct
        result = download(parameters, EFETCH_URL)

        # comments
        if verb > 1:
            print(f"{round((int(retstart)/count)*100, 1)} % of the taxonomy found")

        ## analyse the results from efetch
        result = result.text.split("</Taxon>\n<Taxon>")
        for seq in result:
            dicttemp = {}
            try:
                TaxId, _ = seq.split("</TaxId>", 1)
                _, TaxId = TaxId.split("<TaxId>", 1)
                TaxId = TaxId.strip()
            except ValueError:
                TaxId = "not found"

            # check if the taxonomy for a given TaxId is already in memory
            if TaxId in data.keys():
                continue

            try:
                Name, _ = seq.split("</ScientificName>", 1)
                _, Name = Name.split("<ScientificName>", 1)
            except ValueError:
                Name = "not found"
            dicttemp["Name"] = Name

            try:
                Lineage, _ = seq.split("</Lineage>", 1)
                _, Lineage = Lineage.split("<Lineage>", 1)
            except ValueError:
                Lineage = "not found"
            lineage = Lineage.split("; ")
            dicttemp["Lineage"] = lineage

            ## dispatch
            if isinstance(classif, str):
                lineage = parseClassifXML(seq)
                if classif in lineage.keys():
                    dicttemp["dispatch"] = lineage[classif].replace(" ", "_")
                else:
                    dicttemp["dispatch"] = "OTHERS"
            else:
                dicttemp["dispatch"] = dispatch(lineage, classif)

            data[TaxId] = dicttemp
    # comments
    if verb and verb > 0:
        print(f"number of taxids:\t{len(data.keys())}")

    return data


def cds_fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None):
    """

    Query eftch with batches of ids
    Parse the result to find match for gene in genelist

    a list of the accession numbers for which a gene (from genelist) have been found (LIST)
    INPUTS:
        path: (STRING) output_path
        dict_ids: (DICT) { accession_number: TaxId }
        dict_taxo: (DICT) { tadId: dicttemp }
        QUERY: (TUPLE) (_, api_key)
        list_of_ids: (LIST) [accession_version_numbers]
        OPTION: (TUPLE) (verb: (STRING), args.cds (LIST), classif (INT, or LIST), _, _, args.information (BOOL))

    OUTPUTS: (LIST) [accession_number] matches genelist/results

    """

    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    ## Unpack parameters
    (_, api_key) = QUERY
    (verb, genelist, classif, _, _, information) = OPTIONS

    # Comment:
    if verb and verb > 0:
        print("Downloading the CDS fasta files...")

    # List of accession number for wich a gene is found or the file has been retrieve if no gene filter:
    found = []
    count = len(list_of_ids)

    # Number of accession numbers to be sent at each API query
    retmax = 200
    if count < retmax:
        retmax = count

    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    for x in range(nb):
        ## Split the list of ids
        ids = list_of_ids[x * retmax : (x * retmax) + retmax]
        ## Check that id parameters is not empty
        ids = [i for i in ids if i]
        # Parameters
        parameters = {
            "id": ",".join(ids),
            "db": "nuccore",
            **({"api_key": api_key} if api_key else {}),
            "rettype": "fasta_cds_na",
            "retmode": "text",
        }
        ## Download
        raw_result = download(parameters, EFETCH_URL)
        raw_result = raw_result.text

        ## Extract available information
        if not information and not genelist and classif == 3:
            result_fasta = raw_result.split(">lcl|")[1:]
            sublist = [r.split("_cds")[0] for r in result_fasta]

        ## analyse the results
        sublist = extract(
            path, raw_result, dict_ids, dict_taxo, genelist, OPTIONS, verb
        )
        found = found + sublist

        # comments
        if verb > 1:
            print(countDown(x, nb, "Downloading the cds_fasta files"))

    return found


def subextract(seq, path, dict_ids, dict_taxo, genelist, OPTIONS=None):
    """
    INPUTS:
        seq: (STRING) the gene sequence with its information line
        path: (STRING) output_path
        dict_ids: (DICT) { accession_number: TaxId }
        dict_taxo: (DICT) { tadId: dicttemp }
        genelist: (LIST) args.cds

    OUTPUTS:
        (LIST) [accession_version_number]

    """

    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    (_, _, classif, _, tsv, information) = OPTIONS

    ### find gene in a seq and write to ouput file
    ## extract accession number
    try:
        key = seq.split(">lcl|")[1].split("_cds")[0]
    except IndexError:
        return

    ## extract SeqID
    try:
        SeqID = seq.split(">lcl|")[1].split(" [")[0]
    except IndexError:
        return

    ## build id_line (retrieve info)
    try:
        TaxId = dict_ids[key]
    except KeyError:
        return

    ## Extract info
    # Lineage
    try:
        Lineage = dict_taxo[TaxId]["Lineage"]
    except KeyError:
        Lineage = "no info"

    # Name
    try:
        Name = dict_taxo[TaxId]["Name"]
    except KeyError:
        Name = "no info"

    # dispatch
    try:
        dispatch = dict_taxo[TaxId]["dispatch"]
    except KeyError:
        dispatch = "others"
    if classif == 2:
        dispatch = "sequences"

    ## check if genes
    check = [
        1
        for reg_exp in genelist
        if len(re.split(reg_exp, seq, flags=re.IGNORECASE)) > 1
    ]
    if 1 in check or not genelist:
        ## get the Sequence
        _, dna = seq.split("\n", 1)

        # if dict_taxo and information:
        if information:
            Lineage = ", ".join(Lineage)
            fasta_Name = "_".join(Name.split())
            info_line = fasta_Name + "-" + SeqID + " | " + TaxId + " | " + Lineage
        else:
            info_line = seq.split("\n", 1)[0]

        # Make only one > and \n
        info_line = ">" + info_line.lstrip(">")
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
        with open(fasta_file, "a") as new:
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
    """

    Iterates over lines of text to parse sequences
    Send sequences and infos to subextract and add to result if subextract returms a result

    INPUTS:
        path: (STRING) output_path
        dict_ids: (DICT) { accession_number: TaxId }
        dict_taxo: (DICT) { tadId: dicttemp }
        genelist: (LIST) args.cds
        OPTIONS: (TUPLE) (verb, args.cds, classif, args.taxids, args.tsv, args.information) optionnal

    OUTPUTS:
        (LIST) [accession_version_number]

    """

    # Comments
    if verb and verb > 1:
        print("analyzing the results...")

    found = []

    # Extract genes to filter
    genelist = ["=" + gene + "]" for gene in genelist]

    seq = ""
    text = text.splitlines()

    if not text:
        return found

    for line in text:
        if len(line.split(">lcl|")) > 1:
            if seq:
                try:
                    result = subextract(
                        seq, path, dict_ids, dict_taxo, genelist, OPTIONS
                    )
                    if result:
                        found.append(result)
                except:
                    pass
            seq = str(line)
        else:
            seq = seq + "\n" + line

    return found


def fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS=None):
    """
    Retrieves fasta files from nuccore db calls and parse it to find DNA sequence and info for the information line of the created fasta file

    INPUTS
        path: (STRING) output_path
        dict_ids: (DICT) { accession_number: TaxId }
        dict_taxo: (DICT) { tadId: dicttemp }
        QUERY: (TUPLE) (query: STRING, apikey: STRING)
        list_of_ids: (LIST) [accession_version_numbers]
        OPTIONS: (TUPLE) (verb, args.cds, classif, args.taxids, args.tsv, args.information) optionnal

    OUTPUTS:
        (LIST) [ matching_accession_number ]
            if selected tsv fils and/or info

    """

    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    ## Unpack parameters
    (_, api_key) = QUERY
    (verb, _, classif, _, tsv, information) = OPTIONS

    if verb and verb > 0:
        print("Downloading the fasta files...")

    keys = []
    count = len(list_of_ids)

    # Number of accession numbers to be sent at each API query
    retmax = 200
    if count < retmax:
        retmax = count

    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    for x in range(nb):
        ## Split the list of ids
        ids = list_of_ids[x * retmax : (x * retmax) + retmax]
        ## Check that id parameters is not empty
        ids = [i for i in ids if i]
        # Parameters
        parameters = {
            "db": "nuccore",
            "id": ",".join(ids),
            "rettype": "fasta",
            "retmode": "text",
            "api_key": api_key if api_key else None,
        }

        ## Download
        raw_result = download(parameters, EFETCH_URL)
        raw_result = raw_result.text

        ## Extract available informations
        result = raw_result.split(">")

        ## Store analyzed Accession version numbers
        for seq in result:
            try:
                id_line, dna = seq.split("\n", 1)
            except ValueError:
                continue

            try:
                key = id_line.split()[0]
            except IndexError:
                continue

            # from dict_ids
            try:
                taxid = dict_ids[key]
            except KeyError:
                taxid = "not found"

            # from dict_taxo
            try:
                lineage = dict_taxo[taxid]["Lineage"]
                lineage = ", ".join(lineage)
            except KeyError:
                lineage = "not found"

            try:
                name = dict_taxo[taxid]["Name"]
            except KeyError:
                name = "not found"

            try:
                dispatch = dict_taxo[taxid]["dispatch"]
            except KeyError:
                dispatch = "OTHERS"

            if classif == 2:
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
                fasta_name = "_".join(name.split())
                id_line = (
                    fasta_name
                    + "-"
                    + key
                    + " | "
                    + taxid
                    + " | "
                    + lineage
                    + " | "
                    + id_line
                )
            with open(fasta_file, "a") as f:
                f.write(f">{id_line}\n")
                f.write(f"{dna}\n")

            if tsv:
                tsv_file_writer(tsv_file, data, OPTIONS)

            keys.append(key)

        if verb and verb > 1:
            print(countDown(x, nb, "Downloading the fasta files"))
    return keys


def duplicates(listofaccess, path):
    """

    Finds the number of value in a list that has more than one occurence

    INPUTS:
        listofaccess: (LIST) [ STRING, ]
        path: (STRING) path to write the textfile output

    OUTPUTS:
        (NUMBER) number of duplicate
        () textfile with the values and their number of occurences in the list

    """

    filename = path + "/duplicates.txt"
    count = Counter(listofaccess)
    count = dict(count)
    nb = 0
    for key, value in count.items():
        if value > 1:
            nb += 1
            with open(filename, "a") as f:
                f.write(f"{key}   {value}\n")
    return nb


def taxo(path, list_of_ids, dict_ids, QUERY, dict_taxo=None, OPTIONS=None):
    """

    Finds the number of value in a list that has more than one occurence

    INPUTS:
        path: (STRING) output_path
        list_of_ids: (LIST) [ STRING ]
        dict_ids: (DICT) { accession_number: TaxId }
        QUERY: (TUPLE) (query: STRING, apikey: STRING)
        dict_taxo: (DICT) { tadId: dicttemp }
        OPTIONS: (TUPLE) (verb, args.cds, classif, args.taxids, args.tsv, args.information) optionnal

    OUTPUTS:
        analysed: (LIST) [accession_number] accession number found in the gb file
        genefound: (LIST) [accession_number] accession number with matching cds of filter

    """

    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    if len(list_of_ids) < 1:
        return ([], [])

    ## unpack params
    (verb, genelist, classif, _, tsv, information) = OPTIONS
    (_, api_key) = QUERY

    ## build output unique filename
    notfound = path + "/notfound.txt"

    # format the expression to be found in 'gene' (from gene and CDS section of the gb file)
    if genelist:
        genelist = ['[; "()]+' + gene + '["; ()]+' for gene in genelist]

    # comments
    if verb and verb > 0:
        print("Downloading the GenBank files...")

    remain = []  # accessions not downloaded from previous iteration
    analysed = []  # accessions successfully donwnloaded and found in the gb file
    genefound = (
        []
    )  ## accessions with some cds found or matching the filter if filter(s)
    count = len(list_of_ids)
    retmax = 10
    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    for x in range(nb):
        ###################  API CALL  ##################
        ## slice the list of ids passed to the function
        ids = list_of_ids[x * retmax : (x + 1) * retmax]
        ## if some ids haven't been dl at the last call add them to this call
        if remain:
            ids = ids + remain
        ids1 = ",".join(ids)
        retstart = str(x * retmax)

        # parameters
        parameters = {
            "db": "nuccore",
            "id": ids1,
            "rettype": "gb",
            "retmode": "text",
            **({"api_key": api_key} if api_key else {}),
        }

        ## loop until dl is correct
        result = download(parameters, EFETCH_URL)
        result = result.text

        ########################################################################
        #######################   ANALYZING RESULTS   ##########################
        ########################################################################

        result = result.split("\n//")
        ### extract the CDS for each asscession version number
        accessionlist = []
        for i, seq in enumerate(result[:-1]):
            ## search in CDS
            listCDS, dna = genbankfields(seq, genelist)

            for dictCDS in listCDS:
                if dictCDS:
                    accessionlist.append(dictCDS["version"])
                    # select the gene if genes to select
                    if "gene" in dictCDS.keys():
                        ##genefound
                        genefound.append(dictCDS["version"])
                        ### path
                        taxo = dictCDS["taxo"]
                        filename = dispatch(taxo, classif)
                        if tsv:
                            fasta_file = path + "/fasta/" + filename + ".fasta"
                        else:
                            fasta_file = path + "/" + filename + ".fasta"

                        ## information line
                        taxo = ", ".join(taxo)

                        try:
                            taxid = dict_ids[dictCDS["version"]]
                        except IndexError:
                            taxid = ""

                        if information:
                            try:
                                name = dict_taxo[taxid]["Name"]
                                name = "_".join(name.split())
                            except:
                                name = "not found"
                            info_line = (
                                ">"
                                + name
                                + "-"
                                + dictCDS["version"]
                                + "_cds_"
                                + dictCDS["proteinid"].strip('"')
                                + " | "
                                + taxid
                                + " | "
                                + "".join(taxo).rstrip(".")
                            )

                        else:
                            info_line = (
                                ">"
                                + dictCDS["version"]
                                + "_cds_"
                                + dictCDS["proteinid"].strip('"')
                                + " [gene="
                                + dictCDS["gene"]
                                + "] "
                                + "[protein="
                                + dictCDS["proteinid"]
                                + "] "
                                + "[location="
                                + dictCDS["loc"].strip()
                                + "] "
                                + "[gbkey=CDS] "
                                + "[definition="
                                + " ".join(
                                    dictCDS["definition"].split(" " * 12)
                                ).rstrip(".")
                                + "]"
                            )

                        ## append to file
                        with open(fasta_file, "a") as a:
                            a.write(f"{info_line}\n")
                            [
                                a.write(
                                    f'{"".join(list(dictCDS["sequence"])[i: i + 70]).upper()}\n'
                                )
                                for i in range(0, len(dictCDS["sequence"]), 70)
                            ]

        remain = list(set(accessionlist) - set(ids))
        analysed = analysed + accessionlist

        # comments
        if verb > 1:
            print(
                f"{round(((int(retstart))/count)*100, 1)} %  of the remaining  analysis done"
            )

    if remain:
        for number in remain:
            with open(notfound, "a") as nf:
                nf.write(f"{number}    Accession number not found in gb files\n")

    # accessions found in bg file wihtout matching gene
    nogene = list(set(analysed) - set(genefound))
    for number in nogene:
        with open(notfound, "a") as nf:
            nf.write(f"{number}    No matching gene found in gb file\n")

    return analysed, genefound


def genbankfields(text, genelist):
    ### extract the CDS for each asscession version number
    dictfield = {}
    listofdict = []
    dna = []
    ## ACCESSION VERSION NUMBER
    try:
        version = text.split("VERSION", 1)[1]
        version = version.split("\n", 1)[0]
        version = version.split()[0]
        version = version.strip()
        dictfield["version"] = version
    except IndexError:
        return listofdict, dna

    ## ORGANISM And TAXO
    try:
        taxo = text.split("ORGANISM", 1)[1]
        taxo = taxo.split("REFERENCE")[0]
        organism = taxo.splitlines()[0].strip()
        taxo = "".join(taxo.splitlines()[1:]).split("; ")
        taxo = [t.strip() for t in taxo]
    except IndexError:
        taxo, organism = "not found", "not found"
    dictfield["taxo"] = taxo
    dictfield["organism"] = organism

    ### Definition line (to use if information option is not selected)
    try:
        definition = text.split("DEFINITION", 1)[1]
        definition = definition.split("ACCESSION", 1)[0]
    except IndexError:
        definition = "not found"
    dictfield["definition"] = "".join(definition.split("\n"))

    ### DNA sequence
    try:
        dna = text.split("ORIGIN")[1].splitlines()
        dna = [d.strip().strip("1234567890") for d in dna]
        dna = "".join("".join(dna).split())
    except IndexError:
        dna = []
    dictfield["dna"] = dna

    ### look for all the CDS, their gene names or product names (== protein) and locations and sequences
    ## and protein_id, frame
    seqgene = text.split("  gene  ")
    for seq in seqgene:
        dictgene = {}
        dictgene = search(dna, dictgene, seq)
        seqcds = seq.split("  CDS  ")[1:]
        for seq1 in seqcds:
            dictcds = search(dna, dictfield, seq1)
            if genelist:
                ## check if target is found
                check = [
                    1
                    for reg in genelist
                    if re.findall(reg, dictcds["product"], flags=re.IGNORECASE)
                    or re.findall(reg, dictcds["gene"], flags=re.IGNORECASE)
                    or re.findall(reg, dictcds["note"], flags=re.IGNORECASE)
                    or re.findall(reg, dictcds["genesynonym"], flags=re.IGNORECASE)
                ]
                try:
                    if not check:
                        if (
                            dictgene["location"][0][0] == dictcds["location"][0][0]
                            and dictgene["location"][-1][1]
                            == dictcds["location"][-1][1]
                        ):
                            check = [
                                1
                                for reg in genelist
                                if re.findall(
                                    reg, dictgene["product"], flags=re.IGNORECASE
                                )
                                or re.findall(
                                    reg, dictgene["gene"], flags=re.IGNORECASE
                                )
                                or re.findall(
                                    reg, dictgene["note"], flags=re.IGNORECASE
                                )
                                or re.findall(
                                    reg, dictgene["genesynonym"], flags=re.IGNORECASE
                                )
                            ]
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


def search(dna, dictentry, s):
    """

    Search for

    INPUTS:
        dna: (LIST) [STRING]
        dictentry: (DICT) { informations_field: extracted_value }
        s: (STRING)

    OUTPUTS:
        (DICT) {
                "sequence",
                "location",
                "loc",
                "product",
                "proteinid",
                "note",
                "genesynonym",
                "gene",
                "locustag"
            }

    """
    dict1 = dict(dictentry)
    s = (
        s.split("RNA   ")[0]
        .split("  misc_feature  ")[0]
        .split("  gene  ")[0]
        .split("repeat_region")[0]
        .split("transit_peptide")[0]
        .split("mat_peptide")[0]
        .split("3'UTR")[0]
        .split("5'UTR")[0]
    )
    # Location and sequence
    if dna:
        ## if join or complement:
        try:
            loc = s.split("/")[0]
            loc1 = loc.split(",")
            loc1 = [
                (
                    int(i.split("..")[0].strip("cmpletjoin(><) \n")),
                    int(i.split("..")[1].strip("cmpletjoin(><) \n")),
                )
                for i in loc1
            ]
            sequence = "".join([dna[i[0] : i[1]] for i in loc1])
        # else
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

    # Product
    try:
        product = s.split('product="')[1].split('"')[0]
    except IndexError:
        product = "not found"
    dict1["product"] = product

    # protein_id
    try:
        proteinid = s.split("protein_id=")[1].split()[0]
    except IndexError:
        proteinid = "not found"
    dict1["proteinid"] = proteinid

    # note
    try:
        note = s.split("note=")[1].split("/")[0]
        note = "".join(note.split("\n"))
    except IndexError:
        note = ""
    dict1["note"] = note

    # gene
    try:
        gene = s.split("gene=")[1].split("\n")[0]
    except IndexError:
        gene = "not found"
    dict1["gene"] = gene

    # gene_synonym
    try:
        genesynonym = s.split("gene_synonym=")[1].split("/")[0].strip("\n")
    except IndexError:
        genesynonym = "not found"
    dict1["genesynonym"] = genesynonym

    # locus_tag
    try:
        locustag = s.split("locus_tag=")[1].split()[0]
    except IndexError:
        locustag = "not found"
    dict1["locustag"] = locustag

    return dict1


def tsv_file_writer(path, data, OPTIONS=None):
    """

    Writes a tsv file with the given data

    INPUTS:
        path: (STRING) output_path
        data: (TUPLE) (name (STRING), seqid (STRING), taxid (STRING), lineage (STRING), dna (STRING))
        OPTIONS: (TUPLE) (verb, args.cds, classif, args.taxids, args.tsv, args.information) optionnal

    OUTPUTS:
        (VOID) path.tsv

    """

    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    (_, _, _, _, _, information) = OPTIONS

    # check if the file already exists
    if not os.path.exists(path):
        with open(path, "a") as tsv_to_write:
            writer = csv.writer(tsv_to_write, delimiter="\t")
            if information:
                writer.writerow(
                    ["Name", "SeqID", "TaxID", "Lineage", "sequence length", "sequence"]
                )
            else:
                writer.writerow(["SeqID", "TaxID", "sequence length", "sequence"])

    # unpack data
    (name, seqid, taxid, lineage, dna) = data

    dna = "".join(dna.split("\n"))

    # write data
    with open(path, "a") as outtsv:
        writer = csv.writer(outtsv, delimiter="\t")
        if information:
            writer.writerow([name, seqid, taxid, lineage, len(dna), dna])
        else:
            writer.writerow([seqid, taxid, len(dna), dna])

    return


def parseClassifXML(xml):
    """
    takes a string and parse it as xml format to extract the available taxonomy


    INPUTS: parseClassifXML(xml)
        xml: string
    OUTPUTS:
        classif: dict
    """

    classif = {}

    # parse the name before lineageex as well
    general_infos = ""
    lineage_info = ""
    taxon = []

    if "</ScientificName>" in xml and "<ScientificName>" in xml:
        scientificName, _ = xml.split("</ScientificName>", 1)
        _, scientificName = scientificName.split("<ScientificName>", 1)
        classif["ScientificName"] = scientificName

    if "</LineageEx>" in xml and "<LineageEx>" in xml:
        lineage_info, general_infos = xml.split("</LineageEx>", 1)
        general_infos, lineage_info = lineage_info.split("<LineageEx>", 1)

    if (
        "</Rank>" in general_infos
        and "<Rank>" in general_infos
        and "ScientificName" in classif
    ):
        taxon_info = general_infos.split("</Rank>", 1)[0].split("<Rank>", 1)[1]
        classif[taxon_info] = classif["ScientificName"]

    taxons = lineage_info.split("</Taxon>")
    for taxon in taxons:
        keys = classif.keys()
        if (
            "</ScientificName>" in taxon
            and "<ScientificName>" in taxon
            and "<Rank>" in taxon
            and "</Rank>" in taxon
        ):
            name, _ = taxon.split("</ScientificName>", 1)
            _, name = name.split("<ScientificName>", 1)
            name = re.sub(r"\s+", "_", name)
            rank, _ = taxon.split("</Rank>", 1)
            _, rank = rank.split("<Rank>", 1)
            rank = re.sub(r"\s+", "_", rank)
            if rank == "clade":
                if rank not in keys:
                    classif["clade"] = [name]
                else:
                    classif["clade"].append(name)
            else:
                classif[rank] = name

    return classif


def download_gff3(list_of_ids, path, OPTIONS, write_file=True):
    """

    Retrieve gff3 files and optionnaly write the result in a file

    INPUTS:
        ids: (LIST) [id] accession sequence id
        path: (STRING)
        write_file: (BOOL)

    OUTPUTS:
        (DICT) {ok: (BOOL),
                text: (STRING),
                url: (STRING)
                }   result from request.get call

    """
    if OPTIONS is None:
        OPTIONS = ("", "", "", "", "", "")

    ## Unpack parameters
    (verb, _, _, _, _, _) = OPTIONS

    count = len(list_of_ids)
    retmax = 200

    if count < retmax:
        retmax = count

    if count % retmax == 0:
        nb = count // retmax
    else:
        nb = (count // retmax) + 1

    for x in range(nb):
        ids = list_of_ids[x * retmax : (x * retmax) + retmax]
        ## Check that id parameters is not empty
        ids = [i for i in ids if i]

        parameters = {
            "db": "nuccore",
            "report": "gff3",
            "id": ",".join(ids),
            "email": EMAIL,
            "tool": TOOL,
        }

        gff3_result = requests.get(NCBI_URL, params=parameters, timeout=60)

        gff3_file = path + "/results.gff3"

        if not gff3_result.ok:
            return
        # write gff3 files in result folder
        if write_file:
            with open(gff3_file, "a") as f:
                f.write(gff3_result.text)

        if verb and verb > 1:
            print(countDown(x, nb, "Downloading the gff3 files"))

    return gff3_result


if __name__ == "_main_":
    countDown()
    download()
    dispatch()
