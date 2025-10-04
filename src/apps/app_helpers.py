"""
Application-specific helpers
Contains specialized logic for different applications
"""

import logging
from typing import Dict, Any, List
from abc import ABC, abstractmethod

class AppHelper(ABC):
    """Base class for application-specific helpers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def get_context_hints(self, window_info: Dict[str, Any]) -> List[str]:
        """Get context-specific hints for this application"""
        pass
    
    @abstractmethod
    def analyze_content(self, screenshot, window_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze application-specific content"""
        pass

class VSCodeHelper(AppHelper):
    """Helper for Visual Studio Code"""
    
    def get_context_hints(self, window_info: Dict[str, Any]) -> List[str]:
        """Get VS Code specific hints"""
        hints = [
            "I can help with code review and suggestions",
            "Ask me about debugging techniques",
            "I can explain syntax and best practices",
            "Need help with Git commands or workflows?",
            "I can suggest useful VS Code extensions"
        ]
        
        # Analyze window title for more specific hints
        title = window_info.get("title", "").lower()
        
        if ".py" in title:
            hints.extend([
                "Python-specific help available",
                "I can suggest Python best practices",
                "Need help with Python libraries?"
            ])
        elif ".js" in title or ".ts" in title:
            hints.extend([
                "JavaScript/TypeScript assistance ready",
                "I can help with modern JS features",
                "React/Node.js guidance available"
            ])
        elif ".html" in title or ".css" in title:
            hints.extend([
                "Web development help available",
                "I can suggest CSS improvements",
                "HTML accessibility tips ready"
            ])
        
        return hints
    
    def analyze_content(self, screenshot, window_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze VS Code specific content"""
        return {
            "app_type": "vscode",
            "suggestions": [
                "Code assistance and debugging",
                "Syntax explanations",
                "Best practices and refactoring tips",
                "Extension recommendations"
            ],
            "window_title": window_info.get("title", ""),
            "file_type": self._extract_file_type(window_info.get("title", ""))
        }
    
    def _extract_file_type(self, title: str) -> str:
        """Extract file type from window title"""
        if ".py" in title:
            return "python"
        elif ".js" in title:
            return "javascript"
        elif ".ts" in title:
            return "typescript"
        elif ".html" in title:
            return "html"
        elif ".css" in title:
            return "css"
        elif ".json" in title:
            return "json"
        elif ".md" in title:
            return "markdown"
        else:
            return "unknown"

class ExcelHelper(AppHelper):
    """Helper for Microsoft Excel"""
    
    def get_context_hints(self, window_info: Dict[str, Any]) -> List[str]:
        return [
            "I can help with Excel formulas and functions",
            "Need data analysis or chart suggestions?",
            "I can explain complex formulas step by step",
            "Ask about pivot tables and data visualization",
            "I can suggest data cleaning techniques"
        ]
    
    def analyze_content(self, screenshot, window_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "app_type": "excel",
            "suggestions": [
                "Formula help and explanations",
                "Data analysis tips",
                "Chart and visualization suggestions",
                "Pivot table guidance",
                "Data validation and cleaning"
            ],
            "window_title": window_info.get("title", "")
        }

class BrowserHelper(AppHelper):
    """Helper for web browsers"""
    
    def get_context_hints(self, window_info: Dict[str, Any]) -> List[str]:
        hints = [
            "I can summarize web pages for you",
            "Need help researching a topic?",
            "I can analyze content and provide insights",
            "Ask me to explain complex articles",
            "I can suggest related topics to explore"
        ]
        
        title = window_info.get("title", "").lower()
        
        if "github" in title:
            hints.extend([
                "I can help with GitHub workflows",
                "Code repository analysis available",
                "Git best practices guidance"
            ])
        elif "stackoverflow" in title:
            hints.extend([
                "I can help explain technical solutions",
                "Code review and improvement suggestions",
                "Alternative approaches to problems"
            ])
        elif "youtube" in title:
            hints.extend([
                "I can suggest related learning content",
                "Help with technical tutorials",
                "Learning path recommendations"
            ])
        
        return hints
    
    def analyze_content(self, screenshot, window_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "app_type": "browser",
            "suggestions": [
                "Web page summarization",
                "Research assistance",
                "Link and content analysis",
                "Learning guidance"
            ],
            "window_title": window_info.get("title", ""),
            "url_hints": self._analyze_url_type(window_info.get("title", ""))
        }
    
    def _analyze_url_type(self, title: str) -> List[str]:
        """Analyze what type of website based on title"""
        title_lower = title.lower()
        hints = []
        
        if "github" in title_lower:
            hints.append("code_repository")
        if "stackoverflow" in title_lower:
            hints.append("technical_qa")
        if "youtube" in title_lower:
            hints.append("video_content")
        if "documentation" in title_lower or "docs" in title_lower:
            hints.append("documentation")
        
        return hints

class AppHelperFactory:
    """Factory for creating application-specific helpers"""
    
    _helpers = {
        "vscode": VSCodeHelper,
        "excel": ExcelHelper,
        "browser": BrowserHelper
    }
    
    @classmethod
    def get_helper(cls, app_type: str) -> AppHelper:
        """Get helper for specific application type"""
        helper_class = cls._helpers.get(app_type)
        
        if helper_class:
            return helper_class()
        else:
            return DefaultAppHelper()

class DefaultAppHelper(AppHelper):
    """Default helper for unknown applications"""
    
    def get_context_hints(self, window_info: Dict[str, Any]) -> List[str]:
        return [
            "I can see what you're working on",
            "Feel free to ask me any questions",
            "I can provide general assistance",
            "Tell me what you need help with!"
        ]
    
    def analyze_content(self, screenshot, window_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "app_type": "unknown",
            "suggestions": [
                "General assistance available",
                "Ask me questions about what you see",
                "I can help analyze content"
            ],
            "window_title": window_info.get("title", "")
        }