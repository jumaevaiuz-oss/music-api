from fastapi import FastAPI
from ytmusicapi import YTMusic
import uvicorn

app = FastAPI()
yt = YTMusic()

@app.get("/search")
def search(q: str, limit: int = 5):
    try:
        results = yt.search(q, filter="songs", limit=limit)
        tracks = []
        for item in results:
            if item.get("videoId"):
                tracks.append({
                    "title": item.get("title", ""),
                    "artist": item.get("artists", [{}])[0].get("name", "") if item.get("artists") else "",
                    "duration": item.get("duration", ""),
                    "videoId": item.get("videoId", ""),
                    "thumbnail": item.get("thumbnails", [{}])[-1].get("url", "") if item.get("thumbnails") else "",
                    "url": f"https://www.youtube.com/watch?v={item.get('videoId', '')}"
                })
        return {"success": True, "results": tracks}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def root():
    return {"status": "Music API ishlayapti!"}
