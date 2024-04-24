from io import BytesIO
import io
import os
from fastapi import FastAPI, Request, Response, UploadFile, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from typing import List
from PIL import Image
import requests
from surya.ocr import run_ocr
from surya.model.detection import segformer
from surya.model.recognition.model import load_model
from surya.model.recognition.processor import load_processor
from surya.postprocessing.text import draw_text_on_image
from surya.input.load import load_from_folder

app = FastAPI()


@app.post('/upload')
async def upload(files: List[UploadFile]):
    for file in files:
        try:
            contents = await file.read()
            with open(f'images/{file.filename}', 'wb') as image:
                image.write(contents)
                
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='There was an error uploading the file(s)',
            )
        finally:
            await file.close()

    return {'message': f'Successfuly uploaded {[file.filename for file in files]}'}  

@app.post('/ocr')
async def ocr():
    file_path = 'images'
    result_path = 'results'
    result_path_list = []
    images, names = load_from_folder(file_path)
    image_langs = ["en","zh"] # Replace with your languages
    det_processor, det_model = segformer.load_processor(), segformer.load_model()
    rec_model, rec_processor = load_model(), load_processor()
    predictions = run_ocr(images, [image_langs], det_model, det_processor, rec_model, rec_processor)
    # draw the image by predictions content
    for idx, (name, image, pred, langs) in enumerate(zip(names, images, predictions, image_langs)):
        bboxes = [l.bbox for l in pred.text_lines]
        pred_text = [l.text for l in pred.text_lines]
        page_image = draw_text_on_image(bboxes, pred_text, image.size, langs, has_math="_math" in langs)
        page_image.save(os.path.join(result_path, f"{name}_{idx}_text.png"))
        result_path_list.append(os.path.join(result_path, f"{name}_{idx}_text.png"))

    return {'message': predictions, 'result_path_list': result_path_list}

@app.get('/results')
async def get_images(image_path):
    print(image_path)
    # image = '1000003081_01_text.png'
    # image_path = os.path.join('results/', image_path)
    return FileResponse(image_path, media_type="image/png")
# Access the form at 'http://127.0.0.1:8000/' from your browser
@app.get('/')
async def main():
    content = '''
    <body>
    <form action='/upload' enctype='multipart/form-data' method='post'>
    <input name='files' type='file' multiple>
    <input type='submit'>
    </form>
    <form action="/ocr" method="post">
    <input type="submit" value="ocr" />
    </form>
    <form action="/results" method="get">
    <input type="input" name='image_path' value="show results" />
    </form>
    </body>
    '''
    return HTMLResponse(content=content)