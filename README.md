# Baher: DeepSeek-Powered Python Code Analysis System

## Abstract

**Baher Code Analyzer** is an end-to-end web-based static analysis system designed for automated code explanation, algorithmic optimization, software quality auditing, and defect detection in Python source code. Powered by a quantized **DeepSeek GGUF** model and orchestrated via **FastAPI** and **llama-cpp-python**, the application leverages **NVIDIA CUDA** acceleration to achieve real-time, low-latency token streaming over HTTP.

---

## Core Features

- **Code Explanation**: Generates structural summaries and step-by-step execution flow breakdowns.
- **Performance Optimization**: Assesses computational efficiency and provides refactored implementations with time and space complexity analysis.
- **Software Quality Audit**: Performs static code reviews adhering to PEP 8 standards, maintainability guidelines, and clean code principles.
- **Defect & Bug Detection**: Identifies syntax errors, runtime vulnerabilities, and edge-case execution faults.
- **Real-Time Token Streaming**: Implements chunked HTTP streaming to render output tokens interactively via JavaScript `ReadableStream`.

---

## System Architecture & Technical Specifications

| Component | Specification |
| :--- | :--- |
| **Language Model** | DeepSeek GGUF (`Ishammari77/my-deepseek-model`) |
| **Inference Engine** | `llama-cpp-python` (Compiled with CUDA support: `GGML_CUDA=on`) |
| **Backend API** | FastAPI / Uvicorn ASGI Server |
| **Frontend Stack** | HTML5, Modern CSS3, Asynchronous JavaScript (`Fetch API`) |
| **Containerization** | Docker (Base Image: NVIDIA CUDA 12.1.1 Ubuntu 22.04) |
| **Deployment Hardware** | Hugging Face Spaces (NVIDIA T4 GPU, 16GB VRAM) |

---

## Repository Structure

```text
.
├── Dockerfile          # CUDA-enabled multi-stage Docker configuration
├── app.py              # FastAPI server, inference routing, and streaming logic
├── index.html          # Web interface and client-side streaming handler
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
