"""
Ollama client for local LLM integration.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, AsyncGenerator
import ollama
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)


class InfluencedReadingResponse(BaseModel):
    """Structured response schema for influenced readings."""
    reading_id: str
    summary: str
    cards: List[Dict[str, Any]]
    advice: List[str]
    follow_up_questions: List[str]


class OllamaClient:
    """Client for interacting with local Ollama LLM."""
    
    def __init__(self, model: str = "llama3.2:3b", host: str = "localhost", port: int = 11434):
        self.model = model
        self.host = host
        self.port = port
        self.client = ollama.Client(host=f"http://{host}:{port}")
        
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            models = self.client.list()
            return any(model['name'] == self.model for model in models['models'])
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    async def generate_influenced_meanings(self, reading_context: Dict[str, Any]) -> InfluencedReadingResponse:
        """
        Generate influenced meanings for a tarot reading.
        
        Args:
            reading_context: Context including cards, positions, and influences
            
        Returns:
            Structured response with influenced meanings
        """
        
        prompt = self._build_influence_prompt(reading_context)
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 2000
                }
            )
            
            # Parse JSON response
            response_text = response['response']
            parsed_response = self._parse_json_response(response_text)
            
            # Validate against schema
            validated_response = InfluencedReadingResponse(**parsed_response)
            
            return validated_response
            
        except Exception as e:
            logger.error(f"Error generating influenced meanings: {e}")
            return self._create_fallback_response(reading_context)
    
    async def chat_stream(self, messages: List[Dict[str, str]], 
                         context: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Stream chat responses from Ollama.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            context: Optional context for the conversation
            
        Yields:
            Streaming response chunks
        """
        
        try:
            # Add context to system message if provided
            if context:
                system_message = self._build_context_message(context)
                messages.insert(0, {'role': 'system', 'content': system_message})
            
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    'temperature': 0.8,
                    'top_p': 0.9
                }
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            logger.error(f"Error in chat stream: {e}")
            yield "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
    
    async def chat(self, messages: List[Dict[str, str]], 
                   context: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a complete chat response from Ollama.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            context: Optional context for the conversation
            
        Returns:
            Complete response text
        """
        
        try:
            # Add context to system message if provided
            if context:
                system_message = self._build_context_message(context)
                messages.insert(0, {'role': 'system', 'content': system_message})
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.8,
                    'top_p': 0.9
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
    
    def _build_influence_prompt(self, reading_context: Dict[str, Any]) -> str:
        """Build prompt for generating influenced meanings."""
        
        cards_info = []
        for card in reading_context.get('cards', []):
            card_info = f"""
Card: {card['card_name']} ({card['orientation']})
Position: {card['position_name']}
Base Polarity: {card['polarity_score']:.2f}
Base Intensity: {card['intensity_score']:.2f}
Influence Factors:
"""
            for factor in card.get('influence_factors', []):
                card_info += f"  - {factor['explain']} (effect: {factor['effect']:+.2f})\n"
            
            cards_info.append(card_info)
        
        prompt = f"""
You are a skilled tarot reader with deep knowledge of card meanings and interactions. 
Generate influenced meanings for this tarot reading.

Reading Context:
- Reading ID: {reading_context.get('reading_id', 'unknown')}
- Spread: {reading_context.get('spread_name', 'unknown')}
- Date: {reading_context.get('date', 'unknown')}

Cards and Influences:
{chr(10).join(cards_info)}

Please provide a JSON response with the following structure:
{{
  "reading_id": "{reading_context.get('reading_id', 'unknown')}",
  "summary": "A brief overall summary of the reading",
  "cards": [
    {{
      "position": "position_name",
      "card_id": "card_id",
      "card_name": "card_name",
      "orientation": "upright|reversed",
      "base_text": "Original card meaning",
      "influenced_text": "How the card's meaning is modified by influences",
      "polarity_score": 0.0,
      "intensity_score": 0.0,
      "influence_factors": [
        {{
          "source_card_id": "source_card_id",
          "effect": "+0.40",
          "explain": "Explanation of the influence"
        }}
      ],
      "journal_prompt": "A thoughtful prompt for journaling about this card"
    }}
  ],
  "advice": ["Practical advice item 1", "Practical advice item 2"],
  "follow_up_questions": ["Question 1", "Question 2"]
}}

Focus on:
1. How neighboring cards modify each card's meaning
2. The overall story the reading tells
3. Practical, actionable advice
4. Thoughtful journaling prompts
5. Specific influence factors with clear explanations

Respond with valid JSON only.
"""
        return prompt
    
    def _build_context_message(self, context: Dict[str, Any]) -> str:
        """Build context message for chat conversations."""
        
        if 'reading' in context:
            reading = context['reading']
            return f"""
You are a wise tarot reader helping someone understand their reading. 

Current Reading Context:
- Title: {reading.get('title', 'Untitled Reading')}
- Spread: {reading.get('spread_name', 'Unknown')}
- Date: {reading.get('date', 'Unknown')}
- Cards: {', '.join([f"{card['card_name']} ({card['orientation']})" for card in reading.get('cards', [])])}

You can reference this reading context in your responses. Be helpful, insightful, and encouraging.
"""
        elif 'card' in context:
            card = context['card']
            return f"""
You are a wise tarot reader helping someone understand a specific card.

Card Context:
- Name: {card.get('name', 'Unknown')}
- Orientation: {card.get('orientation', 'upright')}
- Position: {card.get('position', 'Unknown')}
- Keywords: {', '.join(card.get('keywords', []))}

Provide insightful guidance about this card's meaning and significance.
"""
        else:
            return "You are a wise tarot reader. Help the user with their tarot questions and provide insightful guidance."
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        
        # Try to extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[start_idx:end_idx]
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def _create_fallback_response(self, reading_context: Dict[str, Any]) -> InfluencedReadingResponse:
        """Create fallback response when AI is unavailable."""
        
        cards = []
        for card in reading_context.get('cards', []):
            cards.append({
                "position": card.get('position_name', 'unknown'),
                "card_id": card.get('card_id', 'unknown'),
                "card_name": card.get('card_name', 'Unknown'),
                "orientation": card.get('orientation', 'upright'),
                "base_text": "Card meaning temporarily unavailable",
                "influenced_text": "AI analysis temporarily unavailable",
                "polarity_score": card.get('polarity_score', 0.0),
                "intensity_score": card.get('intensity_score', 0.0),
                "influence_factors": [
                    {
                        "source_card_id": "unknown",
                        "effect": "unknown",
                        "explain": "AI analysis temporarily unavailable"
                    }
                ],
                "journal_prompt": "Reflect on what this card means to you in your current situation."
            })
        
        return InfluencedReadingResponse(
            reading_id=reading_context.get('reading_id', 'unknown'),
            summary="AI analysis temporarily unavailable. Please try again later.",
            cards=cards,
            advice=["Take time to reflect on the cards and their meanings"],
            follow_up_questions=["What does this reading mean to you?", "How do you feel about these cards?"]
        )
    
    async def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry."""
        try:
            self.client.pull(model_name)
            return True
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False