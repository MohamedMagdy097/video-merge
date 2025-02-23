def start():
    import subprocess

    subprocess.run(
        "uvicorn video_merge:app --host 0.0.0.0 --port 8000 --loop asyncio",
        shell=True,
    )

def dev():
    import subprocess

    subprocess.run(args="fuser -k 8000/tcp", shell=True)
    subprocess.run(
        args="uvicorn video_merge:app --reload --host 0.0.0.0 --port 8000 --loop asyncio",
        shell=True,
    )

def dev_win():
    import subprocess

    subprocess.run(
        args="uvicorn video_merge:app --reload --host 0.0.0.0 --port 8000 --loop asyncio",
        shell=True,
    )
