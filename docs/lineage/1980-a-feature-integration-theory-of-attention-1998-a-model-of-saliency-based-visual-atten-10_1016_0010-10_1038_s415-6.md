---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2021
  Highly accurate protein structure prediction with
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1038/s41586-021-03819-2
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2021 Highly accurate protein structure prediction with

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2016** — [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)
1. **2021** — [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception.

Treisman and Gelade’s 1980 feature-integration theory framed attention as the process that binds information from separate feature dimensions into coherent object perception. That made it natural to think of early vision as organized around feature-specific representations, with attention selecting or combining across them rather than treating a scene as an undifferentiated whole.

Itti, Koch, and Niebur’s 1998 saliency-based model inherits that conceptual scaffold: rapid scene analysis can begin from multiple feature maps whose signals are integrated into a priority structure for attention. In that lineage, feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception, giving later computational work a clear way to model how visual features guide where attention goes.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based attention supplied the selective visual-processing idea echoed by cascade-style focus on promising image regions in real-time face detection.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize the idea that vision can be made efficient by prioritizing likely informative parts of a scene rather than processing everything with equal depth. Its saliency-based account of selective attention gave computational shape to a broader strategy: use early cues to focus resources on promising visual regions under time pressure.

“Robust Real-Time Face Detection” echoes that selective-processing lineage in an engineering form. Rather than exhaustively applying heavy analysis everywhere, its cascade-style detector rapidly rejects unlikely image windows and concentrates later computation on candidates that remain plausible. The connection is not that the face detector directly implements saliency, but that both works embody the same enabling idea: real-time vision becomes practical when attention or computation is staged toward the most promising regions first.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Viola-Jones showed that object categories could be detected efficiently with learned visual features, motivating the benchmarked detection task in Pascal VOC.

“Robust Real-Time Face Detection” made object detection feel like an engineered, learnable visual task rather than a hand-built special case. Viola-Jones showed that learned visual features, arranged in an efficient cascade, could locate a category in images fast enough for practical use. Even though its focus was faces, the broader lesson was that detection could be framed as training a system to recognize category-specific visual patterns under computational constraints.

“The Pascal Visual Object Classes (VOC) Challenge” extended that logic into a public benchmark culture for many object categories. If Viola-Jones helped prove that learned detectors could work efficiently for a visually meaningful class, Pascal VOC helped turn object detection into a comparative research problem: define categories, datasets, tasks, and evaluation so methods could be measured against one another. The lineage is from practical learned category detection to standardized, benchmarked visual object detection.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)

> PASCAL VOC established object-recognition benchmarks and evaluation practices that helped measure ResNet's deep convolutional image classification gains.

The Pascal Visual Object Classes (VOC) Challenge helped make object recognition a benchmarked, comparable problem: researchers could test recognition systems against shared datasets, tasks, and evaluation practices rather than only isolated demonstrations. That infrastructure mattered because it gave later computer-vision work a common language for measuring progress in learned visual representations and convolutional recognition systems.

Deep Residual Learning for Image Recognition built on that benchmarking culture. ResNet’s contribution was not enabled by VOC through a specific algorithmic technique, but through the broader evaluation environment VOC helped establish: deep convolutional models could be judged as part of a lineage of object-recognition progress, with their gains made legible against established practices for measuring visual recognition performance.

### 2016 → 2021: [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md) enables [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

> Residual connections enabled very deep neural networks, an architectural principle used in AlphaFold's deep protein-structure model.

“Deep Residual Learning for Image Recognition” helped establish residual connections as a practical way to train very deep neural networks. Its central architectural idea was not limited to image recognition: by letting layers learn residual transformations, it made depth easier to optimize and helped normalize the use of skip-connected deep models across machine learning.

AlphaFold’s 2021 protein-structure model drew on that broader architectural lineage. Protein structure prediction required learning complex relationships from sequence and evolutionary information, and residual-style deep networks were part of the design vocabulary that made such large, stacked models workable. In that sense, ResNet enabled AlphaFold not by solving biology directly, but by proving and popularizing a neural-network principle: very deep models can be trained effectively when information can flow through residual connections.
