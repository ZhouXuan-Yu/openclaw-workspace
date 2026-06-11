"""
本地 OCR 工具 — 图片文字识别
用法: python ocr.py <图片路径>
"""
import sys
import json
import easyocr

def ocr_image(image_path, languages=['ch_sim', 'en']):
    """识别图片中的文字"""
    reader = easyocr.Reader(languages, gpu=False, verbose=False)
    results = reader.readtext(image_path)
    
    output = []
    for (bbox, text, confidence) in results:
        output.append({
            "text": text,
            "confidence": round(confidence, 3),
            "bbox": [[int(x), int(y)] for x, y in bbox]
        })
    
    return output

def ocr_summary(image_path):
    """识别并返回纯文字摘要"""
    results = ocr_image(image_path)
    lines = [r["text"] for r in results if r["confidence"] > 0.5]
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ocr.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if "--json" in sys.argv:
        results = ocr_image(image_path)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        text = ocr_summary(image_path)
        print(text)
