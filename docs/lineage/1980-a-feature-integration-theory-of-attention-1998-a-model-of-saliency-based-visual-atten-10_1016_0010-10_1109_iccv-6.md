---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2023
  Segment Anything
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1109/iccv51070.2023.00371
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2023 Segment Anything

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2016** — [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)
1. **2023** — [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception.

“A feature-integration theory of attention” (1980) framed visual attention as the process that binds separately registered features into coherent object perception. That idea made it natural to think of early vision as operating over distinct feature maps, with attention selecting or integrating information across them rather than treating the visual field as already object-complete.

“A model of saliency-based visual attention for rapid scene analysis” (1998) built in that lineage by formalizing how separate visual feature channels could contribute to a saliency representation that guides attention through a scene. In this sense, feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception, giving later computational work a conceptual bridge from feature-specific coding to attentional selection.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based attention supplied the selective visual-processing idea echoed by cascade-style focus on promising image regions in real-time face detection.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision as selective processing: instead of treating every part of a scene with equal priority, an attention mechanism can bias computation toward regions that appear more promising or informative.

“Robust Real-Time Face Detection” reflects a different but related engineering instinct. Its cascade-style detector rapidly rejects unlikely image regions and concentrates later, more expensive processing on candidates that remain plausible. The lineage is not that the face detector directly implements the 1998 saliency model, but that saliency-based attention supplied a broader selective visual-processing idea: real-time vision becomes practical when computation is focused on promising regions rather than spent uniformly across the whole image.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Viola-Jones showed that object categories could be detected efficiently with learned visual features, motivating the benchmarked detection task in Pascal VOC.

“Robust Real-Time Face Detection” made object detection feel like an empirical machine-learning problem rather than only a hand-engineered vision pipeline. Viola-Jones showed that a visual category could be detected efficiently using learned features, a boosted cascade, and a clear evaluation target: find instances of an object class in images fast enough to matter in practice.

That success helped set the stage for the Pascal VOC Challenge’s benchmarked detection task. VOC broadened the question from faces to many everyday object categories, but it inherited the same framing: detection systems should be trained, run on shared image data, and compared under common protocols. In that lineage, Viola-Jones was not a direct VOC baseline so much as a proof that learned visual features could make category-level detection a central, measurable challenge for computer vision.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)

> PASCAL VOC established object-recognition benchmarks and evaluation practices that helped measure ResNet's deep convolutional image classification gains.

“The Pascal Visual Object Classes (VOC) Challenge” helped turn object recognition into a measurable, comparable research problem. By establishing shared benchmark tasks and evaluation practices, PASCAL VOC gave the vision community a common way to judge whether new recognition systems were actually improving, rather than merely working on isolated datasets or demos.

That benchmarking culture enabled later deep-learning work such as “Deep Residual Learning for Image Recognition” to be understood as a concrete advance in convolutional image recognition. ResNet’s contribution was not just a new architecture in the abstract; its gains could be situated against established evaluation norms for object and image recognition that challenges like PASCAL VOC had helped normalize.

### 2016 → 2023: [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> ResNet's residual connections enabled very deep visual backbones that Segment Anything uses for scalable image feature extraction.

“Deep Residual Learning for Image Recognition” made it practical to train much deeper visual networks by using residual connections, which let layers learn refinements rather than entirely new transformations. That design became a foundation for modern visual backbones: deep, scalable feature extractors that can support increasingly broad recognition and perception tasks.

“Segment Anything” builds on that lineage by relying on powerful visual feature extraction at scale. The key enabling relationship is that ResNet’s residual connections helped establish the deep-backbone paradigm that later segmentation systems could use: first compute rich image features, then apply task-specific machinery for producing masks. In this sense, ResNet did not directly solve promptable segmentation, but it enabled the depth and reliability of visual representations that systems like Segment Anything depend on.
