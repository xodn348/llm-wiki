---
title: The Sequence Alignment/Map format and SAMtools
doi: 10.1093/bioinformatics/btp352
openalex_id: https://openalex.org/W2108234281
year: 2009
venue: Bioinformatics
authors: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer,
  Gábor Marth, Gonçalo R. Abecasis
citations: 66938
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

- **cite** → [Ultrafast and memory-efficient alignment of short DNA sequences to the human genome](10_1186_gb_2009_10_3_r25.md) — SAMtools provides the SAM/BAM data format and processing utilities used to store and manipulate short-read alignments produced by Bowtie.
- **enables** → [A new coronavirus associated with human respiratory disease in China](10_1038_s41586_020_2008_3.md) — SAMtools provided the standard read-alignment and variant-processing infrastructure used to assemble and analyze sequencing data from the new coronavirus.
- **enables** → [Minimap2: pairwise alignment for nucleotide sequences](10_1093_bioinformatics_bty191.md) — SAM/BAM standardization enabled minimap2 to output interoperable alignments directly into common genomics analysis pipelines.
- **cite** ← [A framework for variation discovery and genotyping using next-generation DNA sequencing data](10_1038_ng_806.md) — The GATK framework uses the SAM/BAM alignment format and SAMtools ecosystem as core infrastructure for storing and processing sequencing reads.
- **cite** ← [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — BWA relates to SAMtools through the SAM alignment format used to store and process short-read mapping results.
- **cite** ← [The variant call format and VCFtools](10_1093_bioinformatics_btr330.md) — VCFtools complements SAMtools by storing variant calls derived from sequence alignments represented in the SAM/BAM format.
- **cite** ← [A new coronavirus associated with human respiratory disease in China](10_1038_s41586_020_2008_3.md) — The coronavirus genome study used SAMtools/SAM-format read alignment workflows to assemble and analyze sequencing data from patient samples.
- **cite** ← [Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation](10_1038_nbt_1621.md) — Cufflinks uses SAM/BAM alignment files and SAMtools conventions as the input representation for RNA-Seq transcript assembly and quantification.
- **cite** ← [Minimap2: pairwise alignment for nucleotide sequences](10_1093_bioinformatics_bty191.md) — Minimap2 outputs and interoperates with the SAM/BAM alignment ecosystem defined by the SAM format and SAMtools paper.
- **cite** ← [A map of human genome variation from population-scale sequencing](10_1038_nature09534.md) — The 1000 Genomes Project cites Li et al. because SAMtools and the SAM/BAM format provided core infrastructure for aligning and calling variants from population-scale sequencing data.


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352)
- OpenAlex: [https://openalex.org/W2108234281](https://openalex.org/W2108234281)