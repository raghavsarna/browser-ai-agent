# AI Agent to navigate the front end of a website

Here are two approaches of doing so

## 1. Building it from scratch using Selenium + LLM API

### Overall structure for how code works:

- **Setup**: Launches Chrome (headless optional), connects to Gemini AI via API key.
- **Core**:
  - Scans the page for interactive elements like buttons and links.
  - Takes screenshots and sends them to the AI for analysis.
  - Receives instructions from the AI on what actions to take.
- **Actions**:
  - Click elements.
  - Type text.
  - Scroll.
  - Navigate to URLs.
  - Wait between steps.
- **Task Flow**:
  - Navigates to a specified URL.
  - Uses AI to determine and execute actions (up to predefined number of steps).
  - Handles errors.

### Demonstration:

Prompt: Go to google.com, search for 'agentic ai' and click on the first result.  
<video src="demo_videos/using_selenium.mp4" controls width="600"></video>

Do note that this is just a prototype to demonstrate proof of concept so there are many optimizations to be made. I have presented this solution to give an idea of how I can build it from scratch.

A much more robust way would be to use browser-use.

## 2. Using Browser-Use

It is an open source library to connect AI agents with the browser. (https://github.com/browser-use/browser-use)

### Demonstration:

Prompt: Go to amazon.in, search for 'laptops', sort by best sellers and add the first item to the cart.  
<video src="demo_videos/using_browser_use.mp4" controls width="600"></video>

- Faster and more reliable than the Selenium prototype.
- Simple to set up.
- Requires significantly less code.

Another way to access browser-use is using web-ui in case it is to be used by non tech users. (https://github.com/browser-use/web-ui)

### Demonstration:

<video src="demo_videos/using_browser_use_web-ui.mp4" controls width="600"></video>

P.S. Didn't set it up on VM just yet. My main goal was to just show proof of concept and working.
