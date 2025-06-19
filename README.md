# AI Agent to navigate the front end of a website

## Two Implementation Approaches

### 1. Custom Selenium + LLM Implementation

A from-scratch implementation using Selenium WebDriver combined with Google's Gemini AI model.

**Demonstration:**

> **Prompt:** "Go to google.com, search for 'agentic ai' and click on the first result."
>
> 📹 [Demo Video: using_selenium.mp4](demo_videos/using_selenium.mp4)

_Note: This is a prototype demonstrating proof of concept. While functional, there are many optimizations that could be made for production use._

### 2 Browser-Use Library Implementation

A more robust solution using the open-source [Browser-Use](https://github.com/browser-use/browser-use) library.

**Demonstration:**

> **Prompt:** "Go to amazon.in, search for 'laptops', sort by best sellers and add the first item to the cart."
>
> 📹 [Demo Video: using_browser_use.mp4](demo_videos/using_browser_use.mp4)

#### Browser-Use Web UI

For non-technical users, Browser-Use provides a user-friendly web interface.

**Demonstration:**

> 📹 [Demo Video: using_browser_use_web-ui.mp4](demo_videos/using_browser_use_web-ui.mp4)

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.11+
- Chrome browser (for Selenium approach)
- Google API Key (for Gemini AI)

### Environment Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/raghavsarna/browser-ai-agent.git
   cd Browser_AI_Agent
   ```

2. **Create environment file:**

   ```bash
   cp .env.example .env
   ```

3. **Add your API keys to `.env`:**
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### Option 1: Selenium Implementation

1. **Install dependencies:**

   ```bash
   pip install selenium google-generativeai pillow python-dotenv requests
   ```

2. **Install ChromeDriver:**

   - Download from [ChromeDriver](https://chromedriver.chromium.org/)
   - Add to PATH or place in project directory

3. **Run the agent:**
   ```bash
   python using_selenium.py
   ```

### Option 2: Browser-Use Implementation

1. **Install dependencies:**

   ```bash
   pip install browser-use langchain-google-genai python-dotenv
   ```

2. **Install Playwright browsers:**

   ```bash
   playwright install chromium --with-deps
   ```

3. **Run the agent:**
   ```bash
   python using_browser_use.py
   ```

### Option 3: Web UI Setup

1. **Navigate to web-ui directory:**

   ```bash
   cd web-ui
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   playwright install chromium --with-deps
   ```

3. **Run the web interface:**

   ```bash
   python webui.py
   ```

4. **Access the interface:**
   Open http://localhost:7788 in your browser

## Usage Examples

### Selenium Agent

```python
agent = WebNavigationAgent(API_KEY, headless=False)
await agent.perform_task(
    url="https://google.com",
    task="Search for 'agentic ai' and click on the first result.",
    max_steps=7
)
```

### Browser-Use Agent

```python
agent = Agent(
    task="Go to amazon.in, search for 'laptops', sort by best sellers and add the first item to the cart.",
    llm=llm,
    browser_session=browser_session
)
result = await agent.run()
```

_P.S. The VM setup is not yet complete as the main goal was to demonstrate proof of concept and working functionality._
