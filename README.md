# Speech-to-text aligner

## Installation

All you need is numpy and >= python 3.8

## Usage

`$ python aligner.py <proofread_transcript_id>`

This will align the proofread transcript at the given id with the firstdraft word timings.

The output of the alignment is in `out/aligned_<transcript_id>.json`

## Help
```python aligner.py --help
usage: align word timings with known transcript [-h] proofread_id

positional arguments:
  proofread_id  The STELLA transcript id for the proofread transcript

optional arguments:
  -h, --help    show this help message and exit
```
