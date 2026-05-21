---
title: The variant call format and VCFtools
doi: 10.1093/bioinformatics/btr330
openalex_id: https://openalex.org/W2149992227
year: 2011
venue: Bioinformatics
authors: Petr Danecek, Adam Auton, Gonçalo R. Abecasis, Cornelis A. Albers, Eric Banks,
  Mark A. DePristo, Robert E. Handsaker, Gerton Lunter
citations: 17533
fleming_tier: true
concepts:
- dbSNP
- Perl
- Computer science
- Suite
- Software
- Exome
- Annotation
- Exome sequencing
- World Wide Web
- Single-nucleotide polymorphism
---

# The variant call format and VCFtools

## Why this mattered

Before VCF, large sequencing projects lacked a compact, shared representation for variant calls that could carry genotypes, quality scores, filters, and annotations across many samples while still supporting efficient genomic range queries. Danecek et al. mattered because it turned variant data from project-specific output into portable infrastructure. By standardizing SNPs, indels, and structural variants in a compressed, indexable text format, VCF made it practical for different callers, databases, and analysis tools to exchange results without first negotiating a bespoke schema.

The immediate shift was especially important for population-scale genomics. The format was developed for the 1000 Genomes Project, where the central problem was not just detecting variants, but distributing and comparing millions of them across many individuals and analysis centers. Once VCF was adopted by resources such as dbSNP, UK10K, and the NHLBI Exome Project, variant calls became easier to merge, validate, filter, annotate, and reanalyze. VCFtools reinforced the standard by supplying common operations around the format, helping make VCF not merely a file specification but a working ecosystem.

Its longer-term importance is that many later breakthroughs in human genetics and precision medicine depended on this layer of interoperability. Genome-wide association studies, rare-variant burden analyses, clinical variant interpretation pipelines, large biobank sequencing projects, and modern joint-calling workflows all rely on being able to represent variation consistently across cohorts and tools. VCF did not itself solve variant discovery, but it made variant discovery outputs composable, searchable, and shareable at scale, which is why it became one of the quiet standards underlying the genomic data era.

## Abstract

SUMMARY: The variant call format (VCF) is a generic format for storing DNA polymorphism data such as SNPs, insertions, deletions and structural variants, together with rich annotations. VCF is usually stored in a compressed manner and can be indexed for fast data retrieval of variants from a range of positions on the reference genome. The format was developed for the 1000 Genomes Project, and has also been adopted by other projects such as UK10K, dbSNP and the NHLBI Exome Project. VCFtools is a software suite that implements various utilities for processing VCF files, including validation, merging, comparing and also provides a general Perl API. AVAILABILITY: http://vcftools.sourceforge.net


## Related

- **cite** → [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — VCFtools complements SAMtools by standardizing variant-call data downstream of sequence alignments represented in SAM/BAM format.
- **cite** → [A map of human genome variation from population-scale sequencing](10_1038_nature09534.md) — VCF was motivated by population-scale variant data such as the 1000 Genomes map of human genetic variation.


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btr330](https://doi.org/10.1093/bioinformatics/btr330)
- OpenAlex: [https://openalex.org/W2149992227](https://openalex.org/W2149992227)