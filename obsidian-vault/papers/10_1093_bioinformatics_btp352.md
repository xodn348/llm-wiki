---
title: The Sequence Alignment/Map format and SAMtools
doi: 10.1093/bioinformatics/btp352
year: 2009
venue: Bioinformatics
authors: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer,
  Gábor Marth, Gonçalo R. Abecasis
citations: 66938
openalex_id: https://openalex.org/W2108234281
tags:
- computer-science
- search-engine-indexing
- sequence-alignment
- k-mer
- multiple-sequence-alignment
---

# The Sequence Alignment/Map format and SAMtools

## Abstract

SUMMARY: The Sequence Alignment/Map (SAM) format is a generic alignment format for storing read alignments against reference sequences, supporting short and long reads (up to 128 Mbp) produced by different sequencing platforms. It is flexible in style, compact in size, efficient in random access and is the format in which alignments from the 1000 Genomes Project are released. SAMtools implements various utilities for post-processing alignments in the SAM format, such as indexing, variant caller and alignment viewer, and thus provides universal tools for processing read alignments. AVAILABILITY: http://samtools.sourceforge.net.


## Concepts

- [[computer-science|Computer science]] (0.65)
- [[search-engine-indexing|Search engine indexing]] (0.64)
- [[sequence-alignment|Sequence alignment]] (0.58)
- [[k-mer|k-mer]] (0.56)
- [[multiple-sequence-alignment|Multiple sequence alignment]] (0.55)


## Related


### Outgoing
- **cite** → [[10_1186_gb_2009_10_3_r25|Ultrafast and memory-efficient alignment of short DNA sequences to the human genome]] — SAMtools provides the SAM/BAM data format and processing utilities used to store and manipulate short-read alignments produced by Bowtie.
- **enables** → [[10_1038_s41586_020_2008_3|A new coronavirus associated with human respiratory disease in China]] — SAMtools provided the standard read-alignment and variant-processing infrastructure used to assemble and analyze sequencing data from the new coronavirus.
- **enables** → [[10_1093_bioinformatics_bty191|Minimap2: pairwise alignment for nucleotide sequences]] — SAM/BAM standardization enabled minimap2 to output interoperable alignments directly into common genomics analysis pipelines.

### Incoming
- **cite** ← [[10_1038_ng_806|A framework for variation discovery and genotyping using next-generation DNA sequencing data]] — The GATK framework uses the SAM/BAM alignment format and SAMtools ecosystem as core infrastructure for storing and processing sequencing reads.
- **cite** ← [[10_1093_bioinformatics_btp324|Fast and accurate short read alignment with Burrows–Wheeler transform]] — BWA relates to SAMtools through the SAM alignment format used to store and process short-read mapping results.
- **cite** ← [[10_1093_bioinformatics_btr330|The variant call format and VCFtools]] — VCFtools complements SAMtools by storing variant calls derived from sequence alignments represented in the SAM/BAM format.
- **cite** ← [[10_1038_s41586_020_2008_3|A new coronavirus associated with human respiratory disease in China]] — The coronavirus genome study used SAMtools/SAM-format read alignment workflows to assemble and analyze sequencing data from patient samples.
- **cite** ← [[10_1038_nbt_1621|Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation]] — Cufflinks uses SAM/BAM alignment files and SAMtools conventions as the input representation for RNA-Seq transcript assembly and quantification.
- **cite** ← [[10_1093_bioinformatics_bty191|Minimap2: pairwise alignment for nucleotide sequences]] — Minimap2 outputs and interoperates with the SAM/BAM alignment ecosystem defined by the SAM format and SAMtools paper.
- **cite** ← [[10_1038_nature09534|A map of human genome variation from population-scale sequencing]] — The 1000 Genomes Project cites Li et al. because SAMtools and the SAM/BAM format provided core infrastructure for aligning and calling variants from population-scale sequencing data.

## Sources

- DOI: <https://doi.org/10.1093/bioinformatics/btp352>
- OpenAlex: <https://openalex.org/W2108234281>