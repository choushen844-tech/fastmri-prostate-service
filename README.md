---
title: FastMRI Prostate Service
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.26.0
app_file: app.py
pinned: false
---

# FastMRI Prostate Cancer Risk Assessment

This is a Hugging Face Space for AI-powered prostate cancer risk assessment from MRI images using FastMRI technology.

## Features

- **Automated MRI Analysis**: Upload MRI images for instant analysis
- **Risk Stratification**: Get low, medium, or high risk classifications
- **Confidence Scoring**: Understand the model's confidence in its predictions
- **Visual Heatmaps**: See which areas of the image contribute to the risk assessment
- **Fast Processing**: Get results in seconds

## How to Use

1. Upload an MRI image (PNG, JPEG, DICOM, or NIfTI format)
2. Click "Analyze" to run the prediction
3. Review the risk score, level, and clinical significance
4. Check the heatmap visualization for spatial risk distribution

## Supported Formats

- PNG
- JPEG
- DICOM (as image)
- NIfTI (as image)

## Disclaimer

This tool is for research and educational purposes only. It should not be used for clinical diagnosis without professional medical review. Always consult with a qualified healthcare provider for medical decisions.

## Technical Details

- **Model**: FastMRI Prostate Predictor
- **Input**: MRI images (256x256 pixels after preprocessing)
- **Output**: Risk score (0-1), risk level, clinical significance, and heatmap
- **Framework**: Gradio + Python

## Citation

If you use this tool in your research, please cite:

```bibtex
@article{fastmri2020,
  title={FastMRI: A Publicly Available Raw k-Space and DICOM Image Dataset of Magnetic Resonance Imaging Experiments},
  author={Knoll, Florian and others},
  journal={Radiology: Artificial Intelligence},
  year={2020}
}
```

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please contact the developers.
