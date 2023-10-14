import unittest
from unittest.mock import patch, call
from nsdpy import nsdpy
import tempfile
import os
import io


species_file_content = ""
with open("./tests/data/species_100.txt", "r") as file:
    for line in file:
        species_file_content += line

query = "Embryophyta[ORGN] AND (ITS1[All fields] OR ITS2[All fields] OR internal transcribed spacer[All fields]) AND 50:10000[SLEN] NOT gbdiv est[PROP] NOT gbdiv gss[PROP] NOT gbdiv env[PROP] NOT unverified[All Fields]"

call_1 = (
    "Embryophyta[ORGN] AND (ITS1[All fields] OR ITS2[All fields] OR internal transcribed spacer[All fields]) AND 50:10000[SLEN] NOT gbdiv est[PROP] NOT gbdiv gss[PROP] NOT gbdiv env[PROP] NOT unverified[All Fields] AND (Abies alba[ORGN] OR Abies concolor[ORGN] OR Acer campestre[ORGN] OR Acer monspessulanum[ORGN] OR Acer negundo[ORGN] OR Acer platanoides[ORGN] OR Acer pseudoplatanus[ORGN] OR Acer saccharinum[ORGN] OR Acer tataricum[ORGN] OR Achillea millefolium[ORGN] OR Achillea nobilis[ORGN] OR Achillea ptarmica[ORGN] OR Aconitum lycoctonum[ORGN] OR Acorus calamus[ORGN] OR Actaea spicata[ORGN] OR Adoxa moschatellina[ORGN] OR Aegopodium podagraria[ORGN] OR Aesculus hippocastanum[ORGN] OR Aesculus pavia[ORGN] OR Aethusa cynapium[ORGN] OR Agrimonia eupatoria[ORGN] OR Agrimonia procera[ORGN] OR Agrostemma githago[ORGN] OR Agrostis canina[ORGN] OR Agrostis capillaris[ORGN] OR Agrostis gigantea[ORGN] OR Agrostis stolonifera[ORGN] OR Agrostis vinealis[ORGN] OR Ailanthus altissima[ORGN] OR Ailanthus altissimus[ORGN] OR Aira caryophyllea[ORGN] OR Aira praecox[ORGN] OR Ajuga genevensis[ORGN] OR Ajuga reptans[ORGN] OR Alcea rosea[ORGN] OR Alchemilla arvensis[ORGN] OR Alchemilla monticola[ORGN] OR Alchemilla xanthochlora[ORGN] OR Alisma gramineum[ORGN] OR Alisma lanceolatum[ORGN] OR Alisma plantago-aquatica[ORGN] OR Alkekengi officinarum[ORGN] OR Alleniella complanata[ORGN] OR Alliaria petiolata[ORGN] OR Allium ampeloprasum[ORGN] OR Allium cepa[ORGN] OR Allium fistulosum[ORGN] OR Allium oleraceum[ORGN] OR Allium rotundum[ORGN] OR Allium sativum[ORGN] OR Allium schoenoprasum[ORGN] OR Allium scorodoprasum[ORGN] OR Allium sphaerocephalon[ORGN] OR Allium ursinum[ORGN] OR Allium vineale[ORGN] OR Alnus glutinosa[ORGN] OR Alnus incana[ORGN] OR Alopecurus aequalis[ORGN] OR Alopecurus arundinaceus[ORGN] OR Alopecurus geniculatus[ORGN] OR Alopecurus myosuroides[ORGN])",
    None,
)
call_2 = (
    "Embryophyta[ORGN] AND (ITS1[All fields] OR ITS2[All fields] OR internal transcribed spacer[All fields]) AND 50:10000[SLEN] NOT gbdiv est[PROP] NOT gbdiv gss[PROP] NOT gbdiv env[PROP] NOT unverified[All Fields] AND (Alopecurus pratensis[ORGN] OR Althaea hirsuta[ORGN] OR Althaea officinalis[ORGN] OR Alyssum alyssoides[ORGN] OR Amaranthus blitum[ORGN] OR Amaranthus retroflexus[ORGN] OR Amblystegium serpens[ORGN] OR Ambrosia artemisiifolia[ORGN] OR Ambrosia psilostachya[ORGN] OR Amelanchier lamarckii[ORGN] OR Amorpha fruticosa[ORGN] OR Anacamptis coriophora[ORGN] OR Anacamptis morio[ORGN] OR Anacamptis pyramidalis[ORGN] OR Anagallis arvensis[ORGN] OR Anchusa arvensis[ORGN] OR Andreaea rothii[ORGN] OR Andromeda polifolia[ORGN] OR Anemone alpina[ORGN] OR Anemone hepatica[ORGN] OR Anemone nemorosa[ORGN] OR Anemone pulsatilla[ORGN] OR Anemone ranunculoides[ORGN] OR Anemone sylvestris[ORGN])",
    None,
)

