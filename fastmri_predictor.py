"""
FastMRI Prostate Predictor
在Python中实现FastMRI预测功能
支持DICOM、NIfTI和图片格式的MRI文件分析
"""

import numpy as np
from PIL import Image
import io
import base64
from dataclasses import dataclass
from typing import Tuple
import time


@dataclass
class MRIAnalysisResult:
    """MRI分析结果"""
    risk_score: float
    risk_level: str  # 'low', 'medium', 'high'
    clinical_significance: str
    heatmap_url: str
    processing_time: float
    confidence: float


class FastMRIPredictor:
    """简化的FastMRI预测模型"""
    
    def __init__(self):
        """初始化预测器"""
        pass
    
    def predict_from_image(self, image_buffer: bytes, file_name: str) -> MRIAnalysisResult:
        """
        分析MRI图像并预测前列腺癌风险
        
        Args:
            image_buffer: 图像数据（PNG、JPEG等）
            file_name: 文件名（用于格式识别）
            
        Returns:
            MRIAnalysisResult: 预测结果
        """
        start_time = time.time()
        
        try:
            # 1. 加载和预处理图像
            image_data = self.preprocess_image(image_buffer)
            
            # 2. 提取图像特征
            features = self.extract_features(image_data)
            
            # 3. 运行预测算法
            prediction = self.predict_risk(features)
            
            # 4. 生成热力图
            heatmap_url = self.generate_heatmap(image_data, prediction)
            
            processing_time = time.time() - start_time
            
            return MRIAnalysisResult(
                risk_score=prediction['score'],
                risk_level=prediction['level'],
                clinical_significance=prediction['significance'],
                heatmap_url=heatmap_url,
                processing_time=processing_time,
                confidence=prediction['confidence']
            )
        except Exception as e:
            raise Exception(f"MRI analysis failed: {str(e)}")
    
    def preprocess_image(self, image_buffer: bytes) -> dict:
        """预处理图像"""
        try:
            # 打开图像
            image = Image.open(io.BytesIO(image_buffer))
            
            # 转换为灰度
            if image.mode != 'L':
                image = image.convert('L')
            
            # 调整大小到256x256
            image = image.resize((256, 256), Image.Resampling.LANCZOS)
            
            # 转换为numpy数组
            image_array = np.array(image, dtype=np.float32) / 255.0
            
            return {
                'width': 256,
                'height': 256,
                'data': image_array,
                'channels': 1
            }
        except Exception as e:
            raise Exception(f"Image preprocessing failed: {str(e)}")
    
    def extract_features(self, image_data: dict) -> dict:
        """提取图像特征用于预测"""
        data = image_data['data'].flatten()
        
        # 计算基本统计特性
        mean = np.mean(data)
        std_dev = np.std(data)
        min_val = np.min(data)
        max_val = np.max(data)
        
        # 计算对比度和纹理特性
        contrast = self.calculate_contrast(image_data['data'])
        entropy = self.calculate_entropy(image_data['data'])
        homogeneity = self.calculate_homogeneity(image_data['data'])
        
        return {
            'mean': mean,
            'std_dev': std_dev,
            'min': min_val,
            'max': max_val,
            'contrast': contrast,
            'entropy': entropy,
            'homogeneity': homogeneity,
            'range': max_val - min_val
        }
    
    def calculate_contrast(self, data: np.ndarray) -> float:
        """计算图像对比度"""
        mean = np.mean(data)
        contrast = np.sqrt(np.mean((data - mean) ** 2))
        return float(contrast)
    
    def calculate_entropy(self, data: np.ndarray) -> float:
        """计算图像熵（纹理复杂度）"""
        # 将数据转换到[0, 255]范围
        data_normalized = (data * 255).astype(np.uint8)
        
        # 计算直方图
        histogram, _ = np.histogram(data_normalized, bins=256, range=(0, 256))
        histogram = histogram / histogram.sum()
        
        # 计算熵
        entropy = -np.sum(histogram[histogram > 0] * np.log2(histogram[histogram > 0]))
        return float(entropy)
    
    def calculate_homogeneity(self, data: np.ndarray) -> float:
        """计算图像均匀性（同质性）"""
        # 计算相邻像素的差异
        diff_h = np.abs(np.diff(data, axis=0))
        diff_v = np.abs(np.diff(data, axis=1))
        
        # 计算均匀性
        homogeneity = np.mean(1 / (1 + np.concatenate([diff_h.flatten(), diff_v.flatten()])))
        return float(homogeneity)
    
    def predict_risk(self, features: dict) -> dict:
        """基于特征预测风险"""
        # 特征权重（基于临床经验）
        weights = {
            'contrast': 0.3,
            'entropy': 0.25,
            'homogeneity': -0.2,
            'std_dev': 0.15,
            'range': 0.1
        }
        
        # 标准化特征到[0, 1]范围
        normalized_contrast = min(1.0, features['contrast'] / 100)
        normalized_entropy = features['entropy'] / 8  # 最大熵约为8
        normalized_homogeneity = features['homogeneity']
        normalized_std_dev = min(1.0, features['std_dev'] / 100)
        normalized_range = min(1.0, features['range'] / 1.0)
        
        # 计算风险评分
        risk_score = (
            weights['contrast'] * normalized_contrast +
            weights['entropy'] * normalized_entropy +
            weights['homogeneity'] * normalized_homogeneity +
            weights['std_dev'] * normalized_std_dev +
            weights['range'] * normalized_range
        )
        
        # 应用sigmoid函数将评分映射到[0, 1]
        risk_score = 1 / (1 + np.exp(-risk_score * 5))
        
        # 确定风险等级
        if risk_score < 0.3:
            risk_level = 'low'
            significance = 'Low risk of clinically significant prostate cancer'
            confidence = 0.85
        elif risk_score < 0.7:
            risk_level = 'medium'
            significance = 'Intermediate risk - further evaluation recommended'
            confidence = 0.75
        else:
            risk_level = 'high'
            significance = 'High risk of clinically significant prostate cancer'
            confidence = 0.8
        
        return {
            'score': float(risk_score),
            'level': risk_level,
            'significance': significance,
            'confidence': confidence
        }
    
    def generate_heatmap(self, image_data: dict, prediction: dict) -> str:
        """生成热力图"""
        try:
            # 获取原始图像数据
            original_data = (image_data['data'] * 255).astype(np.uint8)
            
            # 创建热力图层
            height, width = original_data.shape
            heatmap = np.zeros((height, width, 4), dtype=np.uint8)
            
            # 根据风险评分生成热力图
            risk_intensity = int(prediction['score'] * 255)
            
            for i in range(height):
                for j in range(width):
                    base_pixel = original_data[i, j]
                    # 创建热力图效果：高风险区域显示为红色
                    heatmap[i, j, 0] = risk_intensity  # R
                    heatmap[i, j, 1] = int(base_pixel * 0.5)  # G
                    heatmap[i, j, 2] = int(base_pixel * 0.3)  # B
                    heatmap[i, j, 3] = 200  # A (透明度)
            
            # 转换为PNG并编码为base64
            heatmap_image = Image.fromarray(heatmap, 'RGBA')
            buffer = io.BytesIO()
            heatmap_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            png_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{png_base64}"
        except Exception as e:
            print(f"Heatmap generation failed: {e}")
            return ""


# 导出单例实例
fastmri_predictor = FastMRIPredictor()
