from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn

app = FastAPI()

def ordinal_date(date: datetime) -> str:
    day = date.day
    suffix = 'th' if 4 <= day <= 20 or day % 10 == 0 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return date.strftime(f"%B {day}{suffix}, %Y")

app.mount("/static", StaticFiles(directory="./templates/src"), name="static")
templates = Jinja2Templates(directory="templates")

templates.env.filters['ordinal_date'] = ordinal_date

blog_posts = {
    "posts": [
        {
            "id": 1,
            "name": "Exploring the World of Gems",
            "description": """Gems have captivated humanity for centuries, their dazzling colors and intrinsic value making them highly sought after. 
            In this post, we delve into the origins of some of the most famous gemstones, their formation processes, and how they are used in various cultural contexts. 
            From the sparkling beauty of diamonds to the deep, mysterious allure of sapphires, gems hold a special place in both history and modern times.""",
            "created_at": datetime.now()
        },
        {
            "id": 2,
            "name": "The Art of Cabochon Cutting",
            "description": "Cabochon cutting is a traditional lapidary technique that emphasizes the natural beauty of gemstones. Unlike faceting, which uses multiple flat surfaces to reflect light, cabochons are smooth, rounded shapes that display the stone's internal structure and color in a subtle yet striking way. This post covers the basics of cabochon cutting, from selecting the right stone to mastering the techniques needed to create a perfect cut.",
            "created_at": datetime.now()
        },
        {
            "id": 3,
            "name": "Uncovering the Secrets of Geology",
            "description": "Geology is the study of the Earth’s physical structure, its materials, and the processes that have shaped it over millions of years. Whether you are a rockhound looking for valuable minerals or simply fascinated by the planet’s history, geology provides a wealth of knowledge that can enrich your understanding of the world. This post explores the basics of geology, from the different types of rocks to the forces that cause earthquakes and volcanoes.",
            "created_at": datetime.now()
        },
        {
            "id": 4,
            "name": "Lapidary Arts: An Introduction",
            "description": "The world of lapidary arts is a rich and diverse field where creativity and skill come together to transform rough stones into beautiful works of art. Whether you are interested in cabochon cutting, faceting, or carving intricate designs, this post serves as an introduction to the basics of lapidary, the tools needed, and the various techniques that will help you get started in this exciting craft.",
            "created_at": datetime.now()
        },
        {
            "id": 5,
            "name": "Top 10 Gemstones to Look for in the Field",
            "description": "When you're out rockhounding, knowing which gemstones to look for can make all the difference. This post highlights the top 10 gemstones that are commonly found in nature, from amethyst to turquoise, and offers tips on how to identify them in the field. Whether you're a seasoned prospector or a beginner, these gemstones should be on your radar during your next rockhounding adventure.",
            "created_at": datetime.now()
        }
    ]
}

@app.get("/home", response_class=HTMLResponse)
async def view_home(request: Request):
    return templates.TemplateResponse(
        "index.html",context= {"request": request, "posts": blog_posts["posts"]}
    )

@app.get("/posts/{id}", response_class=HTMLResponse)
async def view_details(request: Request, id: int):

    post = next((p for p in blog_posts["posts"] if p["id"] == id), None)
    
    if post is None:
        return templates.TemplateResponse("404.html", {"request": request})
    
    return templates.TemplateResponse(
        "post-detail.html", context={"request": request, "post": post}
    )
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
