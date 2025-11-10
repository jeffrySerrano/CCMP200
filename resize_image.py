import boto3
import os
from PIL import Image
import io
import urllib.parse

s3 = boto3.client('s3')
RESIZED_BUCKET = os.environ['RESIZED_BUCKET']

def lambda_handler(event, context):
    # Expect input: {"bucket":"...","key":"..."}
    bucket = event.get('bucket')
    key = event.get('key')
    if not bucket or not key:
        return {"status": "FAILURE", "error": "missing bucket/key"}

    try:
        obj = s3.get_object(Bucket=bucket, Key=urllib.parse.unquote_plus(key))
        img = Image.open(obj['Body'])
        img.thumbnail((128, 128))

        out = io.BytesIO()
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255,255,255))
            background.paste(img, mask=img.split()[-1])
            background.thumbnail((128,128))
            background.save(out, format='JPEG')
        else:
            img.save(out, format='JPEG')

        out.seek(0)
        resized_key = "thumb-" + key
        s3.put_object(Bucket=RESIZED_BUCKET, Key=resized_key, Body=out, ContentType='image/jpeg')
        return {"status":"SUCCESS", "resized_key": resized_key}
    except Exception as e:
        return {"status":"FAILURE", "error": str(e)}