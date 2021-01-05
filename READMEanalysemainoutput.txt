analysemainoutput.py

    INPUTS:
        -no inputs as command line arguments
        -the script prompte the user for filenames: the file containing the TaxIDs and the file with the COI returned by main.py script

    ACTIONS:
        -try to open the notfound.txt file (created by main.py) and count the number of lines (1 line = 1 accession number) and the number of unique lines
        -prompt the use for the TaxIDs filename
        -try to open the file and count the number of lines (1 line = 1 accession number) and the number of unique lines
        -prompt the user for the COI file name (COI....fasta)
        -split the file to get a list of sequences (info line + DNA sequence)
        -for each sequence:
            -add the accession number to the access list
            -look for the taxonomy information 
            -if the taxonomy correspond to Metazoa append the sequence to the animals list
            -if the taxonomy correspond to Plantae or Fungi append the sequence to the plantaefungi list
            -if the taxonomy does not correspond to Metazoa or Plantae or Fungi append the sequence to the others list
        -for each of these 3 lists write a file with the corresponding sequences
        -call the function table with the metazoan file and a unique output file name as inputs
    The function table retrive the info from the input file and write a text file formatted as csv with all the sequences for which the location contains a 'join' (i.e location with at least on intron)
        -call the function duplicates with the name of the metazoan file as input
    The duplicate function extract the for which the accession number is found to have more than one sequence, write these sequence in a file (Duplicates...fasta)
    and rewrites the metazoan file wihtout these sequences.

        -prints the number of sequences found for each kingdom, number of sequence in the notefound.txt file and number of sequences if the TaxIDs file (if the file is provided)

