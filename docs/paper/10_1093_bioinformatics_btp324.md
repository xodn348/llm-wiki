---
title: Fast and accurate short read alignment with Burrows–Wheeler transform
doi: 10.1093/bioinformatics/btp324
openalex_id: https://openalex.org/W2103441770
year: 2009
venue: Bioinformatics
authors: Heng Li, Richard Durbin
citations: 62244
fleming_tier: true
concepts:
- Computer science
- Software
- Alignment-free sequence analysis
- Hash table
- Reference genome
- Hybrid genome assembly
- Indel
- Multiple sequence alignment
- Sequence alignment
- DNA sequencing
---

# Fast and accurate short read alignment with Burrows–Wheeler transform

## Why this mattered

Li and Durbin’s BWA work made Burrows–Wheeler transform/FM-index alignment a practical foundation for high-throughput genomics. The key shift was not simply faster read mapping, but a different scaling regime: large mammalian references could be searched accurately with modest memory, while preserving enough speed for the exploding output of next-generation sequencers. This helped move whole-genome resequencing from a specialized computational bottleneck toward a routine analysis step.

After BWA, short-read and longer-read alignment became less dependent on slower hash-based tools such as BLAT and SSAHA2 for large genomes. The paper showed that indexed, compressed reference search could deliver both accuracy and throughput, making it feasible to align millions to billions of reads as a standard precursor to SNP calling, indel detection, copy-number analysis, RNA-seq quantification, and population-scale genomics. In practice, BWA became one of the core aligners behind the sequencing pipelines that enabled projects such as the 1000 Genomes Project and later clinical and population sequencing efforts.

Its longer-term importance is that it helped establish read alignment as a stable infrastructure layer for genomics. Subsequent breakthroughs in variant calling, cancer genomics, ancient DNA, metagenomics, and clinical sequencing depended on reliable, scalable mapping to reference genomes. Later aligners and graph-based methods would revise parts of this model, especially for long reads and structurally diverse genomes, but BWA defined the dominant computational pattern for the short-read era: compact indexing, fast approximate matching, and integration into reproducible genome analysis workflows.

## Abstract

MOTIVATION: Many programs for aligning short sequencing reads to a reference genome have been developed in the last 2 years. Most of them are very efficient for short reads but inefficient or not applicable for reads >200 bp because the algorithms are heavily and specifically tuned for short queries with low sequencing error rate. However, some sequencing platforms already produce longer reads and others are expected to become available soon. For longer reads, hashing-based software such as BLAT and SSAHA2 remain the only choices. Nonetheless, these methods are substantially slower than short-read aligners in terms of aligned bases per unit time. RESULTS: We designed and implemented a new algorithm, Burrows-Wheeler Aligner's Smith-Waterman Alignment (BWA-SW), to align long sequences up to 1 Mb against a large sequence database (e.g. the human genome) with a few gigabytes of memory. The algorithm is as accurate as SSAHA2, more accurate than BLAT, and is several to tens of times faster than both. AVAILABILITY: http://bio-bwa.sourceforge.net


## Related

- **cite** → [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — 


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324)
- OpenAlex: [https://openalex.org/W2103441770](https://openalex.org/W2103441770)