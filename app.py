"""
FastMRI Prostate Service
Gradio应用用于前列腺癌MRI预测
"""

import gradio as gr
import json
from fastmri_predictor import fastmri_predictor, MRIAnalysisResult


def predict_prostate_cancer(image_file):
    """
    预测前列腺癌风险
    
    Args:
        image_file: 上传的图像文件
        
    Returns:
        tuple: (结果字符串, 热力图)
    """
    try:
        if image_file is None:
            return "Please upload an MRI image", None
        
        # 读取图像文件
        with open(image_file, 'rb') as f:
            image_buffer = f.read()
        
        # 获取文件名
        file_name = image_file.split('/')[-1] if isinstance(image_file, str) else 'image.png'
        
        # 运行预测
        result: MRIAnalysisResult = fastmri_predictor.predict_from_image(image_buffer, file_name)
        
        # 格式化结果
        result_text = f"""
## FastMRI Prostate Analysis Results

**Risk Score:** {result.risk_score:.1%}

**Risk Level:** {result.risk_level.upper()}

**Clinical Significance:** {result.clinical_significance}

**Confidence:** {result.confidence:.1%}

**Processing Time:** {result.processing_time:.2f} seconds

---

### Interpretation:
- **Low Risk (<30%):** Low probability of clinically significant prostate cancer. Routine follow-up recommended.
- **Medium Risk (30-70%):** Intermediate risk. Further evaluation and specialist consultation recommended.
- **High Risk (>70%):** High probability of clinically significant prostate cancer. Urgent specialist evaluation recommended.
"""
        
        # 如果有热力图，返回热力图
        heatmap = None
        if result.heatmap_url:
            # 从base64数据URL创建图像
            import base64
            import io
            from PIL import Image
            
            # 提取base64数据
            base64_data = result.heatmap_url.split(',')[1]
            image_data = base64.b64decode(base64_data)
            heatmap = Image.open(io.BytesIO(image_data))
        
        return result_text, heatmap
    
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(error_msg)
        return error_msg, None


# 创建Gradio界面
with gr.Blocks(title="FastMRI Prostate Service", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏥 FastMRI Prostate Cancer Risk Assessment
    
    Upload an MRI image to get an AI-powered risk assessment for clinically significant prostate cancer.
    
    **Supported Formats:** PNG, JPEG, DICOM (as image), NIfTI (as image)
    
    **Disclaimer:** This tool is for research and educational purposes only. It should not be used for clinical diagnosis without professional medical review.
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Upload MRI Image")
            image_input = gr.File(
                label="Select MRI Image",
                file_count="single",
                file_types=["image"]
            )
            analyze_btn = gr.Button("Analyze", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### Results")
            result_output = gr.Markdown(label="Analysis Results")
    
    gr.Markdown("### Heatmap Visualization")
    heatmap_output = gr.Image(label="Risk Heatmap", type="pil")
    
    # 绑定按钮事件
    analyze_btn.click(
        fn=predict_prostate_cancer,
        inputs=[image_input],
        outputs=[result_output, heatmap_output]
    )
    
    # 示例
    gr.Examples(
        examples=[],
        inputs=[image_input],
        label="Examples (coming soon)"
    )
    
    gr.Markdown("""
    ---
    
    ### About FastMRI Prostate Service
    
    This service uses advanced image analysis techniques to assess the risk of clinically significant prostate cancer from MRI images.
    
    **Features:**
    - Automated MRI image analysis
    - Risk stratification (Low/Medium/High)
    - Confidence scoring
    - Visual heatmap generation
    
    **Important Notes:**
    - This is a research tool and should not replace professional medical diagnosis
    - Always consult with a qualified healthcare provider for medical decisions
    - Results should be interpreted in conjunction with clinical findings and other diagnostic tests
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
