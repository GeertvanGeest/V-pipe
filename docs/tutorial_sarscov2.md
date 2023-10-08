---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- markdownlint-configure-file { "MD010": { "ignore_code_languages" : [ "tsv", "bash" ] } } -->
# SARS-CoV-2 Tutorial

This tutorial shows the basics of how to interact with V-pipe.

For the purpose of this Tutorial, we will work with the master branch of V-pipe and use the _sars-cov-2_ virus base config which is adapted for the SARS-CoV-2 virus.

## Requirements

The tutorial assumes that you have [installed V-pipe using the installation tutorial](tutorial_0_install.md), and that the workflow is setup with the following structure:

```text
📁 [HOME]
└───📁vp-analysis
    ├───📁V-pipe      # V-pipe checked out from Github
    ├───📁Miniforge3  # bioconda + conda-forge + mamba + Snakemake
    ├───📁work        # work directories
    ├───📁work-tests  #  …
    └───📁 …          #  …
```

- `vp-analysis` is the main directory where we installed everything in the previous tutorial
- `Miniforge3` has dependencies to start using V-pipe (bioconda, conda-forge, mamba, snakemake)
- `V-pipe` is the directory with V-pipe's own code
- and for this tutorial we will create a directory like `work…`, which will hold the configuration and the sequencing data for our analysis.

## Organizing Data

V-pipe expects the input samples to be organized in a two-level hierarchy:

- At the first level, input files grouped by samples (e.g.: patients or biological replicates of an experiment).
- A second level for distinction of datasets belonging to the same sample (e.g.: sample dates).
- Inside that directory, the sub-directory raw_data holds the sequencing data in FASTQ format (optionally compressed with GZip).
- Paired-ended reads need to be in split files with `_R1` and `_R2` suffixes.


## Preparing a small dataset

You can run the first test on your workstation or a good laptop.

First, you need to prepare the data:

* For that test, you need to download the following runs from SRA: [SRR10903401](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR10903401) and [SRR10903402](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR10903402)

```bash
mkdir -p samples/SRR10903401/20200102/raw_data
cd samples/SRR10903401/20200102/raw_data
fasterq-dump --progress SRR10903401
cd -
```

```bash
mkdir -p samples/SRR10903402/20200102/raw_data
cd samples/SRR10903402/20200102/raw_data
fasterq-dump --progress SRR10903402
cd -
```

You then have to rename the files so that they have `_R1` and `_R2` suffixes:

```bash
mv samples/SRR10903401/20200102/raw_data/SRR10903401_1.fastq samples/SRR10903401/20200102/raw_data/SRR10903401_R1.fastq
mv samples/SRR10903401/20200102/raw_data/SRR10903401_2.fastq samples/SRR10903401/20200102/raw_data/SRR10903401_R2.fastq

mv samples/SRR10903402/20200102/raw_data/SRR10903402_1.fastq samples/SRR10903402/20200102/raw_data/SRR10903402_R1.fastq
mv samples/SRR10903402/20200102/raw_data/SRR10903402_2.fastq samples/SRR10903402/20200102/raw_data/SRR10903402_R2.fastq
```

The downloaded files should have the following structure:

```text
📁samples
├───📁SRR10903401
│   └───📁20200102
│       └───📁raw_data
│           ├───🧬SRR10903401_R1.fastq
│           └───🧬SRR10903401_R2.fastq
└───📁SRR10903402
    └───📁20200102
        └───📁raw_data
            ├───🧬SRR10903402_R1.fastq
            └───🧬SRR10903402_R2.fastq
```

You can display the directory structure with the following command on Linux (on Mac OS, use `find samples`)

```bash
tree samples
```


## Install V-pipe

## Install V-pipe

After [having installed V-pipe using the installation tutorial](tutorial_0_install.md), create a new working directory for this analysis:

```bash
cd vp-analysis

# create a new directory and initialise it
mkdir -p work_sarscov2
cd work_sarscov2
../V-pipe/init_project.sh

cd ../..
```


## Running V-pipe

