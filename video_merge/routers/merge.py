from fastapi import (
    APIRouter,
    HTTPException
)
from pydantic import BaseModel
import aiohttp
import tempfile
from pathlib import Path
import os
import asyncio
from video_merge.deps.supabase import supabase

router = APIRouter(prefix="/merge", tags=["core"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


class VideoRequest(BaseModel):
    urls: list[str]

async def download_video(url: str, session: aiohttp.ClientSession) -> Path:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=400, detail=f"Failed to download {url}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                content = await response.read()
                tmp_file.write(content)
                return Path(tmp_file.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")
    


@router.post("/merge-videos")
async def merge_videos(request: VideoRequest):
    temp_files = []
    
    try:
        async with aiohttp.ClientSession() as session:
            # Download all videos concurrently
            download_tasks = [download_video(url, session) for url in request.urls]
            video_files = await asyncio.gather(*download_tasks)
            temp_files.extend(video_files)

            # Create input list for FFmpeg
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as list_file:
                list_content = "\n".join(f"file '{file}'" for file in video_files)
                list_file.write(list_content)
                list_path = Path(list_file.name)
                temp_files.append(list_path)

            # Create output file for merged video
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as merged_file:
                merged_path = Path(merged_file.name)
                temp_files.append(merged_path)
            print(merged_file.name)

            # Merge videos using FFmpeg
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(list_path),
                '-c', 'copy',
                str(merged_path),
                '-y'
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()

            print(stdout)
            
            if process.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"Video merge failed: {stderr.decode()}"
                )

            # Print all paths
            print("\nTemporary files created:")
            for i, file in enumerate(video_files, 1):
                print(f"Video {i}: {file}")
            print(f"Merged video: {merged_path}\n")

            supabase.storage.from_('vids').upload(str(merged_path), open(merged_path, 'rb'))
            # get public url from supabase
            public_url = supabase.storage.from_('vids').get_public_url(str(merged_path))
            print(public_url)

            return {
                "message": "Videos merged successfully",
                "merged_path": str(merged_path),
                "temp_files": [str(f) for f in temp_files],
                "public_url": public_url
            }
    except Exception as e:
                print(f"Error: {str(e)}")
            
    finally:
        # Cleanup all temporary files
        for f in temp_files:
            try:
                if f.exists():
                    os.unlink(f)
                    print(f"Deleted temporary file: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {str(e)}")

@router.post("/delete-temp-files")
async def delete_temp_files(filesPath: str):
    try:
        if filesPath.exists():
                    os.unlink(filesPath)
    except Exception as e:
                print(f"Error deleting {filesPath}: {str(e)}")


@router.post("/process-videos")
async def process_videos(request: VideoRequest):
    temp_files = []
    
    try:
        async with aiohttp.ClientSession() as session:
            # Download both videos concurrently
            file1 = await download_video(request.urls[0], session)
            file2 = await download_video(request.urls[1], session)
            
            temp_files = [file1, file2]
            
            # Print paths (you could add actual processing here)
            print(f"Temporary files created:")
            print(f"1. {file1}")
            print(f"2. {file2}")
            
            return {"message": "Videos processed successfully"}
            
    finally:
        # Cleanup temporary files
        for f in temp_files:
            try:
                if f.exists():
                    os.unlink(f)
                    print(f"Deleted temporary file: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {str(e)}")