

This is for my project on the research of refining the **Causality Graph**.
I used CauseNet (https://causenet.org/).

In the folder /data_transformation_script you can find some Python script where I transformed the original data in JSONL to TSV (CSV with \tab).

The transformed data comes in two ways:

 1. The original data in TSV: source	target	weight
 2. The common causal relations in TSV: source	target	weight

You can find the data from Zenodo at: XXXXX. There you can find

 - the original CauseNet (causenet-full.jsonl), 14GB (also see the website: https://causenet.org/)
 - the original CauseNet with higher precision (causenet-precision.jsonl), 990MB (also see the website: https://causenet.org/)
 - the TSV file of the original CauseNet (causenet-full-without-NUL.tsv), 601MB
 - the file of the CauseNet as linked data (in HDT format), X MB
 - the mapping of the CauseNet to LOD-a-lot (in HDT), X MB
 - the CommonCauseNet (in HDT format), Y MB
 - the refined CommonCauseNet (in HDT format), Y MB

You can also find the following data there:
 - all the removed reflexive links (in TSV format), Z MB
 - the automatically removed links (with some manual evaluation, in TSV format), Z MB
 - the detected links in 10 files (2 files each round, 5 rounds).
 - the removed links of CommonCauseNet (in TSV format), Y MB
 - the removed links of CauseNet (in TSV format), Y MB

In the folder /data_analysis you can find some Python script about the analysis of the following aspects:

 - The script analysis of the degrees
 - The script about the analysis of SCC
 - The script about

> Written with [StackEdit](https://stackedit.io/).
