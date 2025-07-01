# 🧠 Enhanced Web Search Agent using LangChain + Gemini + Flask

This project is an **intelligent agent** built using **LangChain**, **Google Gemini 2.5 Flash**, **SerpAPI**, and **Selenium**, wrapped in a **Flask API**. It supports web-enhanced, multimodal, real-time search and tool use with streaming responses.

---

## 🚀 Features

- ✅ Google Gemini 2.5 Flash as LLM
- 🔎 Real-time search using SerpAPI with:
  - Headless Chrome scraping
  - Dynamic content rendering via Selenium
  - Screenshot + visual analysis via Gemini Vision
- 🛠 Tools:
  - `DateAndTime`
  - `WebSearch`
  - `Add`, `Subtract`, `Multiply`, `Exponentiate`
  - `final_answer` signaling final response
- 🌐 Flask server with `/chat`, `/new_chat`, `/health`
- 📡 SSE-style response streaming

---

## 🧰 Technologies Used

- **Python**
- **LangChain**
- **Google Generative AI (Gemini 2.5 Flash)**
- **SerpAPI**
- **Selenium + ChromeDriver**
- **BeautifulSoup**
- **Flask**

---

## 🛠 Installation

```bash
git clone https://github.com/saiteja9078/GenAi-Langchain.git
cd GenAi-Langchain/projects/<your_project_folder>
pip install -r requirements.txt
