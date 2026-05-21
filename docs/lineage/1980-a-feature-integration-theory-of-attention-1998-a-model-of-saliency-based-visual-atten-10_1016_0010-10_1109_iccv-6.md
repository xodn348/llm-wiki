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

> Feature-integration theory linked attention to basic visual feature maps, which Itti, Koch, and Niebur computationalized as saliency maps for rapid scene analysis.

“A feature-integration theory of attention” framed visual attention as operating over separable basic features, with attention binding those features into coherent perceived objects. That gave later researchers a conceptual bridge between early visual feature processing and selective attention: attention was not just a vague cognitive spotlight, but something tied to organized feature representations.

“A model of saliency-based visual attention for rapid scene analysis” computationalized that lineage. Itti, Koch, and Niebur took the feature-map idea into an explicit model of visual saliency, combining basic visual feature maps into saliency maps that could guide rapid scene analysis. In that sense, Treisman and Gelade supplied the attentional architecture, while the 1998 model turned a related feature-map framework into a working computational account of where attention is likely to go.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based rapid scene analysis reinforced the idea of fast attentional feature selection that Viola-Jones implemented through efficient visual features.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision as fast, selective processing: scenes could be scanned by prioritizing salient low-level features before deeper interpretation. Its importance here is not that it solved face detection, but that it reinforced an attentional framing in which efficient feature selection is central to rapid visual analysis.

“Robust Real-Time Face Detection” carried that pressure for speed into a practical detection system. Viola-Jones used simple visual features in an efficient cascade, making face detection fast enough for real-time use. In lineage terms, saliency-based rapid scene analysis helped make fast attentional feature selection a credible design principle; Viola-Jones translated that principle into an engineered framework for selecting and applying efficient visual features to faces.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

“Robust Real-Time Face Detection” helped make sliding-window detection a practical, canonical pattern: scan an image at multiple positions and scales, score candidate windows, and return localized object instances. Its importance was not just that it detected faces, but that it showed object detection could be framed as repeatable window classification under real-time constraints, with evaluation tied to finding objects in images rather than merely recognizing whole scenes.

“The Pascal Visual Object Classes (VOC) Challenge” generalized that kind of detection problem beyond faces into a shared benchmark across many visual object classes. In that lineage, the face-detection work helped establish the methodological template, while PASCAL VOC supplied the broader task framing, datasets, and comparative challenge structure needed to turn object detection into a community-wide problem across categories.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)

> PASCAL VOC helped standardize visual-recognition benchmarking and detection tasks that residual networks later improved through very deep convolutional features.

“The Pascal Visual Object Classes (VOC) Challenge” helped turn visual recognition into a shared, comparable benchmark culture. By standardizing tasks such as object classification and detection, PASCAL VOC gave the field common problem definitions, datasets, and evaluation expectations, making progress in recognition systems easier to measure and discuss across research groups.

That benchmarking foundation enabled later architectures such as “Deep Residual Learning for Image Recognition” to be understood not just as deeper neural networks, but as improvements on established visual-recognition tasks. Residual networks advanced the convolutional feature-learning approach by making very deep models more trainable, and their impact was legible because challenges like PASCAL VOC had already shaped the community’s expectations for detection and recognition performance.

### 2016 → 2023: [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> Residual learning enabled very deep vision backbones, supporting SAM's high-capacity image encoder for general-purpose segmentation.

“Deep Residual Learning for Image Recognition” introduced residual learning as a practical way to train very deep vision networks, making depth itself a usable source of representational capacity rather than a training obstacle. In the historical arc of computer vision, that helped establish high-capacity backbones as standard infrastructure for recognition and downstream perception tasks.

“Segment Anything” builds in that lineage: its general-purpose segmentation system depends on a strong image encoder that can produce rich visual representations across diverse scenes and objects. The enabling relationship is not that ResNet directly solved segmentation prompting, but that residual learning helped make very deep, reliable vision backbones a foundation on which later large-scale systems like SAM could depend.
