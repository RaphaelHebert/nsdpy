# nsdpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pypi](https://img.shields.io/pypi/v/nsdpy)](https://pypi.org/project/nsdpy/)
[![Python 3.8](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/nsdpy/badge/?version=latest)](https://nsdpy.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/RaphaelHebert/nsdpy/badge.svg?branch=fix/longSpeciesList)](https://coveralls.io/github/RaphaelHebert/nsdpy?branch=fix/longSpeciesList)

<div align="center" style="text-align: center">
Your support means the world to me and helps me continue developing and maintaining this repository to benefit the entire community. Thank you for making a difference in the open-source world! </div>
<br/>
<div align="center" style="text-align: center;" markdown="1"><a href="https://www.buymeacoffee.com/joe010" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
</div>

## 

- [Introduction](#introduction)
- [Workfolw](#workflow)
- [Quick start](#quick-start)
- [Usage](#usage)
  - [Google Colab](#google-colab)
  - [Command line](#command-line)
- [Authors and acknowledgment](#authors-and-acknowledgment)
- [Support](#support)
- [Licence](#license)
- [More Documentation](#more-documentation)

## Introduction

nsdpy (nucleotide or NCBI sequence downloader) aims to ease the download and sort of big bacth of DNA sequences from the NCBI database.
It can also be usefull to filter the sequences based on their annotations.
Using nsdpy the user can:

- **Search** NCBI nucleotide database
- **Download** the fasta files or the cds_fasta files corresponding to the result of the search
- **Sort** the sequences based on their taxonomy
- **Select** coding sequences from cds files based on the gene names using one or more regular expressions.
This can help the user retrieve some sequences for which the gene name is annotated in another field.
- **Retrieve** the taxonomic information and add it to the output sequences.

## Quick start

- Clone the repo from Github:
```bash
git clone https://github.com/RaphaelHebert/nsdpy.git
  ```
- pip:
_depending on the user environment pip may be replaced by pip3 if pip3 is used_
```bash
pip install nsdpy
```
*minimum python version for nsdpy: 3.8.2*

- Google Colab: save a copy of [this notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing) in your drive.

## Workflow

<img src="https://docs.google.com/drawings/d/e/2PACX-1vRD4h7l0S57op_4j-5xsz8iv1j1XBliw-jEdtnWOIq-JAU2l8kSV6d1NmkHd5Q4zhUmZCA3SHUSuHJw/pub?w=801&amp;h=744" width="600" />

## Usage
### Google colab

[nsdpy colab notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing)

### Command line

```bash
nsdpy -r "USER'S REQUEST" [OPTIONS]
```

## Authors and acknowledgment

[Raphael Hebert](https://github.com/RaphaelHebert)
[Emese Meglecz](https://github.com/meglecz)


## Support

## License

Code and documentation copyright 2021 the nsdpy authors. Code released under the MIT License.

## More Documentation

Official documentation:
[Readthedocs](https://nsdpy.readthedocs.io/en/latest/main.html#overview)
