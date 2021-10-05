# nsdpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pypi](https://img.shields.io/pypi/v/nsdpy)](https://pypi.org/project/nsdpy/)



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

## Quick start

- Clone the repo from Github: 
```bash 
git clone https://github.com/RaphaelHebert/nsdpy.git
  ```
- pip:  
```bash 
pip install nsdpy
```
*minimum python version for nsdpy: 3.8.2* 

- Google Colab: save a copy of [this notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing) in your drive.

## Workflow

<img src="workflow.png" alt="workflow" width="600"/>

## Usage
### Google colab

[nsdpy colab notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing)

### Command line

```bash
nsdpy -r USER'S REQUEST [OPTIONS] 
```

## Authors and acknowledgment  

[Raphael Hebert](https://github.com/RaphaelHebert)

## Support

## License

Code and documentation copyright 2021 the nsdpy Authors. Code released under the MIT License.

## More Documentation

Official documentation:  
[Readthedocs](https://nsdpy.readthedocs.io/en/latest/main.html#overview)
  
On Google Doc:  
[Users manual on google doc](https://docs.google.com/document/d/1CJQg2Cv3P0lgWZRYd9xJQfj8qwIY4a-wtXa4VERdH2c/edit?usp=sharing=100)  



