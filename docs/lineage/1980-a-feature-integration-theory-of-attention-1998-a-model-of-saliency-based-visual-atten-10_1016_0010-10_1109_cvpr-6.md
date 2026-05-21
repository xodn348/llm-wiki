---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2020
  Momentum Contrast for Unsupervised Visual Representation
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1109/cvpr42600.2020.00975
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2020 Momentum Contrast for Unsupervised Visual Representation

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2014** — [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)
1. **2020** — [Momentum Contrast for Unsupervised Visual Representation Learning](../paper/10_1109_cvpr42600_2020_00975.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception.

“A feature-integration theory of attention” (1980) framed visual attention as the process that binds separately registered features into coherent object perception. Its key historical role here was not to provide a computational saliency algorithm, but to make feature maps and their integration a central way to think about early vision and attention.

“A model of saliency-based visual attention for rapid scene analysis” (1998) could build on that conceptual lineage by treating attention as guided by distinct feature channels whose activity can be combined into a saliency representation. In that sense, feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception, giving later models a principled bridge from low-level feature coding to attentional selection in scenes.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based attention supplied the selective visual-processing idea echoed by cascade-style focus on promising image regions in real-time face detection.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision as selective rather than exhaustive: a system can prioritize promising parts of a scene for further processing. That idea matters historically because rapid visual analysis is not only about better features, but about deciding where scarce computation should be spent.

“Robust Real-Time Face Detection” echoes that selective-processing lineage in a different engineering form. Its cascade-style detector focuses computation on image regions that remain plausible face candidates, rejecting unlikely regions early so real-time scanning becomes practical. The connection is conceptual rather than a direct method transfer: saliency-based attention supplied the broader idea of prioritizing promising visual regions, while the face detector turned selective focus into a robust real-time detection pipeline.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Viola-Jones showed that object categories could be detected efficiently with learned visual features, motivating the benchmarked detection task in Pascal VOC.

“Robust Real-Time Face Detection” helped make object detection feel like a practical, learnable vision task rather than a brittle, hand-engineered exercise. Viola-Jones showed that a detector could use learned visual features and run efficiently enough for real-time use, giving the field a concrete example of category-level visual detection working at useful speed.

“The Pascal Visual Object Classes (VOC) Challenge” broadened that ambition from faces to many everyday object categories, turning detection into a shared benchmarked task. In that lineage, Viola-Jones did not solve general object recognition, but it helped establish the template: learn visual features for a category, detect instances in images, and evaluate competing systems on a common task. The VOC Challenge made that template systematic and comparative across object classes.

### 2009 → 2014: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)

> Pascal VOC supplied the standardized object detection and segmentation benchmark on which R-CNN measured its region-based CNN improvements.

“The Pascal Visual Object Classes (VOC) Challenge” established a shared benchmark culture for object recognition, including standardized tasks for object detection and segmentation. By defining common datasets, evaluation protocols, and comparison points, Pascal VOC made it possible for later systems to demonstrate progress against a widely recognized yardstick rather than isolated, incompatible test setups.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” built directly on that foundation. R-CNN’s contribution was not just proposing region-based CNN features, but showing their value in the Pascal VOC setting where object detection and segmentation methods could be compared meaningfully. In that sense, Pascal VOC enabled R-CNN by supplying the standardized benchmark on which its region-based CNN improvements could be measured, interpreted, and placed within the field’s existing trajectory.

### 2014 → 2020: [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md) enables [Momentum Contrast for Unsupervised Visual Representation Learning](../paper/10_1109_cvpr42600_2020_00975.md)

> R-CNN popularized transfer evaluation for learned visual features, a protocol used to assess Momentum Contrast representations.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” helped make transfer evaluation central to computer vision representation learning. R-CNN showed that features learned in one setting could be repurposed effectively for downstream detection and segmentation, turning transfer performance into a practical way to judge whether a visual representation was broadly useful.

“Momentum Contrast for Unsupervised Visual Representation Learning” later operated in that same evaluation culture. MoCo proposed a self-supervised way to learn visual features without labels, but its significance depended on demonstrating that those features transferred well to standard downstream vision tasks. In that sense, R-CNN enabled MoCo not by providing its contrastive method, but by popularizing the protocol: learned visual representations are valuable when they support transfer beyond their original training objective.
