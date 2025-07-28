import requests
import json
import random
from typing import Dict, List, Optional

class FluencyCoach:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.groq_api_key = None
        
        if api_keys.get('GROQ_API_KEY'):
            try:
                self.groq_api_key = api_keys['GROQ_API_KEY']
                self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
                self.groq_model = "llama3-8b-8192"
                print("✅ Groq API configured successfully for fluency coaching")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.groq_api_key = None
        else:
            print("⚠️ No Groq API key provided")

    def provide_coaching(self, user_input: str, practice_type: str, topic: str, user_level: str) -> Dict:
        """
        Provide personalized coaching based on user input
        """
        try:
            coaching_prompt = self._create_coaching_prompt(user_input, practice_type, topic, user_level)
            
            coaching_response = self._get_ai_response(coaching_prompt)
            parsed_coaching = self._parse_coaching_response(coaching_response)
            
            return parsed_coaching
            
        except Exception as e:
            print(f"❌ Coaching error: {e}")
            return self._generate_fallback_coaching(user_input, practice_type)

    def generate_practice_prompt(self, practice_type: str, topic: str, level: str) -> Dict:
        """
        Generate practice prompts for different types of exercises
        """
        prompts = {
            'conversation': self._get_conversation_prompts(topic, level),
            'pronunciation': self._get_pronunciation_prompts(level),
            'vocabulary': self._get_vocabulary_prompts(topic, level),
            'storytelling': self._get_storytelling_prompts(topic, level),
            'debate': self._get_debate_prompts(topic, level),
            'presentation': self._get_presentation_prompts(topic, level),
            'song_analysis': self._get_song_prompts(level)
        }
        
        return prompts.get(practice_type, prompts['conversation'])

    def _create_coaching_prompt(self, user_input: str, practice_type: str, topic: str, user_level: str) -> str:
        """
        Create coaching prompt for AI analysis
        """
        return f"""
You are an expert English fluency coach with 15+ years of experience helping students improve their speaking skills. You specialize in providing constructive, encouraging, and actionable feedback.

PRACTICE TYPE: {practice_type}
TOPIC: {topic}
USER LEVEL: {user_level}
USER INPUT: "{user_input}"

Provide comprehensive coaching feedback following this EXACT format:

## IMMEDIATE FEEDBACK
[Provide immediate positive reinforcement and acknowledgment of their effort]

## CORRECTIONS
[List specific corrections needed with explanations]
- Original: [what they said]
- Corrected: [how it should be said]
- Explanation: [why this correction is needed]

## PRONUNCIATION NOTES
[Specific pronunciation feedback and tips]

## VOCABULARY ENHANCEMENT
[Suggest better word choices or more advanced vocabulary]
- Instead of: [basic word/phrase]
- Try using: [advanced alternative]
- Example: [sentence using the advanced word]

## GRAMMAR IMPROVEMENTS
[Point out grammar issues and provide corrections]

## FLUENCY TIPS
[Specific tips to improve natural flow and reduce hesitations]

## CULTURAL CONTEXT
[Explain any cultural nuances or more natural expressions]

## PRACTICE SUGGESTION
[Specific practice exercise based on their performance]

## ENCOURAGEMENT
[Motivational message highlighting their progress and strengths]

## NEXT CHALLENGE
[Suggest a slightly more challenging exercise for continued growth]

Be supportive, specific, and actionable in your feedback. Focus on 2-3 main areas for improvement rather than overwhelming them.
"""

    def _get_conversation_prompts(self, topic: str, level: str) -> Dict:
        """
        Generate conversation practice prompts
        """
        prompts_by_level = {
            'beginner': [
                f"Tell me about your daily routine and how {topic} fits into it.",
                f"Describe your opinion about {topic} in simple terms.",
                f"What do you like or dislike about {topic}? Why?"
            ],
            'intermediate': [
                f"Explain the advantages and disadvantages of {topic}.",
                f"How has {topic} changed in your country over the past 10 years?",
                f"Compare {topic} in your culture versus other cultures you know."
            ],
            'advanced': [
                f"Analyze the long-term implications of current trends in {topic}.",
                f"Debate the ethical considerations surrounding {topic}.",
                f"Propose innovative solutions to challenges related to {topic}."
            ]
        }
        
        level_prompts = prompts_by_level.get(level, prompts_by_level['intermediate'])
        
        return {
            'type': 'conversation',
            'prompt': random.choice(level_prompts),
            'instructions': "Speak naturally for 1-2 minutes. Focus on expressing your ideas clearly.",
            'tips': [
                "Take your time to organize your thoughts",
                "Use specific examples to support your points",
                "Don't worry about perfect grammar - focus on communication"
            ]
        }

    def _get_pronunciation_prompts(self, level: str) -> Dict:
        """
        Generate pronunciation practice prompts
        """
        exercises = {
            'beginner': {
                'tongue_twisters': [
                    "She sells seashells by the seashore",
                    "Peter Piper picked a peck of pickled peppers",
                    "How much wood would a woodchuck chuck"
                ],
                'minimal_pairs': [
                    "Practice: ship/sheep, bit/beat, cat/cut",
                    "Focus on: think/sink, three/tree, bath/bat"
                ]
            },
            'intermediate': {
                'connected_speech': [
                    "Practice linking: 'an apple', 'turn off', 'look at it'",
                    "Work on contractions: 'I'll', 'won't', 'should've'"
                ],
                'stress_patterns': [
                    "Practice word stress: PHOtograph, phoTOGraphy, photoGRAPHic",
                    "Sentence stress: I LOVE chocolate (not hate), I love CHOColate (not vanilla)"
                ]
            },
            'advanced': {
                'intonation': [
                    "Practice rising intonation for questions: 'You're coming?'",
                    "Falling intonation for statements: 'I'm definitely going.'"
                ],
                'rhythm': [
                    "Practice English rhythm with poetry or song lyrics",
                    "Focus on content words vs. function words stress"
                ]
            }
        }
        
        level_exercises = exercises.get(level, exercises['intermediate'])
        exercise_type = random.choice(list(level_exercises.keys()))
        
        return {
            'type': 'pronunciation',
            'exercise_type': exercise_type,
            'prompt': random.choice(level_exercises[exercise_type]),
            'instructions': f"Focus on {exercise_type.replace('_', ' ')} while speaking clearly and slowly.",
            'tips': [
                "Record yourself and listen back",
                "Exaggerate the sounds at first, then make them more natural",
                "Practice in front of a mirror to see mouth movements"
            ]
        }

    def _get_vocabulary_prompts(self, topic: str, level: str) -> Dict:
        """
        Generate vocabulary practice prompts
        """
        vocabulary_challenges = {
            'beginner': f"Use these basic words related to {topic}: important, different, interesting, helpful, difficult. Create sentences with each.",
            'intermediate': f"Incorporate these words about {topic}: significant, diverse, fascinating, beneficial, challenging, innovative, traditional.",
            'advanced': f"Use sophisticated vocabulary for {topic}: paramount, multifaceted, compelling, advantageous, formidable, groundbreaking, conventional."
        }
        
        return {
            'type': 'vocabulary',
            'prompt': vocabulary_challenges.get(level, vocabulary_challenges['intermediate']),
            'instructions': "Create a short speech using as many of these words as possible naturally.",
            'tips': [
                "Don't force words - use them when they fit naturally",
                "Explain the meaning if you're unsure",
                "Try to use synonyms to show vocabulary range"
            ]
        }

    def _get_storytelling_prompts(self, topic: str, level: str) -> Dict:
        """
        Generate storytelling practice prompts
        """
        story_prompts = [
            f"Tell a story about a time when {topic} played an important role in your life.",
            f"Create a fictional story involving {topic} and an unexpected twist.",
            f"Describe a memorable experience related to {topic} from your childhood.",
            f"Tell a story about how {topic} might look like in the future."
        ]
        
        return {
            'type': 'storytelling',
            'prompt': random.choice(story_prompts),
            'instructions': "Tell your story with a clear beginning, middle, and end. Use descriptive language.",
            'tips': [
                "Use past tense consistently for stories",
                "Include dialogue to make it more engaging",
                "Use transition words: first, then, suddenly, finally"
            ]
        }

    def _get_debate_prompts(self, topic: str, level: str) -> Dict:
        """
        Generate debate practice prompts
        """
        debate_topics = [
            f"Should {topic} be regulated by the government?",
            f"Is {topic} more beneficial or harmful to society?",
            f"Will {topic} be more or less important in the future?",
            f"Should schools teach more about {topic}?"
        ]
        
        return {
            'type': 'debate',
            'prompt': random.choice(debate_topics),
            'instructions': "Choose a side and argue your position with evidence and examples.",
            'tips': [
                "Use phrases like 'In my opinion', 'Furthermore', 'However'",
                "Provide specific examples to support your arguments",
                "Acknowledge counterarguments: 'While some may argue...'"
            ]
        }

    def _get_presentation_prompts(self, topic: str, level: str) -> Dict:
        """
        Generate presentation practice prompts
        """
        presentation_topics = [
            f"Give a 3-minute presentation introducing {topic} to beginners.",
            f"Present the pros and cons of {topic} to a business audience.",
            f"Explain how {topic} has evolved over time.",
            f"Propose a solution to a problem related to {topic}."
        ]
        
        return {
            'type': 'presentation',
            'prompt': random.choice(presentation_topics),
            'instructions': "Structure your presentation with introduction, main points, and conclusion.",
            'tips': [
                "Start with: 'Today I'll be talking about...'",
                "Use signposting: 'First', 'Second', 'Finally'",
                "End with: 'To conclude' or 'In summary'"
            ]
        }

    def _get_song_prompts(self, level: str) -> Dict:
        """
        Generate song analysis prompts
        """
        return {
            'type': 'song_analysis',
            'prompt': "Sing or recite a verse from an English song, then explain what it means.",
            'instructions': "Focus on pronunciation, rhythm, and meaning. Don't worry about singing ability!",
            'tips': [
                "Choose a song with clear pronunciation",
                "Pay attention to connected speech in lyrics",
                "Explain any idioms or slang you encounter"
            ]
        }

    def _get_groq_response(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 2000
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"⚠️ Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return None
    
    def _get_ai_response(self, prompt: str) -> str:
        try:
            if self.groq_api_key:
                groq_response = self._get_groq_response(prompt)
                if groq_response:
                    return groq_response
            
            return self._generate_mock_coaching()
                
        except Exception as e:
            print(f"⚠️ AI API Error: {e}")
            return self._generate_mock_coaching()

    def _generate_mock_coaching(self) -> str:
        return """
## IMMEDIATE FEEDBACK
Great effort! I can see you're working hard to express your ideas clearly.

## CORRECTIONS
- Original: "I am very interesting in this topic"
- Corrected: "I am very interested in this topic"
- Explanation: Use "interested" (past participle) when describing your feelings

## PRONUNCIATION NOTES
Focus on the 'th' sound in "think" and "through" - place your tongue between your teeth.

## VOCABULARY ENHANCEMENT
- Instead of: "very good"
- Try using: "excellent" or "outstanding"
- Example: "That's an excellent point about the topic."

## GRAMMAR IMPROVEMENTS
Watch your article usage - remember to use "the" before specific nouns you've mentioned before.

## FLUENCY TIPS
Try to reduce filler words like "um" and "uh" by pausing silently instead.

## CULTURAL CONTEXT
In English, we often use "I think" or "In my opinion" to soften statements and sound more polite.

## PRACTICE SUGGESTION
Practice describing your daily routine using past tense consistently.

## ENCOURAGEMENT
Your communication is clear and your ideas are well-organized. Keep practicing!

## NEXT CHALLENGE
Try incorporating more complex sentence structures with "although" or "despite."
"""

    def _parse_coaching_response(self, response: str) -> Dict:
        """
        Parse the coaching response into structured format
        """
        coaching = {
            'immediate_feedback': '',
            'corrections': [],
            'pronunciation_notes': '',
            'vocabulary_enhancement': [],
            'grammar_improvements': '',
            'fluency_tips': '',
            'cultural_context': '',
            'practice_suggestion': '',
            'encouragement': '',
            'next_challenge': ''
        }
        
        current_section = None
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if '## IMMEDIATE FEEDBACK' in line:
                current_section = 'immediate_feedback'
            elif '## CORRECTIONS' in line:
                current_section = 'corrections'
            elif '## PRONUNCIATION NOTES' in line:
                current_section = 'pronunciation_notes'
            elif '## VOCABULARY ENHANCEMENT' in line:
                current_section = 'vocabulary_enhancement'
            elif '## GRAMMAR IMPROVEMENTS' in line:
                current_section = 'grammar_improvements'
            elif '## FLUENCY TIPS' in line:
                current_section = 'fluency_tips'
            elif '## CULTURAL CONTEXT' in line:
                current_section = 'cultural_context'
            elif '## PRACTICE SUGGESTION' in line:
                current_section = 'practice_suggestion'
            elif '## ENCOURAGEMENT' in line:
                current_section = 'encouragement'
            elif '## NEXT CHALLENGE' in line:
                current_section = 'next_challenge'
            elif line and current_section:
                if current_section in ['corrections', 'vocabulary_enhancement']:
                    if line.startswith('- '):
                        coaching[current_section].append(line[2:])
                else:
                    if coaching[current_section]:
                        coaching[current_section] += ' ' + line
                    else:
                        coaching[current_section] = line
        
        return coaching

    def _generate_fallback_coaching(self, user_input: str, practice_type: str) -> Dict:
        """
        Generate fallback coaching when AI is not available
        """
        return {
            'immediate_feedback': "Thank you for practicing! Your effort is appreciated.",
            'corrections': ["Configure your API keys for detailed corrections"],
            'pronunciation_notes': "Focus on clear articulation and natural rhythm.",
            'vocabulary_enhancement': ["Try using more descriptive adjectives", "Practice synonyms for common words"],
            'grammar_improvements': "Review basic sentence structures and verb tenses.",
            'fluency_tips': "Practice speaking slowly and clearly, reducing filler words.",
            'cultural_context': "English speakers often use polite phrases like 'I think' or 'perhaps'.",
            'practice_suggestion': f"Continue practicing {practice_type} exercises daily.",
            'encouragement': "Keep practicing! Every attempt helps you improve your English skills.",
            'next_challenge': "Try speaking for longer periods without stopping."
        }
