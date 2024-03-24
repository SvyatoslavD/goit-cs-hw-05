import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile


async def copy_file(file_path: AsyncPath, destination: AsyncPath):
    ext = file_path.suffix[1:]
    target_folder = destination / ext
    await target_folder.mkdir(exist_ok=True)
    await copyfile(file_path, target_folder / file_path.name)
    print(f"File {file_path} copied to {target_folder / file_path.name}")


async def read_folder(source: AsyncPath, destination: AsyncPath):
    async for file_path in source.glob('**/*'):
        if await file_path.is_dir():
            await read_folder(file_path, destination)
        else:
            await copy_file(file_path, destination)


async def main(src_path, dst_path):
    src = AsyncPath(src_path)
    dst = AsyncPath(dst_path)

    result = await src.is_dir()
    if not result:
        print(f"Source {src_path} does not exist, aborting..")
        raise ValueError("Fatal Error")

    result = await dst.is_dir()
    if not result:
        print(f"Destination {dst_path} does not exist, creating the output folder")
        await dst.mkdir(exist_ok=True)

    await read_folder(src, dst)


parser = argparse.ArgumentParser(description="Task 1")
parser.add_argument("--src", type=str, required=True, help="source")
parser.add_argument("--dst", type=str, required=True, help="destination")

args = parser.parse_args()

src_path = args.src
dst_path = args.dst

asyncio.run(main(src_path, dst_path))
