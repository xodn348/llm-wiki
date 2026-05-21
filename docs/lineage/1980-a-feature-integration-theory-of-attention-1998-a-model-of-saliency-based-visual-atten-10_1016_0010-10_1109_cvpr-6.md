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

> Feature-integration theory linked attention to basic visual feature maps, which Itti, Koch, and Niebur computationalized as saliency maps for rapid scene analysis.

*A feature-integration theory of attention* (1980) framed visual attention as operating over basic feature representations, helping make the idea of separable feature maps central to accounts of perception. Its importance for later work was not that it supplied a computational saliency algorithm, but that it connected attention to the organization and integration of visual features.

*A model of saliency-based visual attention for rapid scene analysis* (1998) built on that conceptual lineage by computationalizing feature-based attention into saliency maps. Itti, Koch, and Niebur translated the feature-map view into a model for rapidly selecting visually conspicuous locations in scenes. In that sense, the earlier theory enabled the later paper by making feature maps a plausible substrate for attention, which the 1998 model turned into an explicit computational architecture for scene analysis.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based rapid scene analysis reinforced the idea of fast attentional feature selection that Viola-Jones implemented through efficient visual features.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision in which scenes could be processed quickly by selecting informative features before deeper recognition. Its saliency framework reinforced the broader idea that attention-like mechanisms can prioritize parts of an image through efficient low-level visual cues.

“Robust Real-Time Face Detection” carried that fast-selection logic into a practical detection system. Viola-Jones did not implement saliency itself, but its cascade of efficient visual features reflects the same lineage: rapid scene analysis depends on choosing simple, discriminative visual evidence early, so later computation is spent only where it is most useful.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

“Robust Real-Time Face Detection” helped make sliding-window detection a practical and influential template: scan an image across positions and scales, score each window, and turn local classifier responses into object detections. Its focus on real-time face detection showed that object localization could be framed as repeated, efficient classification over image regions, not just whole-image recognition.

“The Pascal Visual Object Classes (VOC) Challenge” then broadened that methodology into a benchmark setting across many visual object categories. Rather than centering on faces as a single, highly structured class, VOC helped standardize the evaluation of detection and recognition systems over varied object classes, making the sliding-window detection paradigm part of a wider comparative framework for visual object understanding.

### 2009 → 2014: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)

> PASCAL VOC provided the object-detection benchmark and evaluation protocol on which R-CNN demonstrated region-based CNN detection gains.

“The Pascal Visual Object Classes (VOC) Challenge” helped define object detection as a shared benchmark problem: common datasets, task definitions, and evaluation protocol made competing systems directly comparable. That infrastructure turned object recognition from isolated demonstrations into a measurable research race.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” built on that setting by showing that region-based convolutional networks could be evaluated within the PASCAL VOC detection framework. In that lineage, VOC did not supply the CNN method itself; it supplied the benchmark and protocol that let R-CNN demonstrate region-based CNN detection gains in a form the field could trust and compare.

### 2014 → 2020: [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md) enables [Momentum Contrast for Unsupervised Visual Representation Learning](../paper/10_1109_cvpr42600_2020_00975.md)

> R-CNN demonstrated that deep convolutional features transfer effectively to detection, motivating MoCo to learn transferable visual representations without labels.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” helped establish that deep convolutional features learned for one visual setting could serve as strong, reusable representations for downstream tasks like detection and segmentation. In that sense, R-CNN made transferability itself a central design target: a vision system could benefit from rich feature hierarchies rather than relying only on task-specific hand-engineered representations.

“Momentum Contrast for Unsupervised Visual Representation Learning” follows that lineage by asking how such transferable visual representations might be learned without labels. MoCo’s contrastive framework is motivated by the same broader lesson R-CNN made influential: if deep visual features transfer effectively, then improving the way those features are learned, including through unsupervised pretraining, can expand the usefulness of representation learning across recognition tasks.
