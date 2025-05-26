import asyncio
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

GO_VERSION = "1.22.0"
GO_TAR = f"go{GO_VERSION}.linux-amd64.tar.gz"
GO_URL = f"https://go.dev/dl/{GO_TAR}"
NATS_VERSION = "2.11.3"
NATS_ZIP_URL = f"https://github.com/nats-io/nats-server/archive/refs/tags/v{NATS_VERSION}.zip"
NATS_DIR_NAME = f"nats-server-{NATS_VERSION}"

async def run_cmd(cmd, check=True):
    logging.info(f"Running: {cmd}")
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0 and check:
        raise RuntimeError(f"Command failed: {cmd}\n{stderr.decode()}")
    return stdout.decode()

def verify_go():
    return shutil.which("go") is not None

def verify_nats():
    return shutil.which("nats-server") is not None

async def install_go():
    if verify_go():
        logging.info("Go is already installed.")
        return
    await run_cmd(f"wget {GO_URL} -O /tmp/{GO_TAR}")
    await run_cmd("sudo rm -rf /usr/local/go")
    await run_cmd(f"sudo tar -C /usr/local -xzf /tmp/{GO_TAR}")
    go_path_line = "export PATH=$PATH:/usr/local/go/bin"
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc, "a") as f:
        f.write(f"\n{go_path_line}\n")
    os.environ["PATH"] += ":/usr/local/go/bin"
    logging.info("Go installed and path updated. Please run `source ~/.bashrc` manually or restart your shell.")

async def install_nats():
    if verify_nats():
        logging.info("NATS Server already installed.")
        return
    await run_cmd(f"wget {NATS_ZIP_URL} -O /tmp/nats.zip")
    await run_cmd("unzip /tmp/nats.zip -d /tmp/")
    os.chdir(f"/tmp/{NATS_DIR_NAME}")
    await run_cmd("go build -o nats-server")
    await run_cmd("sudo mv nats-server /usr/local/bin/")
    logging.info("NATS Server built and installed.")

async def main():
    await install_go()
    await install_nats()
    logging.info("Installation complete.")

if __name__ == "__main__":
    asyncio.run(main())
