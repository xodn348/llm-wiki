---
title: The Sequence Alignment/Map format and SAMtools
doi: 10.1093/bioinformatics/btp352
openalex_id: https://openalex.org/W2108234281
year: 2009
venue: Bioinformatics
authors: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer,
  Gábor Marth, Gonçalo R. Abecasis
citations: 66849
fleming_tier: true
concepts:
- Computer science
- Search engine indexing
- Sequence alignment
- k-mer
- Multiple sequence alignment
- File format
- Sanger sequencing
- Sequence (biology)
- Alignment-free sequence analysis
- Information retrieval
---

# The Sequence Alignment/Map format and SAMtools

## Why this mattered

Before SAM, high-throughput sequencing data were fragmented across aligner-specific formats, making downstream analysis brittle and difficult to reproduce across platforms and projects. Li et al. made a decisive infrastructural move: they separated the representation of read alignments from any one aligner or sequencing technology. SAM’s text form, its compressed binary counterpart BAM, coordinate sorting, indexing, and random access turned alignment files into a portable substrate for large-scale genomics rather than intermediate byproducts of individual tools.

This mattered because it made population-scale sequencing operational. The paper explicitly tied SAM/BAM to the 1000 Genomes Project, where standardized, randomly accessible alignments were essential for distributing and reanalyzing data at unprecedented scale. SAMtools also supplied common post-alignment operations, including viewing, indexing, and variant calling, so researchers could build workflows around a shared file format and toolchain instead of repeatedly translating between incompatible representations.

The broader paradigm shift was that genomics gained something analogous to a systems interface: aligners, variant callers, genome browsers, quality-control tools, and pipelines could interoperate through a stable alignment/map layer. Subsequent breakthroughs in human variation discovery, cancer genomics, clinical sequencing, and large reference resources depended on this kind of standardization. The paper was not a new biological theory, but it changed what biological questions could be asked routinely by making massive sequencing datasets exchangeable, queryable, and computable at scale.

## Abstract

SUMMARY: The Sequence Alignment/Map (SAM) format is a generic alignment format for storing read alignments against reference sequences, supporting short and long reads (up to 128 Mbp) produced by different sequencing platforms. It is flexible in style, compact in size, efficient in random access and is the format in which alignments from the 1000 Genomes Project are released. SAMtools implements various utilities for post-processing alignments in the SAM format, such as indexing, variant caller and alignment viewer, and thus provides universal tools for processing read alignments. AVAILABILITY: http://samtools.sourceforge.net.



## Related

- **cite** ← [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — BWA links to SAMtools through producing short-read alignments commonly represented and processed in the SAM/BAM format.
## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352)
- OpenAlex: [https://openalex.org/W2108234281](https://openalex.org/W2108234281)