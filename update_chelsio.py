import glob
import os
import platform
import subprocess


# This script updates chelsio-related binaries and scripts we ship with TrueNAS
# Download the latest "Chelsio Unified Wire vx.y.z for Linux" from https://service.chelsio.com/ and place it here

BASE = "tools/chelsio_adapter_config_v4"


def update(src_directory, arch):
    dest_directory_common = "files/common"
    dest_directory_arch = f"files/{arch}"
    bin_suffix = "_arm" if arch == "arm64" else ""

    os.makedirs(f"{dest_directory_arch}/usr/sbin", exist_ok=True)
    os.makedirs(f"{dest_directory_common}/usr/local/libexec", exist_ok=True)
    os.makedirs(f"{dest_directory_common}/usr/lib/firmware/cxgb4/config", exist_ok=True)

    subprocess.check_call(
        f"cp {src_directory}/{BASE}/bin/new/chelsio_adapter_config.py {dest_directory_common}/usr/local/libexec",
        shell=True,
    )
    subprocess.check_call(
        f"cp {src_directory}/{BASE}/vpds/* {dest_directory_common}/usr/lib/firmware/cxgb4/config/",
        shell=True,
    )
    subprocess.check_call(
        f"mv {src_directory}/{BASE}/bin/t5seeprom_bins/t5seeprom{bin_suffix} {dest_directory_arch}/usr/sbin/t5seeprom",
        shell=True,
    )
    subprocess.check_call(
        f"mv {src_directory}/{BASE}/bin/t6seeprom_bins/t6seeprom{bin_suffix} {dest_directory_arch}/usr/sbin/t6seeprom",
        shell=True,
    )

if __name__ == "__main__":
    source = glob.glob("ChelsioUwire-*.tar.gz")[0]
    src_directory = source.removesuffix(".tar.gz")

    subprocess.check_call(["tar", "xf", source])
    try:
        update(src_directory, "amd64")
        update(src_directory, "arm64")
    finally:
        subprocess.check_call(["rm", "-rf", src_directory])
