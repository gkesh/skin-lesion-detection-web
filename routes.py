from quart import Blueprint, render_template, request
from quart_schema import validate_response

from models import Response
from uploads import images
from classifier import DenseNetClassifier

import os


web = Blueprint(
    "web",
    __name__,
    url_prefix="/"
)

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1"
)

classifier = DenseNetClassifier()

@web.get("/")
async def home():
    return await render_template('app.pug')

@api.get("/")
@validate_response(Response)
async def home() -> Response:
    return Response(
        success=True,
        filename="/app/routes.py",
        label="Welcome to HAM10000 Classifier API"
    )

@api.post("/classify")
@validate_response(Response)
async def classify() -> Response:
    if request.method == 'POST' and 'image' in (await request.files):
        filename = await images.save((await request.files)['image'])
        
        # Passing image to classifier
        label, confidence = classifier.preprocess(f"{os.getcwd()}/static/img/uploads/{filename}").classify()
                
        return Response(
            success=True,
            filename=filename,
            confidence=confidence,
            label=label
        )