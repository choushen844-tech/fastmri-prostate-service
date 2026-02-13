"""
FastMRI Prostate Service - FastAPI版本
用于前列腺癌MRI预测
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import io
import base64
from PIL import Image
import numpy as np
from fastmri_predictor import FastMRIPredictor

# 初始化FastAPI应用
app = FastAPI(title="FastMRI Prostate Service")

# 初始化预测器
predictor = FastMRIPredictor()

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "FastMRI Prostate Service",
        "version": "1.0.0"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    预测前列腺癌风险
    
    参数:
        file: MRI图像文件 (PNG, JPG, DICOM等)
    
    返回:
        {
            "success": bool,
            "risk_score": float (0-100),
            "risk_level": str ("low", "medium", "high"),
            "heatmap": str (base64编码的热力图),
            "message": str
        }
    """
    try:
        # 读取文件
        contents = await file.read()
        
        # 验证文件
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # 进行预测
        result = predictor.predictFromImage(
            contents,
            file.filename
        )
        
        # 返回结果
        return JSONResponse(content={
            "success": True,
            "risk_score": result.get("risk_score", 0),
            "risk_level": result.get("risk_level", "unknown"),
            "heatmap": result.get("heatmap", ""),
            "message": result.get("message", "Prediction completed")
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Prediction failed"
            }
        )

@app.post("/predict-url")
async def predict_url(image_url: str):
    """
    通过URL预测前列腺癌风险
    
    参数:
        image_url: MRI图像的URL
    
    返回:
        预测结果JSON
    """
    try:
        import requests
        
        # 下载图像
        response = requests.get(image_url, timeout=30)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image")
        
        # 进行预测
        result = predictor.predictFromImage(
            response.content,
            image_url.split('/')[-1]
        )
        
        # 返回结果
        return JSONResponse(content={
            "success": True,
            "risk_score": result.get("risk_score", 0),
            "risk_level": result.get("risk_level", "unknown"),
            "heatmap": result.get("heatmap", ""),
            "message": result.get("message", "Prediction completed")
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Prediction failed"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
