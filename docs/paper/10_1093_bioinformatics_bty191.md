---
title: 'Minimap2: pairwise alignment for nucleotide sequences'
doi: 10.1093/bioinformatics/bty191
openalex_id: https://openalex.org/W2789843538
year: 2018
venue: Bioinformatics
authors: Heng Li
citations: 16468
fleming_tier: true
concepts:
- Pairwise comparison
- Nucleotide
- Multiple sequence alignment
- Sequence alignment
- Computational biology
- Computer science
- Genetics
- Biology
- Artificial intelligence
- Gene
---

# Minimap2: pairwise alignment for nucleotide sequences

## Why this mattered

_TBD_

## Abstract

Abstract Motivation Recent advances in sequencing technologies promise ultra-long reads of ∼100 kb in average, full-length mRNA or cDNA reads in high throughput and genomic contigs over 100 Mb in length. Existing alignment programs are unable or inefficient to process such data at scale, which presses for the development of new alignment algorithms. Results Minimap2 is a general-purpose alignment program to map DNA or long mRNA sequences against a large reference database. It works with accurate short reads of ≥100 bp in length, ≥1 kb genomic reads at error rate ∼15%, full-length noisy Direct RNA or cDNA reads and assembly contigs or closely related full chromosomes of hundreds of megabases in length. Minimap2 does split-read alignment, employs concave gap cost for long insertions and deletions and introduces new heuristics to reduce spurious alignments. It is 3–4 times as fast as mainstream short-read mappers at comparable accuracy, and is ≥30 times faster than long-read genomic or cDNA mappers at higher accuracy, surpassing most aligners specialized in one type of alignment. Availability and implementation https://github.com/lh3/minimap2 Supplementary information Supplementary data are available at Bioinformatics online.


## Related

- **cite** → [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — Minimap2 builds on the Burrows-Wheeler-transform alignment lineage represented by BWA while adapting alignment to long noisy reads and assemblies.
- **cite** → [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — Minimap2 outputs and interoperates with the SAM/BAM alignment ecosystem defined by the SAM format and SAMtools paper.
- **cite** → [A framework for variation discovery and genotyping using next-generation DNA sequencing data](10_1038_ng_806.md) — Minimap2 is positioned upstream of variant-discovery workflows such as GATK by providing read alignments used for genotyping from sequencing data.
- **enables** ← [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — BWA's Burrows-Wheeler indexing enabled minimap2's emphasis on fast seed-and-extend alignment for large-scale nucleotide read mapping.
- **enables** ← [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — SAM/BAM standardization enabled minimap2 to output interoperable alignments directly into common genomics analysis pipelines.
- **enables** ← [A framework for variation discovery and genotyping using next-generation DNA sequencing data](10_1038_ng_806.md) — GATK's variant-discovery workflows depend on accurate read-to-reference alignment, a core capability later accelerated and generalized by Minimap2's seed-chain-align method.


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191)
- OpenAlex: [https://openalex.org/W2789843538](https://openalex.org/W2789843538)