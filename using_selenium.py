import asyncio
import json
import base64
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ElementInfo:
    tag: str
    text: str
    xpath: str
    attributes: Dict[str, str]
    coordinates: Tuple[int, int, int, int]
    element_id: str

class WebNavigationAgent:
    def __init__(self, gemini_api_key: str, headless: bool = False):
        self.gemini_api_key = gemini_api_key
        self.headless = headless
        self.driver = None
        self.wait = None
        
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.setup_browser()
    
    def setup_browser(self):
        chrome_options = Options()
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Browser initialized successfully")
    
    def take_screenshot(self) -> str:
        screenshot = self.driver.get_screenshot_as_png()
        return base64.b64encode(screenshot).decode('utf-8')
    
    def get_page_elements(self) -> List[ElementInfo]:
        elements = []
        
        selectors = [
            "//button", "//input", "//select", "//textarea", 
            "//a[@href]", "//div[@onclick]", "//span[@onclick]",
            "//div[@role='button']", "//div[@role='link']",
            "//div[@role='tab']", "//div[@role='menuitem']",
            "//h1/a", "//h2/a", "//h3/a", "//h4/a", "//h5/a", "//h6/a",
            "//li/a", "//p/a", "//span/a",
            "//div[@tabindex]", "//span[@tabindex]",
            "//form", "//label[@for]"
        ]
        
        for selector in selectors:
            try:
                web_elements = self.driver.find_elements(By.XPATH, selector)
                for i, element in enumerate(web_elements):
                    try:
                        if not element.is_displayed():
                            continue
                            
                        rect = element.rect
                        if rect['width'] == 0 or rect['height'] == 0:
                            continue
                        
                        element_info = ElementInfo(
                            tag=element.tag_name,
                            text=element.text.strip()[:100],
                            xpath=self._get_xpath(element),
                            attributes=self._get_element_attributes(element),
                            coordinates=(rect['x'], rect['y'], rect['width'], rect['height']),
                            element_id=f"{element.tag_name}_{i}"
                        )
                        elements.append(element_info)
                    except Exception as e:
                        continue
            except Exception as e:
                continue
        
        return elements[:50] 
    
    def _get_xpath(self, element) -> str:
        try:
            return self.driver.execute_script("""
                function getXPath(element) {
                    if (element.id !== '') {
                        return `//*[@id="${element.id}"]`;
                    }
                    if (element === document.body) {
                        return '/html/body';
                    }
                    
                    var ix = 0;
                    var siblings = element.parentNode.childNodes;
                    for (var i = 0; i < siblings.length; i++) {
                        var sibling = siblings[i];
                        if (sibling === element) {
                            return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                        }
                        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                            ix++;
                        }
                    }
                }
                return getXPath(arguments[0]);
            """, element)
        except:
            return ""
    
    def _get_element_attributes(self, element) -> Dict[str, str]:
        attributes = {}
        try:
            attr_names = ['id', 'class', 'name', 'type', 'href', 'title', 'placeholder', 'value', 'role', 'aria-label', 'data-testid']
            for attr in attr_names:
                value = element.get_attribute(attr)
                if value:
                    attributes[attr] = value[:100]
        except:
            pass
        return attributes
    
    def navigate_to(self, url: str):
        try:
            self.driver.get(url)
            time.sleep(3)
            print(f"Navigated to: {url}")
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False
    
    def click_element(self, xpath: str) -> bool:
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            element.click()
            time.sleep(1)
            print(f"Clicked element: {xpath}")
            return True
            
        except ElementClickInterceptedException:
            print("Click intercepted, trying JavaScript click...")
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(1)
                print(f"JavaScript clicked element: {xpath}")
                return True
            except Exception as e2:
                print(f"JavaScript click failed: {e2}")
                
        except TimeoutException:
            print("Element not clickable, trying to find and click anyway...")
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(1)
                print(f"Force clicked element: {xpath}")
                return True
            except Exception as e3:
                print(f"Force click failed: {e3}")
                
        except Exception as e:
            print(f"Error clicking element {xpath}: {e}")
            
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                time.sleep(1)
                print(f"ActionChains clicked element: {xpath}")
                return True
            except Exception as e4:
                print(f"ActionChains click failed: {e4}")
        
        return False
    
    def type_text(self, xpath: str, text: str) -> bool:
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.clear()
            element.send_keys(text)
            time.sleep(0.5)
            print(f"Typed '{text}' into element: {xpath}")
            return True
        except Exception as e:
            print(f"Error typing into element {xpath}: {e}")
            return False
    
    def scroll_page(self, direction: str = "down", pixels: int = 300):
        try:
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            elif direction == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            time.sleep(1)
            print(f"Scrolled {direction} by {pixels} pixels")
            return True
        except Exception as e:
            print(f"Error scrolling: {e}")
            return False
    
    def get_page_info(self) -> Dict:
        return {
            "url": self.driver.current_url,
            "title": self.driver.title,
            "page_source_length": len(self.driver.page_source),
            "window_size": self.driver.get_window_size()
        }
    
    def find_clickable_links(self) -> List[str]:
        xpaths = [
            "//a[@href and normalize-space(text())]",
            "//a[@href]//h1 | //a[@href]//h2 | //a[@href]//h3 | //a[@href]//h4 | //a[@href]//h5 | //a[@href]//h6",
            "//div[@role='link'] | //span[@role='link']",
            "//a[@href and @title]",
            "//button[@onclick] | //div[@onclick] | //span[@onclick]"
        ]
        
        links = []
        for xpath in xpaths:
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for elem in elements[:5]:
                    if elem.is_displayed() and elem.rect['width'] > 0 and elem.rect['height'] > 0:
                        elem_xpath = self._get_xpath(elem)
                        if elem_xpath:
                            links.append(elem_xpath)
            except Exception as e:
                continue
                
        return links[:10]
    
    async def analyze_page_with_ai(self, task: str) -> Dict:
        """Analyze current page with Gemini AI"""
        try:
            screenshot_b64 = self.take_screenshot()
            
            elements = self.get_page_elements()
            
            page_info = self.get_page_info()
            
            elements_summary = []
            for elem in elements:
                elements_summary.append({
                    "id": elem.element_id,
                    "tag": elem.tag,
                    "text": elem.text,
                    "attributes": elem.attributes,
                    "xpath": elem.xpath,
                    "coordinates": elem.coordinates
                })
            
            prompt = f"""
            You are an AI agent helping to navigate any website. 
            
            TASK: {task}
            
            CURRENT PAGE INFO:
            - URL: {page_info['url']}
            - Title: {page_info['title']}
            
            AVAILABLE ELEMENTS:
            {json.dumps(elements_summary, indent=2)}
            
            INSTRUCTIONS:
            1. Analyze the current page and available elements
            2. Choose the best element to interact with based on the task
            3. Consider element visibility, coordinates, and attributes
            4. For links, prefer elements with meaningful text or titles
            5. For forms, identify input fields and submit buttons
            6. If multiple similar elements exist, choose the most prominent one
            
            Based on the screenshot and available elements, provide your analysis in JSON format:
            {{
                "analysis": "Your analysis of the current page and how it relates to the task",
                "next_action": "click|type|scroll|navigate|wait",
                "target_element": "xpath of target element (if applicable)",
                "input_text": "text to input (if action is type)",
                "scroll_direction": "up|down (if action is scroll)",
                "reasoning": "Why you chose this action and element",
                "confidence": "1-10 scale of confidence in this action",
                "alternative_actions": ["list of alternative XPaths or actions if primary fails"],
                "task_progress": "assessment of how close we are to completing the task"
            }}
            
            Focus on finding the most relevant elements for the task. Be specific about XPath selections.
            """
            
            image_data = base64.b64decode(screenshot_b64)
            image = Image.open(BytesIO(image_data))
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content([prompt, image])
                    break
                except Exception as e:
                    print(f"Gemini API attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(2)
            
            try:
                response_text = response.text
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text
                
                ai_response = json.loads(json_text)
                return ai_response
                
            except json.JSONDecodeError as e:
                print(f"Error parsing AI response: {e}")
                print(f"Raw response: {response.text}")
                return {
                    "analysis": "Error parsing AI response",
                    "next_action": "scroll",
                    "reasoning": "Failed to parse AI response, defaulting to scroll",
                    "confidence": 1,
                    "alternative_actions": ["wait"]
                }
                
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return {
                "analysis": "Error in AI analysis",
                "next_action": "scroll",
                "reasoning": f"AI analysis failed: {str(e)}",
                "confidence": 1,
                "alternative_actions": ["wait"]
            }
    
    def execute_action(self, action_data: Dict) -> bool:
        """Execute an action based on AI recommendation"""
        action = action_data.get("next_action")
        
        if action == "click":
            xpath = action_data.get("target_element")
            if xpath:
                success = self.click_element(xpath)
                if not success:
                    alternatives = action_data.get("alternative_actions", [])
                    for alt in alternatives:
                        if isinstance(alt, str) and (alt.startswith("//") or alt.startswith("/")):
                            if self.click_element(alt):
                                return True
                return success
        
        elif action == "type":
            xpath = action_data.get("target_element")
            text = action_data.get("input_text")
            if xpath and text:
                return self.type_text(xpath, text)
        
        elif action == "scroll":
            direction = action_data.get("scroll_direction", "down")
            return self.scroll_page(direction)
        
        elif action == "navigate":
            url = action_data.get("target_url")
            if url:
                return self.navigate_to(url)
        
        elif action == "wait":
            wait_time = action_data.get("wait_time", 2)
            time.sleep(wait_time)
            print(f"Waited for {wait_time} seconds")
            return True
        
        return False
    
    async def perform_task(self, url: str, task: str, max_steps: int = 10):
        print(f"Starting task: {task}")
        print(f"Target URL: {url}")
        
        if not self.navigate_to(url):
            print("Failed to navigate to URL")
            return False
        
        previous_url = ""
        for step in range(max_steps):
            print(f"\n--- Step {step + 1} ---")
            
            current_url = self.driver.current_url
            if current_url != url and current_url != previous_url:
                print(f"Page changed from {previous_url} to {current_url}")
            
            ai_response = await self.analyze_page_with_ai(task)
            
            print(f"AI Analysis: {ai_response['analysis']}")
            print(f"Next Action: {ai_response['next_action']}")
            print(f"Reasoning: {ai_response['reasoning']}")
            print(f"Confidence: {ai_response['confidence']}/10")
            
            task_progress = ai_response.get('task_progress', '')
            if task_progress:
                print(f"Task Progress: {task_progress}")
            
            success = self.execute_action(ai_response)
            
            if not success:
                print("Primary action failed, trying alternatives...")
                alternatives = ai_response.get("alternative_actions", [])
                for alt_action in alternatives[:2]:
                    try:
                        if isinstance(alt_action, str) and (alt_action.startswith("//") or alt_action.startswith("/")):
                            if self.click_element(alt_action):
                                success = True
                                break
                        elif isinstance(alt_action, str):
                            alt_data = {"next_action": alt_action}
                            if self.execute_action(alt_data):
                                success = True
                                break
                    except Exception as e:
                        print(f"Alternative action failed: {e}")
                        continue
            
            if not success:
                print("All actions failed, continuing to next step")
            
            previous_url = current_url
            
            time.sleep(2)
        
        print(f"\nTask completed after {max_steps} steps")
        print(f"Final URL: {self.driver.current_url}")
        return True
    
    def close(self):
        if self.driver:
            self.driver.quit()
            print("Browser closed")

async def main():    
    API_KEY = os.getenv("GOOGLE_API_KEY")
    
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    agent = WebNavigationAgent(API_KEY, headless=False)
    
    try:
        await agent.perform_task(
            url="https://google.com",
            task="Search for 'agentic ai' and click on the first result.",
            max_steps=7
        )
        
        time.sleep(5)
        
    except Exception as e:
        print(f"Error during task execution: {e}")
    
    finally:
        agent.close()

if __name__ == "__main__":
    asyncio.run(main())