"""
FastMRI Prostate Service - FastAPI Backend
前列腺癌MRI预测API服务
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from fastmri_predictor import fastmri_predictor, MRIAnalysisResult

# 创建FastAPI应用
app = FastAPI(
    title="FastMRI Prostate Service",
    description="AI-powered prostate cancer risk assessment from MRI images",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "FastMRI Prostate Service",
        "version": "1.0.0"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    预测前列腺癌风险
    
    Args:
        file: 上传的MRI图像文件
        
    Returns:
        JSON响应包含风险评分、风险等级、热力图等
    """
    try:
        # 验证文件
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # 读取文件内容
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # 获取文件名
        file_name = file.filename or "image.png"
        
        # 运行预测
        result: MRIAnalysisResult = fastmri_predictor.predict_from_image(content, file_name)
        
        # 返回JSON结果
        return {
            "status": "success",
            "risk_score": result.risk_score,
            "csPCa_probability": result.risk_score,  # 兼容旧API
            "risk_level": result.risk_level,
            "clinical_significance": result.clinical_significance,
            "confidence": result.confidence,
            "processing_time": result.processing_time,
            "heatmap": result.heatmap_url,
            "heatmap_url": result.heatmap_url,
            "message": result.clinical_significance,
            "file_name": file_name
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


@app.post("/predict-url")
async def predict_from_url(request_data: dict):
    """
    从URL预测前列腺癌风险
    
    Args:
        request_data: 包含file_url的JSON对象
        
    Returns:
        JSON响应包含风险评分、风险等级、热力图等
    """
    try:
        file_url = request_data.get("file_url")
        if not file_url:
            raise HTTPException(status_code=400, detail="file_url is required")
        
        # 从URL下载文件
        import requests
        response = requests.get(file_url, timeout=30)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download file: {response.status_code}")
        
        content = response.content
        file_name = file_url.split('/')[-1] or "image.png"
        
        # 运行预测
        result: MRIAnalysisResult = fastmri_predictor.predict_from_image(content, file_name)
        
        # 返回JSON结果
        return {
            "status": "success",
            "risk_score": result.risk_score,
            "csPCa_probability": result.risk_score,
            "risk_level": result.risk_level,
            "clinical_significance": result.clinical_significance,
            "confidence": result.confidence,
            "processing_time": result.processing_time,
            "heatmap": result.heatmap_url,
            "heatmap_url": result.heatmap_url,
            "message": result.clinical_significance,
            "file_url": file_url
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/")
async def root():
    """根端点 - 返回API信息"""
    return {
        "name": "FastMRI Prostate Service",
        "version": "1.0.0",
        "description": "AI-powered prostate cancer risk assessment from MRI images",
        "endpoints": {
            "health": "/health",
            "predict": {
                "method": "POST",
                "path": "/predict",
                "description": "Upload an MRI image file for analysis"
            },
            "predict_from_url": {
                "method": "POST",
                "path": "/predict-url",
                "description": "Analyze an MRI image from a URL"
            },
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # 从环境变量获取端口，默认8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting FastMRI Prostate Service on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
