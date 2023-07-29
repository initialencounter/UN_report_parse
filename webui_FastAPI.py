import uvicorn
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from main import pdf_parser
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    """
        This is a function that returns an HTML response.

        :return: The HTML response.
        :rtype: HTMLResponse
    """
    with open("templates/index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
        This is a function that returns a JSON response.

        :param file: The uploaded file.
        :type file: UploadFile
        :return: The JSON response.
        :rtype: dict
    """
    file_bytes = await file.read()
    data = pdf_parser(BytesIO(file_bytes))
    return data


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5001)
