

This is for my project on the study of **Causality Graph**.

In the folder /data_transformation_script you can find some Python script where I transformed the original data in JSONL to TSV (CSV with \tab).

The transformed data comes in two ways:

 1. The original data in TSV: source	target	weight
 2. The common causal relations in TSV: source	target	weight

You can find the data from Zenodo at: XXXXX. There you can find

 - the original CauseNet (causenet-full.jsonl), 14GB
 - the original CauseNet with higher precision (causenet-precision.jsonl), 990MB
 - the TSV file of the original CauseNet, 601MB
 - the file of the CauseNet as linked data (in HDT format), X MB
 - the mapping of the CauseNet to LOD-a-lot (in HDT), X MB
 - the refined CauseNet (in HDT format), Y MB

In the folder /data_analysis you can find some Python script about the analysis of the following aspects:

 - The script analysis of the degrees
 - The script about the analysis of SCC
 - The script about

> Written with [StackEdit](https://stackedit.io/).
