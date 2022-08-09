import io
import os
import torchvision.transforms as transforms
from PIL import Image
import torch
import numpy as np

from flask import Blueprint, render_template, request, jsonify, redirect
from api.models.yolo_nano import YOLONano
from api.utils.utils import non_max_suppression
from api.utils.gdrive_download import gdrive_download
import gdown

predict = Blueprint('predict', __name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = YOLONano(num_classes=10, image_size=416)

os.makedirs("weights", exist_ok=True)
_model_url = "https://drive.google.com/uc?id=129r1Giqog2UE-AAvxeRVD8GjFutMsXBj"
_model_file = "weights/best_model.pth"
gdrive_download(_model_url, _model_file)

checkpoint = torch.load("weights/best_model.pth", map_location=device)
model.load_state_dict(checkpoint["state_dict"])
model.eval()

with open("data/label.txt") as f:
    imagenet_class_index = [i.strip() for i in f.readlines()]

def _transform_image(image_bytes):
    all_transforms = transforms.Compose([
        transforms.Resize((416, 416)),
        transforms.ToTensor(),
        ])
    image = Image.open(io.BytesIO(image_bytes))
    return all_transforms(image).unsqueeze(0)

def _get_prediction(image_bytes):

    tensor = _transform_image(image_bytes=image_bytes)
    with torch.no_grad():
        detections = model.forward(tensor)
    detections = non_max_suppression(detections, conf_thres=0.5, nms_thres=0.4)[0]
    detections = detections.numpy()
    label = detections[:,6].astype(np.int64).tolist()
    bbox = detections[:,:4].astype(np.int64).tolist()
    print(np.round((detections[:,4] * detections[:,5]), 3).tolist())
    score = [round(i, 3) for i in (detections[:,4] * detections[:,5]).tolist()]
    dict = {"label":label, "bbox":bbox, "score":score}
    return dict

@predict.route("/", methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        try:
            if ("file" not in request.files) or ("" == request.files["file"].filename):
                return jsonify(status="error", message='No images selected for upload')
            file = request.files['file']
            if not file.mimetype=="image/jpeg":
                return jsonify(status="error", message='Only jpg files are supported')
            img_bytes = file.read()
            dict = _get_prediction(image_bytes=img_bytes)
            return jsonify(status="ok", result=dict)
        except:
            return jsonify(status="error", message='An unexpected error has occurred')

    html = \
    """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>

        <form class="form-signin" method=post enctype=multipart/form-data>
            <h1 class="h3 mb-3 font-weight-normal">Upload any image</h1>
            <input type="file" name="file" class="form-control-file" id="inputfile">
            <br/>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
        </form>

    </body>
    </html>
    """
    return html
