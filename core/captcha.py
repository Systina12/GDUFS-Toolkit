import ddddocr

ocr = ddddocr.DdddOcr()

def recognize_captcha(image_bytes):
    return ocr.classification(image_bytes)
