---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2023
  Segment Anything
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1109/iccv51070.2023.00371
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2023 Segment Anything

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2014** — [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)
1. **2023** — [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception.

“A feature-integration theory of attention” framed visual attention as a process that first represents basic visual features separately, then uses attention to bind or integrate them into coherent object perception. That gave later computational work a natural vocabulary for thinking about vision as multiple feature-specific channels whose outputs could be organized before full object recognition.

“A model of saliency-based visual attention for rapid scene analysis” builds in that lineage by treating visual attention as guided by feature maps that can be combined into an overall saliency representation. The enabling idea is not a specific quantitative result, but the conceptual architecture: separate feature maps become useful for explaining how attention selects parts of a scene. Feature-integration theory made it plausible to model rapid visual selection as arising from the combination of feature-based signals, which saliency models then operationalized computationally.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based attention supplied the selective visual-processing idea echoed by cascade-style focus on promising image regions in real-time face detection.

“A model of saliency-based visual attention for rapid scene analysis” framed vision as a selective process: rather than treating every part of an image with equal priority, a system could use saliency to guide attention toward regions likely to matter. Its influence here is conceptual, not a direct algorithmic handoff: it helped normalize the idea that efficient visual systems should focus computation on promising parts of a scene.

“Robust Real-Time Face Detection” carried that selective-processing logic into a practical detection pipeline. The cascade-style detector rapidly rejected unlikely image regions and reserved more computation for candidates that looked face-like. In that sense, saliency-based attention enabled a broader design pattern: real-time vision becomes feasible when the system allocates attention and computation unevenly, concentrating effort where the image is most promising.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Viola-Jones showed that object categories could be detected efficiently with learned visual features, motivating the benchmarked detection task in Pascal VOC.

*Robust Real-Time Face Detection* made object detection feel like a concrete, learnable computer vision task rather than only a handcrafted recognition problem. Its importance was not just that it focused on faces, but that it demonstrated an efficient detection pipeline built from learned visual features, capable of scanning images and returning localized category instances in real time.

That success helped shape the conditions for *The Pascal Visual Object Classes (VOC) Challenge*. If a system like Viola-Jones could detect one object category efficiently, the next scientific question was how to compare methods across many categories under shared data, annotations, and evaluation rules. Pascal VOC turned that motivation into a benchmarked detection task: not merely asking whether objects could be detected, but making object-category detection measurable, comparable, and central to visual recognition research.

### 2009 → 2014: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)

> Pascal VOC supplied the standardized object detection and segmentation benchmark on which R-CNN measured its region-based CNN improvements.

*The Pascal Visual Object Classes (VOC) Challenge* created a shared evaluation setting for object recognition, detection, and segmentation, giving researchers a common dataset, task definition, and benchmark culture. Its importance was not just the images or labels, but the standardization: methods could be compared against the same object categories and evaluation protocols rather than on isolated, custom experiments.

That infrastructure directly enabled *Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation* by giving R-CNN a recognized testbed for its region-based CNN approach. The 2014 paper could frame its contribution as an improvement in object detection and semantic segmentation because Pascal VOC supplied the established benchmark on which those improvements were measured. In that sense, VOC functioned as the experimental ground that made R-CNN’s architectural advance legible to the field.

### 2014 → 2023: [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> R-CNN showed that deep convolutional feature hierarchies could drive accurate object detection and segmentation, a foundation for Segment Anything's learned visual representations.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” helped establish that deep convolutional feature hierarchies could serve as powerful learned visual representations for recognition tasks beyond image classification. In R-CNN, those learned features were applied to object detection and segmentation settings, showing that representation learning from deep networks could materially improve how systems locate and delineate visual objects.

“Segment Anything” builds in a later era of much larger models and broader training regimes, but it inherits that central premise: accurate segmentation depends on learned visual representations that encode objects and regions at multiple levels of abstraction. The lineage is not that R-CNN directly supplied SAM’s architecture or training recipe, but that it helped make deep feature hierarchies a credible foundation for detection and segmentation systems.
