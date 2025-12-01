# 💡 Adapti-Creative AI Studio: Real-Time Creative Compliance Engine

### Tesco Retail Media InnovAItion Jam - Prototype Submission

This project demonstrates a functionally complete Minimum Viable Product (MVP) of the **Intelligent Creative Guardrail™**—a Generative AI/CV solution designed to ensure advertising creatives comply with detailed retailer guidelines in real-time.

---

## 🎯 Core Innovation

The core feature is the **Intelligent Creative Guardrail™**, which integrates Computer Vision (CV) principles to perform mandatory positional and size checks *before* the ad is submitted. This eliminates costly human review cycles and reduces ad rejection risk.

## ✨ Implemented Functionality (MVP)

1.  **Real-Time Compliance Check (CV):** Validates the simulated position of the logo against minimum margin and quadrant rules. (Demonstrated by the dynamic score change: 98% Pass / 45% Fail).
2.  **File Optimization (<500 KB):** Uses the Python Pillow library to automatically resize and compress the final creative output to meet the mandatory file size limit for campaign uploads.
3.  **Front-End Integration:** A simple HTML/JS UI fully integrated with the Flask API endpoints for real-time testing.

## ⚙️ Technical Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend/API** | **Python 3 / Flask** | Provides a lightweight, stable server for routing and ML model serving. |
| **Compliance Logic** | **Python (Pillow, NumPy)** | Used for positional validation logic and image array manipulation. |
| **Image Processing** | **Pillow Library** | Essential for resizing creatives and performing the critical file size compression. |
| **Frontend (UI)** | **HTML/CSS/JavaScript** | Ensures a simple, stable, and highly interactive user experience (UX). |

## 🚀 How to Run the Prototype

Follow these steps to launch the **Creative Guardrail™** locally:

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_LINK]
    cd adapti-creative-studio
    ```

2.  **Setup Backend Dependencies:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Setup Placeholder Image:**
    * Create a placeholder image (any PNG/JPEG, preferably >1MB) and save it in the following path to enable the optimization test:
        ```
        backend/temp/final_creative.png
        ```

4.  **Run the Flask Server:**
    ```bash
    python app.py
    ```
    (The server will start running on `http://127.0.0.1:5000`)

5.  **Access the UI:**
    Open your web browser and navigate to:
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

---

## 🧪 Testing the Guardrail

Use the following input values to validate the key features:

| Test Name | Logo X/Y | Headline | Expected Score | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1: Compliance PASS** | 800 / 800 | `Great product!` | $\approx 98\%$ (Green) | No major violations detected. |
| **Test 2: Margin FAIL (CV)** | 1070 / 1070 | `Great product!` | $\approx 45\%$ (Red) | Violation: Logo is too close to the right edge. |
| **Test 3: Optimization** | N/A | N/A | N/A | Output Optimization Status: SUCCESS! Size: < 500 KB. |

---