Copy the samples directory you created in the step [Preparing a small](#preparing-a-small-dataset) dataset to this working directory. (You can display the directory structure with `tree samples` or `find samples`.)

```bash
mv samples vp-analysis/work_sarscov2/
```

Prepare V-pipe's configuration. You can find more information in [the documentation](https://github.com/cbg-ethz/V-pipe/blob/master/config/README.md). In your local V-pipe installation, you will also find an exhaustive manual about all the configuration options inside `config/config.html`.

```bash
cat <<EOT > vp-analysis/work_sarscov2/config.yaml
general:
    virus_base_config: 'sars-cov-2'

input:
    samples_file: samples.tsv

output:
    trim_primers: false
    # NOTE: set "snv" to "true" to run the tutorial. We left "false" so automated test doesn't take too much time on GitHub.
    snv: false
    local: false
    global: false
    visualization: false
    diversity: false
    QA: false
    upload: false
    dehumanized_raw_reads: false
EOT
```

Check what will be executed:

```bash
cd vp-analysis/work_sarscov2/
./vpipe --dryrun
cd ../..
```

As it is your first run of V-pipe, this will also generate the sample collection table. Check `samples.tsv` in your editor.

Note that the demo files you downloaded have reads of length 150 only. V-pipe’s default parameters are optimized for reads of length 250; add the third column in the tab-separated file:

```bash
cat <<EOT > vp-analysis/work_sarscov2/samples.tsv
SRR10903401	20200102	150
SRR10903402	20200102	150
EOT
```

**Tip:** Always check the content of the `samples.tsv` file.
If you didn’t use the correct structure, this file might end up empty or some entries might be missing.
You can safely delete it and re-run the `--dryrun` to regenerate it.

Run the V-pipe analysis (the necessary dependencies will be downloaded and installed in conda environments managed by snakemake):

```bash
cd vp-analysis/work_sarscov2/
./vpipe -p --cores 2
```


## Output

The section _output_ of the exhaustive configuration manual contains an overview of the output files.
The output of the SNV calling is aggregated in a standard [VCF](https://en.wikipedia.org/wiki/Variant_Call_Format) file, located in `results/`_​{hierarchy}​_`/variants/SNVs/snvs.vcf`, you can open it with your favorite VCF tools for visualisation or downstream processing.
It is also available in a tabular format in `results/​`_{hierarchy}​_`/variants/SNVs/snvs.csv`.

### Expected output

The small dataset that we used in this tutorial section has been analyzed by [doi:10.1093/nsr/nwaa036](https://doi.org/10.1093/nsr/nwaa036). The results of the original analysis (using bwa, samtools mpileup, and bcftools) are displayed in Table 2 in the article:

Using either the VCF or CSV files, compare with the results given out by V-pipe (with bwa and ShoRAH).

* For positions 19164 and 24323 of SRR10903401 and position 11563 of SRR10903402, we expect to see similar results in V-pipe.
* For the remaining positions (1821, 26314 and 26590 of SRR10903401), we expect that ShoRAH will consider the variants of poor quality and reject them because there is very little support ( <= than 5 reads supporting the alt).


## Swapping component

The default configuration uses ShoRAH to call the SNVs and to reconstruct the local (windowed) haplotypes.

Components can be swapped simply by changing the `config.yaml` file. For example to call SNVs using lofreq:

```yaml
general:
  snv_caller: lofreq
```


## Cluster deployment

It is possible to ask snakemake to submit jobs on a cluster using the batch submission command-line interface of your cluster.

The opensource platform SLURM by SchedMD is one of the popular systems you might find on clusters (Others include LSF, Grid Engine).

The most user friendly way to submit jobs to the cluster is using a special _snakemake profile_.
[smk-simple-slurm](https://github.com/jdblischak/smk-simple-slurm) is a profile that works well in our experience with SLURM (for other platforms see suggestions in [the snakemake-profil documentation](https://github.com/snakemake-profiles/doc)).

```bash
cd vp-analysis/
# download the profile
git clone https://github.com/jdblischak/smk-simple-slurm.git
# edit simple/config.yaml and either comment out the partition and qos or adapt to your local HPC
cat > smk-simple-slurm/simple/config.yaml <<EOT
cluster:
  mkdir -p logs/{rule} &&
  sbatch
    --cpus-per-task={threads}
    --mem={resources.mem_mb}
    --job-name=smk-{rule}-{wildcards}
    --output=logs/{rule}/{rule}-{wildcards}-%j.out
  #--partition={resources.partition}
  #--qos={resources.qos}
default-resources:
  #- partition=<name-of-default-partition>
  #- qos=<name-of-quality-of-service>
  - mem_mb=1000
restart-times: 3
max-jobs-per-second: 10
max-status-checks-per-second: 1
local-cores: 1
latency-wait: 60
jobs: 500
keep-going: True
rerun-incomplete: True
printshellcmds: True
scheduler: greedy
use-conda: True
EOT
cd work_sarscov2/
./vpipe --dry-run --profile ../smk-simple-slurm/simple/ --jobs 100
cd ../..
```

Snakemakes documentation [introduces the key concepts used in profile](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).
Check also [the other options for running snakemake on clusters](https://snakemake.readthedocs.io/en/stable/executing/cli.html#CLUSTER) if you need more advanced uses.

### Dependencies downloading on the cluster

In addition, Snakemake has [parameters for conda](https://snakemake.readthedocs.io/en/stable/executing/cli.html#CONDA) that can help management of dependencies:

- using `-conda-create-envs-only` enables to download the dependencies only without running the pipeline itself. This is very useful if the compute nodes of your cluster are not allowed internet access.
- using `--conda-prefix=`_{DIR}_ stores the conda environments of dependencies in a common directory (thus possible to share and re-use between multiple instances of V-pipe).

```bash
cd  vp-analysis/work_sarscov2/
# First download all bioconda dependencies ahead of time
./vpipe --conda-prefix ../snake-envs --cores 1 --conda-create-envs-only
# And then run on the cluster, the compute node will not need to download anything
./vpipe --dry-run --conda-prefix ../snake-envs --profile ../smk-simple-slurm/simple/ --jobs 100
cd ../..
```

When using V-pipe in production environments, plan the installer's `-p` prefix and `-w` working and snakemake's `--conda-prefix` environments directories according to the cluster quotas and time limits.
For example, consider using `${SCRATCH}` and only move the content of the `results/` directory to long-term storage.
