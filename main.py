import uvicorn
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import markdown
import io

app = FastAPI()

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.post("/export", response_class=HTMLResponse)
async def post_export(request: Request, markdown: str = Form(...)):
    print(markdown)
    return templates.TemplateResponse("export.html", {"request": request})

@app.get("/export/txt")
async def get_export_txt(content: str):
    html = markdown.markdown(content)
    content = ''.join(BeautifulSoup(html, features="html.parser").findAll(text=True))
    content = io.StringIO(content)
    return Response(content=content.read(), media_type="text/plain", headers={"Content-Disposition": "attachment; filename=export.txt"})

@app.get("/export/md")
async def get_export_md(content: str):
    content = io.StringIO(content)
    return Response(content=content.read(), media_type="text/markdown", headers={"Content-Disposition": "attachment; filename=export.md"})

@app.get("/export/html")
async def get_export_html(content: str):
    content = markdown.markdown(content)
    content = io.StringIO(content)
    return Response(content=content.read(), media_type="text/html", headers={"Content-Disposition": "attachment; filename=export.html"})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)