expected_calls = [
    call(
        (
            "Embryophyta[ORGN] AND (ITS1[All fields] OR ITS2[All fields] OR internal transcribed spacer[All fields]) AND 50:10000[SLEN] NOT gbdiv est[PROP] NOT gbdiv gss[PROP] NOT gbdiv env[PROP] NOT unverified[All Fields] AND (Abies alba[ORGN] OR Abies concolor[ORGN] OR Acer campestre[ORGN] OR Acer monspessulanum[ORGN] OR Acer negundo[ORGN] OR Acer platanoides[ORGN] OR Acer pseudoplatanus[ORGN] OR Acer saccharinum[ORGN] OR Acer tataricum[ORGN] OR Achillea millefolium[ORGN] OR Achillea nobilis[ORGN] OR Achillea ptarmica[ORGN] OR Aconitum lycoctonum[ORGN] OR Acorus calamus[ORGN] OR Actaea spicata[ORGN] OR Adoxa moschatellina[ORGN] OR Aegopodium podagraria[ORGN] OR Aesculus hippocastanum[ORGN] OR Aesculus pavia[ORGN] OR Aethusa cynapium[ORGN] OR Agrimonia eupatoria[ORGN] OR Agrimonia procera[ORGN] OR Agrostemma githago[ORGN] OR Agrostis canina[ORGN] OR Agrostis capillaris[ORGN] OR Agrostis gigantea[ORGN] OR Agrostis stolonifera[ORGN] OR Agrostis vinealis[ORGN] OR Ailanthus altissima[ORGN] OR Ailanthus altissimus[ORGN] OR Aira caryophyllea[ORGN] OR Aira praecox[ORGN] OR Ajuga genevensis[ORGN] OR Ajuga reptans[ORGN] OR Alcea rosea[ORGN] OR Alchemilla arvensis[ORGN] OR Alchemilla monticola[ORGN] OR Alchemilla xanthochlora[ORGN] OR Alisma gramineum[ORGN] OR Alisma lanceolatum[ORGN] OR Alisma plantago-aquatica[ORGN] OR Alkekengi officinarum[ORGN] OR Alleniella complanata[ORGN] OR Alliaria petiolata[ORGN] OR Allium ampeloprasum[ORGN] OR Allium cepa[ORGN] OR Allium fistulosum[ORGN] OR Allium oleraceum[ORGN] OR Allium rotundum[ORGN] OR Allium sativum[ORGN] OR Allium schoenoprasum[ORGN] OR Allium scorodoprasum[ORGN] OR Allium sphaerocephalon[ORGN] OR Allium ursinum[ORGN] OR Allium vineale[ORGN] OR Alnus glutinosa[ORGN] OR Alnus incana[ORGN] OR Alopecurus aequalis[ORGN] OR Alopecurus arundinaceus[ORGN] OR Alopecurus geniculatus[ORGN] OR Alopecurus myosuroides[ORGN])",
            None,
        )
    ),
    call(
        (
            "Embryophyta[ORGN] AND (ITS1[All fields] OR ITS2[All fields] OR internal transcribed spacer[All fields]) AND 50:10000[SLEN] NOT gbdiv est[PROP] NOT gbdiv gss[PROP] NOT gbdiv env[PROP] NOT unverified[All Fields] AND (Alopecurus pratensis[ORGN] OR Althaea hirsuta[ORGN] OR Althaea officinalis[ORGN] OR Alyssum alyssoides[ORGN] OR Amaranthus blitum[ORGN] OR Amaranthus retroflexus[ORGN] OR Amblystegium serpens[ORGN] OR Ambrosia artemisiifolia[ORGN] OR Ambrosia psilostachya[ORGN] OR Amelanchier lamarckii[ORGN] OR Amorpha fruticosa[ORGN] OR Anacamptis coriophora[ORGN] OR Anacamptis morio[ORGN] OR Anacamptis pyramidalis[ORGN] OR Anagallis arvensis[ORGN] OR Anchusa arvensis[ORGN] OR Andreaea rothii[ORGN] OR Andromeda polifolia[ORGN] OR Anemone alpina[ORGN] OR Anemone hepatica[ORGN] OR Anemone nemorosa[ORGN] OR Anemone pulsatilla[ORGN] OR Anemone ranunculoides[ORGN] OR Anemone sylvestris[ORGN] OR Anemone vernalis[ORGN] OR Anethum graveolens[ORGN] OR Aneura pinguis[ORGN] OR Angelica sylvestris[ORGN] OR Anomodon viticulosus[ORGN] OR Antennaria dioica[ORGN] OR Anthemis arvensis[ORGN] OR Anthemis cotula[ORGN] OR Anthemis ruthenica[ORGN] OR Anthericum liliago[ORGN] OR Anthericum ramosum[ORGN] OR Anthoxanthum odoratum[ORGN] OR Anthriscus caucalis[ORGN] OR Anthriscus cerefolium[ORGN] OR Anthriscus sylvestris[ORGN]))",
            None,
        )
    ),
]


class TestMyScript(unittest.TestCase):
    @patch(
        "sys.argv", ["nsdpy.py", "--r", query, "--list", "./tests/data/species_100.txt"]
    )
    @patch("nsdpy.nsdpy.esearchquery", autospec=True)  # Mock esearchquery function
    @patch("nsdpy.nsdpy.taxids", autospec=True)
    def test_list_with_txt_file(self, mock_taxids, mock_esearchquery):
        mock_taxids.return_value = {"23423423": "123123"}  # Modify as needed
        mock_esearchquery.return_value = {
            "esearchresult": {"count": "3", "webenv": "lol", "querykey": "randomkey"}
        }

        nsdpy.main()
        mock_esearchquery.assert_has_calls(expected_calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
