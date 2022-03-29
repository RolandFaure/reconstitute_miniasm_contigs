# reconstitute_miniasm_contigs

This small python code re-builds the contig sequence from the 'a' lines of the miniasm output. It is designed to work around an unexplained issue where miniasm outputs contigs looking like 'NNNNNNNNN'.

```
usage: python build_seq_from_miniasm.py [-h] --assembly ASSEMBLY --reads READS
                                 --output OUTPUT

build_seq_from_miniasm : to rebuild the contigs from the 'a' lines and the
fasta/q file

optional arguments:
  -h, --help           show this help message and exit
  --assembly ASSEMBLY  Assembly from miniasm, in GFA format with or without
                       the contig sequences
  --reads READS        Fasta/q file of the reads used to build the assembly
  --output OUTPUT      Output file in GFA format

```
