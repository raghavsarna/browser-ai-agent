# AI Agent to navigate the front end of a website

An AI-powered agent designed to navigate and interact with websites automatically. This project demonstrates two different approaches to building browser automation agents using AI.

## 🎯 Overview

This project showcases AI agents that can understand natural language instructions and perform complex web navigation tasks. The agents can search, click, fill forms, and interact with web elements just like a human user would.

## 🚀 Two Implementation Approaches

### 1. Custom Selenium + LLM Implementation

A from-scratch implementation using Selenium WebDriver combined with Google's Gemini AI model.

**Key Features:**

- **Custom Web Element Detection**: Intelligent extraction of clickable elements, forms, and interactive components
- **AI-Powered Decision Making**: Uses Gemini 2.5 Flash model to analyze screenshots and page elements
- **Robust Error Handling**: Multiple fallback strategies for element interaction (direct click, JavaScript click, ActionChains)
- **Smart Element Selection**: XPath-based element targeting with coordinate-aware positioning
- **Screenshot Analysis**: Visual understanding of web pages for better navigation decisions
- **Adaptive Scrolling**: Intelligent page scrolling to find target elements

**Technical Implementation:**

- Selenium WebDriver with Chrome browser automation
- Google Gemini AI for visual and contextual analysis
- Custom element extraction using XPath selectors
- Base64 screenshot encoding for AI analysis
- Comprehensive error handling and retry mechanisms

**Demonstration:**

> **Prompt:** "Go to google.com, search for 'agentic ai' and click on the first result."
>
> 📹 [Demo Video: using_selenium.mp4](demo_videos/using_selenium.mp4)

_Note: This is a prototype demonstrating proof of concept. While functional, there are many optimizations that could be made for production use._

### 2. Browser-Use Library Implementation

A more robust solution using the open-source [Browser-Use](https://github.com/browser-use/browser-use) library.

**Key Features:**

- **Production-Ready**: Built on a mature, well-tested framework
- **High Performance**: Faster and more reliable than the custom Selenium approach
- **Minimal Code**: Requires significantly less implementation code
- **Advanced Capabilities**: Supports complex multi-step workflows out of the box
- **Better Error Handling**: Built-in retry mechanisms and error recovery

**Technical Implementation:**

- Browser-Use library for browser automation
- LangChain integration for LLM management
- Playwright-based browser control (more stable than Selenium)
- Asynchronous operation support

**Demonstration:**

> **Prompt:** "Go to amazon.in, search for 'laptops', sort by best sellers and add the first item to the cart."
>
> 📹 [Demo Video: using_browser_use.mp4](demo_videos/using_browser_use.mp4)

### 3. Browser-Use Web UI

For non-technical users, Browser-Use provides a user-friendly web interface.

**Features:**

- **Gradio-based Web Interface**: Easy-to-use graphical interface
- **Multiple LLM Support**: OpenAI, Anthropic, Google, Azure, DeepSeek, Ollama, and more
- **Custom Browser Support**: Use your own browser instance with existing sessions
- **Docker Support**: Easy deployment with containerization
- **VNC Integration**: Remote browser viewing capabilities

**Demonstration:**

> 📹 [Demo Video: using_browser_use_web-ui.mp4](demo_videos/using_browser_use_web-ui.mp4)

## 📁 Project Structure

```
Browser_AI_Agent/
├── using_selenium.py          # Custom Selenium implementation
├── using_browser_use.py       # Browser-Use library implementation
├── demo_videos/               # Demonstration videos
│   ├── using_selenium.mp4
│   ├── using_browser_use.mp4
│   └── using_browser_use_web-ui.mp4
└── web-ui/                    # Browser-Use Web UI
    ├── webui.py              # Main web interface
    ├── requirements.txt      # Python dependencies
    ├── Dockerfile           # Container configuration
    └── src/                 # Source code modules
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.11+
- Chrome browser (for Selenium approach)
- Google API Key (for Gemini AI)

### Environment Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
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

### Docker Setup (Web UI)

1. **Build and run with Docker:**

   ```bash
   cd web-ui
   docker compose up --build
   ```

2. **Access services:**
   - Web UI: http://localhost:7788
   - VNC Viewer: http://localhost:6080

## 🎮 Usage Examples

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

## 🔧 Configuration

### Supported LLM Providers

- OpenAI (GPT-4, GPT-3.5)
- Google (Gemini Pro, Gemini Flash)
- Anthropic (Claude)
- Azure OpenAI
- DeepSeek
- Ollama (Local models)
- And many more...

### Browser Settings

- Custom browser paths
- User data directories
- Debugging ports
- Resolution settings
- VNC configuration

## 📊 Comparison

| Feature              | Selenium Implementation | Browser-Use Implementation |
| -------------------- | ----------------------- | -------------------------- |
| **Setup Complexity** | High                    | Low                        |
| **Code Required**    | ~500 lines              | ~40 lines                  |
| **Performance**      | Moderate                | High                       |
| **Reliability**      | Good                    | Excellent                  |
| **Customization**    | High                    | Moderate                   |
| **Maintenance**      | High                    | Low                        |
| **Production Ready** | Prototype               | Yes                        |

## 🎯 Use Cases

- **E-commerce Automation**: Product searches, price comparisons, cart management
- **Data Collection**: Automated web scraping and information gathering
- **Testing**: Automated UI testing and validation
- **Research**: Academic and market research automation
- **Social Media**: Content posting and engagement automation
- **Form Filling**: Automated application and registration processes

## ⚠️ Important Notes

- This is a **proof of concept** demonstration
- The Selenium implementation is a prototype showing how to build from scratch
- Browser-Use is recommended for production applications
- Always respect website terms of service and rate limits
- Consider ethical implications of automated web interactions

## 🚧 Future Improvements

- Enhanced error handling and recovery
- Support for more complex authentication flows
- Integration with more LLM providers
- Performance optimizations
- Better element detection algorithms
- Multi-tab and multi-window support

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with website terms of service and applicable laws when using these tools.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

_P.S. The VM setup is not yet complete as the main goal was to demonstrate proof of concept and working functionality._
