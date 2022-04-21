# GROUP: local
# CONDA: boost = 1.77.0
# CONDA: htslib = 1.14
# PIP: git+https://github.com/LaraFuhrmann/shorah@switch-to-poetry

import subprocess
from pathlib import Path


def main(fname_bam, fname_reference, fname_marker, dname_work):
    # TODO: it seems like the region input does not have any effect on the
    # windows that are created.
    # Compared to original shorah we need the argument -r for this version.
    region = "MasterSequence:210-3500"

    dname_work.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "shorah",
            "shotgun",
            "-b",
            fname_bam.resolve(),
            "-f",
            fname_reference.resolve(),
            "-r",
            region,
            "--inference",
            "mfa",
        ],
        cwd=dname_work,
        check=True,
    )

    (dname_work / "snv" / "SNVs_0.010000_final.vcf").rename(
        fname_marker.parent / "snvs.vcf"
    )


if __name__ == "__main__":
    main(
        Path(snakemake.input.fname_bam),
        Path(snakemake.input.fname_reference),
        Path(snakemake.output.fname_marker),
        Path(snakemake.output.dname_work),
    )
