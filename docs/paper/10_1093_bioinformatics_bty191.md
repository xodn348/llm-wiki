---
title: 'Minimap2: pairwise alignment for nucleotide sequences'
doi: 10.1093/bioinformatics/bty191
openalex_id: https://openalex.org/W2789843538
year: 2018
venue: Bioinformatics
authors: Heng Li
citations: 16482
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

Minimap2 mattered because it turned long-read alignment from a specialized bottleneck into a general-purpose infrastructure problem that could be handled at scale. Earlier aligners were often optimized for one regime: short Illumina reads, noisy PacBio/Oxford Nanopore genomic reads, transcript reads, or assembly-to-reference comparison. Li’s contribution was not only speed, but unification: one mapper could align accurate short reads, noisy kilobase-to-ultralong reads, full-length RNA/cDNA reads, and very large contigs or chromosome-scale sequences with competitive or better accuracy. Its minimizer-based seeding, chaining heuristics, split-read support, and long-gap-aware scoring made it practical to treat long insertions, deletions, structural variation, exon-scale gaps, and assembly comparisons as routine alignment cases rather than exceptional workloads.

The practical shift was that long-read sequencing could be used in everyday genomics pipelines without alignment becoming the limiting step. After minimap2, researchers could more readily map noisy nanopore and PacBio reads for structural-variant discovery, phase haplotypes, polish and compare assemblies, align full-length transcript reads, and evaluate chromosome-scale assemblies. This helped long-read analysis move from proof-of-concept studies into large-scale human, plant, microbial, and transcriptomic projects. Its speed also changed iteration: parameters, assemblies, samples, and cohorts could be reprocessed repeatedly, which matters when the biology depends on detecting complex rearrangements or transcript structures that short-read mappers were not designed to expose cleanly.

Its influence is visible in the long-read ecosystem that followed. Tools for structural-variant calling, pangenome construction, telomere-to-telomere assembly evaluation, isoform discovery, and nanopore clinical or pathogen genomics commonly rely on minimap2 or on assumptions it helped normalize: that long noisy reads can be aligned quickly enough, accurately enough, and flexibly enough to serve as primary evidence. The paper did not create long-read sequencing, but it supplied one of the key computational primitives that made long-read sequencing broadly usable. In that sense, minimap2 was paradigm-shifting because it converted a rapidly improving experimental technology into a scalable analytical platform.

## Abstract

Abstract Motivation Recent advances in sequencing technologies promise ultra-long reads of ∼100 kb in average, full-length mRNA or cDNA reads in high throughput and genomic contigs over 100 Mb in length. Existing alignment programs are unable or inefficient to process such data at scale, which presses for the development of new alignment algorithms. Results Minimap2 is a general-purpose alignment program to map DNA or long mRNA sequences against a large reference database. It works with accurate short reads of ≥100 bp in length, ≥1 kb genomic reads at error rate ∼15%, full-length noisy Direct RNA or cDNA reads and assembly contigs or closely related full chromosomes of hundreds of megabases in length. Minimap2 does split-read alignment, employs concave gap cost for long insertions and deletions and introduces new heuristics to reduce spurious alignments. It is 3–4 times as fast as mainstream short-read mappers at comparable accuracy, and is ≥30 times faster than long-read genomic or cDNA mappers at higher accuracy, surpassing most aligners specialized in one type of alignment. Availability and implementation https://github.com/lh3/minimap2 Supplementary information Supplementary data are available at Bioinformatics online.


## Related

- **cite** → [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — Minimap2 uses seed-and-extend alignment ideas related to BWA's Burrows-Wheeler-transform indexing for fast nucleotide alignment.
- **cite** → [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — Minimap2 emits and interoperates with SAM/BAM alignments defined by the SAM format and SAMtools ecosystem.
- **cite** → [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](10_1093_nar_25_17_3389.md) — Minimap2's chaining and gapped alignment stage follows the seed-extension lineage of Gapped BLAST.
- **cite** → [A framework for variation discovery and genotyping using next-generation DNA sequencing data](10_1038_ng_806.md) — Minimap2 supports variant-discovery workflows that commonly feed alignments into GATK-style genotyping frameworks.
- **enables** ← [Fast and accurate short read alignment with Burrows–Wheeler transform](10_1093_bioinformatics_btp324.md) — BWA demonstrated Burrows-Wheeler-transform indexing for fast read alignment, enabling minimap2's later emphasis on efficient large-scale nucleotide mapping.
- **enables** ← [The Sequence Alignment/Map format and SAMtools](10_1093_bioinformatics_btp352.md) — SAM/BAM gave minimap2 a standard alignment output and tooling ecosystem for representing and downstream-processing nucleotide mappings.
- **enables** ← [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](10_1093_nar_25_17_3389.md) — Gapped BLAST and PSI-BLAST established seed-and-extend alignment with gapped extension, a search paradigm minimap2 builds on for pairwise sequence alignment.
- **enables** ← [A framework for variation discovery and genotyping using next-generation DNA sequencing data](10_1038_ng_806.md) — The GATK framework defined variant-discovery workflows that depend on accurate read alignments, motivating minimap2's practical role in sequencing pipelines.


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191)
- OpenAlex: [https://openalex.org/W2789843538](https://openalex.org/W2789843538)