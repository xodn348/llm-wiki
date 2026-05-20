---
title: 'Minimap2: pairwise alignment for nucleotide sequences'
doi: 10.1093/bioinformatics/bty191
year: 2018
venue: Bioinformatics
authors: Heng Li
citations: 16468
openalex_id: https://openalex.org/W2789843538
tags:
- pairwise-comparison
- nucleotide
- multiple-sequence-alignment
- sequence-alignment
- computational-biology
---

# Minimap2: pairwise alignment for nucleotide sequences

## Abstract

Abstract Motivation Recent advances in sequencing technologies promise ultra-long reads of ∼100 kb in average, full-length mRNA or cDNA reads in high throughput and genomic contigs over 100 Mb in length. Existing alignment programs are unable or inefficient to process such data at scale, which presses for the development of new alignment algorithms. Results Minimap2 is a general-purpose alignment program to map DNA or long mRNA sequences against a large reference database. It works with accurate short reads of ≥100 bp in length, ≥1 kb genomic reads at error rate ∼15%, full-length noisy Direct RNA or cDNA reads and assembly contigs or closely related full chromosomes of hundreds of megabases in length. Minimap2 does split-read alignment, employs concave gap cost for long insertions and deletions and introduces new heuristics to reduce spurious alignments. It is 3–4 times as fast as mainstream short-read mappers at comparable accuracy, and is ≥30 times faster than long-read genomic or cDNA mappers at higher accuracy, surpassing most aligners specialized in one type of alignment. Availability and implementation https://github.com/lh3/minimap2 Supplementary information Supplementary data are available at Bioinformatics online.


## Concepts

- [[pairwise-comparison|Pairwise comparison]] (0.84)
- [[nucleotide|Nucleotide]] (0.59)
- [[multiple-sequence-alignment|Multiple sequence alignment]] (0.56)
- [[sequence-alignment|Sequence alignment]] (0.49)
- [[computational-biology|Computational biology]] (0.48)


## Related


### Outgoing
- **cite** → [[10_1093_bioinformatics_btp324|Fast and accurate short read alignment with Burrows–Wheeler transform]] — Minimap2 builds on the Burrows-Wheeler-transform alignment lineage represented by BWA while adapting alignment to long noisy reads and assemblies.
- **cite** → [[10_1093_bioinformatics_btp352|The Sequence Alignment/Map format and SAMtools]] — Minimap2 outputs and interoperates with the SAM/BAM alignment ecosystem defined by the SAM format and SAMtools paper.
- **cite** → [[10_1038_ng_806|A framework for variation discovery and genotyping using next-generation DNA sequencing data]] — Minimap2 is positioned upstream of variant-discovery workflows such as GATK by providing read alignments used for genotyping from sequencing data.

### Incoming
- **enables** ← [[10_1093_bioinformatics_btp324|Fast and accurate short read alignment with Burrows–Wheeler transform]] — BWA's Burrows-Wheeler indexing enabled minimap2's emphasis on fast seed-and-extend alignment for large-scale nucleotide read mapping.
- **enables** ← [[10_1093_bioinformatics_btp352|The Sequence Alignment/Map format and SAMtools]] — SAM/BAM standardization enabled minimap2 to output interoperable alignments directly into common genomics analysis pipelines.
- **enables** ← [[10_1038_ng_806|A framework for variation discovery and genotyping using next-generation DNA sequencing data]] — GATK's variant-discovery workflows depend on accurate read-to-reference alignment, a core capability later accelerated and generalized by Minimap2's seed-chain-align method.

## Sources

- DOI: <https://doi.org/10.1093/bioinformatics/bty191>
- OpenAlex: <https://openalex.org/W2789843538>