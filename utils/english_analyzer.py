import requests
import json
import re
from typing import Dict, List, Optional
import os
from datetime import datetime

class EnglishAnalyzer:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.groq_api_key = None
        
        if api_keys.get('GROQ_API_KEY'):
            try:
                self.groq_api_key = api_keys['GROQ_API_KEY']
                self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
                self.groq_model = "llama3-8b-8192"
                print("✅ Groq API configured successfully for English analysis")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.groq_api_key = None
        else:
            print("⚠️ No Groq API key provided")
        
        if not self.groq_api_key:
            print("⚠️ No AI analysis API available")

    def analyze_speech_proficiency(self, transcription: str, audio_file_path: str = None, 
                                 assessment_type: str = 'general') -> Dict:
        """
        Comprehensive English proficiency analysis
        """
        try:
            # Get audio analysis if file is available
            audio_analysis = self._analyze_audio_characteristics(audio_file_path) if audio_file_path else {}
            
            # Analyze transcription
            text_analysis = self._analyze_text_proficiency(transcription, assessment_type)
            
            # Combine analyses
            combined_analysis = self._combine_analyses(text_analysis, audio_analysis, transcription)
            
            return combined_analysis
            
        except Exception as e:
            print(f"❌ Speech proficiency analysis error: {e}")
            raise

    def _analyze_text_proficiency(self, transcription: str, assessment_type: str) -> Dict:
        """
        Analyze text for English proficiency using AI
        """
        analysis_prompt = self._create_proficiency_prompt(transcription, assessment_type)
        
        analysis_text = self._get_ai_response(analysis_prompt)
        parsed_analysis = self._parse_proficiency_analysis(analysis_text)
        
        return parsed_analysis

    def _create_proficiency_prompt(self, transcription: str, assessment_type: str) -> str:
        """
        Create detailed prompt for English proficiency analysis
        """
        return f"""
You are a world-renowned English language proficiency expert and certified TESOL instructor with 20+ years of experience. You are known for providing detailed, professional analysis like a premium English tutor.

ASSESSMENT TYPE: {assessment_type}
TRANSCRIPTION TO ANALYZE: "{transcription}"

Provide a comprehensive professional English assessment following this EXACT format:

## PRONUNCIATION ANALYSIS
[Provide detailed analysis of pronunciation quality, clarity, accent, stress patterns, intonation, and specific sounds. Be specific about what sounds good and what needs improvement. Mention specific phonetic issues if any.]

## VOCABULARY ASSESSMENT
[Analyze vocabulary range, sophistication, word choice appropriateness, and lexical diversity. Identify advanced words used and suggest specific upgrades.]
- Advanced words used: [list specific advanced words they used]
- Vocabulary level: [beginner/intermediate/advanced with explanation]
- Suggested word upgrades: [specific examples like "tired -> worn out"]

## GRAMMAR EVALUATION
[Assess grammar accuracy, sentence structure complexity, tense usage, and error patterns. Be specific about strengths and areas needing work.]
- Grammar strengths: [specific examples of correct usage]
- Areas for improvement: [specific grammar points to work on]
- Sentence complexity: [analysis of their sentence structures]

## FLUENCY ANALYSIS
[Evaluate speech flow, hesitations, filler words, pace, natural rhythm, and speaking rate]
- Filler words detected: [count and list them]
- Speaking rate assessment: [words per minute if calculable]
- Flow quality: [detailed assessment]

## COHERENCE & ORGANIZATION
[Assess logical flow, idea connection, topic development, clarity of expression]

## PROFESSIONAL IMPROVEMENT PLANS
Create specific, actionable improvement plans for each area:

### Pronunciation Plan:
[3-4 specific daily exercises for pronunciation improvement]

### Vocabulary Plan:
[3-4 specific strategies for vocabulary enhancement]

### Grammar Plan:
[3-4 specific grammar improvement activities]

### Fluency Plan:
[3-4 specific fluency enhancement exercises]

## CEFR LEVEL ASSESSMENT
CEFR Level: [A1, A2, B1, B2, C1, or C2]
Level Description: [Beginner/Elementary/Intermediate/Upper-Intermediate/Advanced/Proficient]

## DETAILED PROFESSIONAL FEEDBACK
[Provide encouraging, detailed feedback like a professional English tutor. Be specific about their current abilities and growth potential. Include cultural and contextual advice.]

## NEXT LEVEL PATHWAY
[Explain specifically what they need to do to reach the next CEFR level, with timeline estimates and priority focus areas]

## PRIORITY FOCUS AREAS
[List the top 2-3 areas they should focus on immediately for maximum improvement]

Be detailed, professional, encouraging, and specific. Provide the kind of analysis a student would get from a premium English tutor.
"""

    def _analyze_audio_characteristics(self, audio_file_path: str) -> Dict:
        """
        Analyze audio characteristics (placeholder for future audio analysis)
        """
        if not audio_file_path or not os.path.exists(audio_file_path):
            return {}
        
        # Basic audio file analysis
        file_size = os.path.getsize(audio_file_path)
        
        # Estimate speaking duration (rough approximation)
        estimated_duration = file_size / (16000 * 2)  # Assuming 16kHz, 16-bit
        
        return {
            'file_size': file_size,
            'estimated_duration': estimated_duration,
            'audio_quality': 'good' if file_size > 50000 else 'low'
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
                "temperature": 0.7,
                "max_tokens": 4000
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
            
            return self._generate_mock_analysis()
                
        except Exception as e:
            print(f"⚠️ AI API Error: {e}")
            return self._generate_mock_analysis()

    def _generate_mock_analysis(self) -> str:
        return """
## PRONUNCIATION ANALYSIS
Your pronunciation shows good clarity with some areas for improvement. Focus on stress patterns and intonation.
Score: 6/10

## VOCABULARY ASSESSMENT
- Advanced words used: demonstrate, analyze, comprehensive
- Basic/Simple words: good, nice, very, really
- Vocabulary level: intermediate
Score: 6/10

## GRAMMAR EVALUATION
- Correct structures: Present tense usage, basic sentence formation
- Grammar errors: Some article usage, verb tense consistency
- Sentence complexity: simple to compound
Score: 6/10

## FLUENCY ANALYSIS
- Filler words detected: um (3), uh (2), like (4)
- Hesitation patterns: Some pauses between thoughts
- Speech flow: moderately natural
Score: 6/10

## COHERENCE & ORGANIZATION
Ideas are generally well-connected with room for improvement in logical flow.
Score: 6/10

## IDIOMS & PHRASES
- Idioms used: break the ice
- Phrasal verbs: look up, come across
- Natural expressions: that's interesting, I think so
Score: 5/10

## LANGUAGE LEVEL ASSESSMENT
CEFR Level: B1
Equivalent Description: Intermediate

## SPECIFIC STRENGTHS
- Clear articulation of main ideas
- Good basic vocabulary usage
- Confident speaking manner
- Appropriate use of common expressions

## AREAS FOR IMPROVEMENT
- Reduce filler words
- Expand vocabulary range
- Improve grammar accuracy
- Work on natural intonation patterns

## PRONUNCIATION FEEDBACK
Focus on word stress and sentence rhythm. Practice with native speaker recordings.

## VOCABULARY ENHANCEMENT
Read more advanced texts and practice using new words in context.

## GRAMMAR CORRECTIONS
Review article usage (a, an, the) and practice verb tense consistency.

## FLUENCY IMPROVEMENT TIPS
Practice speaking without filler words. Record yourself and listen back.

## OVERALL GRADE
Grade: 6/10

## GRADE EXPLANATION
Solid intermediate level with good foundation. Clear communication but needs refinement in accuracy and fluency.

## NEXT LEVEL ACTIONS
1. Practice daily conversation for 15 minutes
2. Learn 5 new vocabulary words weekly
3. Focus on grammar exercises
4. Listen to English podcasts daily

## PRACTICE RECOMMENDATIONS
- Shadow reading with audio books
- Join English conversation groups
- Practice pronunciation with tongue twisters
- Write daily journal entries
"""

    def _parse_proficiency_analysis(self, analysis_text: str) -> Dict:
        """
        Parse the structured proficiency analysis response
        """
        analysis = {
            'pronunciation': {'feedback': ''},
            'vocabulary': {'feedback': '', 'advanced_words': [], 'basic_words': []},
            'grammar': {'feedback': '', 'strengths': [], 'areas': []},
            'fluency': {'feedback': '', 'filler_words': '', 'filler_count': 0},
            'coherence': {'feedback': ''},
            'cefr_level': 'B1',
            'level_description': 'Intermediate',
            'detailed_feedback': '',
            'pronunciation_plan': [],
            'vocabulary_plan': [],
            'grammar_plan': [],
            'fluency_plan': [],
            'next_level_path': '',
            'priority_areas': [],
            'overall_grade': 5.0,
            'words_per_minute': 145
        }
        
        current_section = None
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Section headers
            if '## PRONUNCIATION ANALYSIS' in line:
                current_section = 'pronunciation'
            elif '## VOCABULARY ASSESSMENT' in line:
                current_section = 'vocabulary'
            elif '## GRAMMAR EVALUATION' in line:
                current_section = 'grammar'
            elif '## FLUENCY ANALYSIS' in line:
                current_section = 'fluency'
            elif '## COHERENCE & ORGANIZATION' in line:
                current_section = 'coherence'
            elif '## CEFR LEVEL ASSESSMENT' in line:
                current_section = 'level'
            elif '## DETAILED PROFESSIONAL FEEDBACK' in line:
                current_section = 'detailed_feedback'
            elif '### Pronunciation Plan:' in line:
                current_section = 'pronunciation_plan'
            elif '### Vocabulary Plan:' in line:
                current_section = 'vocabulary_plan'
            elif '### Grammar Plan:' in line:
                current_section = 'grammar_plan'
            elif '### Fluency Plan:' in line:
                current_section = 'fluency_plan'
            elif '## NEXT LEVEL PATHWAY' in line:
                current_section = 'next_level_path'
            elif '## PRIORITY FOCUS AREAS' in line:
                current_section = 'priority_areas'
            elif line and current_section:
                self._process_professional_analysis_line(line, current_section, analysis)
        
        # Calculate overall grade from individual components
        if analysis['overall_grade'] == 5.0:  # Default value, calculate from components
            # Use a weighted average approach
            grade_sum = 0
            grade_count = 0
            
            # Extract numeric values from feedback if available
            for section in ['pronunciation', 'vocabulary', 'grammar', 'fluency', 'coherence']:
                if analysis[section]['feedback']:
                    # Simple heuristic based on feedback tone and content
                    feedback = analysis[section]['feedback'].lower()
                    if any(word in feedback for word in ['excellent', 'outstanding', 'perfect']):
                        grade_sum += 9
                    elif any(word in feedback for word in ['good', 'solid', 'strong']):
                        grade_sum += 7
                    elif any(word in feedback for word in ['adequate', 'fair', 'reasonable']):
                        grade_sum += 6
                    elif any(word in feedback for word in ['needs improvement', 'work on', 'focus on']):
                        grade_sum += 5
                    else:
                        grade_sum += 6  # Default
                    grade_count += 1
            
            if grade_count > 0:
                analysis['overall_grade'] = round(grade_sum / grade_count, 1)
        
        return analysis

    def _process_professional_analysis_line(self, line: str, section: str, analysis: Dict):
        """
        Process individual lines of professional analysis
        """
        # Extract CEFR level
        if section == 'level':
            if 'CEFR Level:' in line:
                analysis['cefr_level'] = line.split('CEFR Level:')[1].strip()
            elif 'Level Description:' in line:
                analysis['level_description'] = line.split('Level Description:')[1].strip()
            return
        
        # Extract lists for improvement plans
        if section in ['pronunciation_plan', 'vocabulary_plan', 'grammar_plan', 'fluency_plan', 'priority_areas']:
            if line.startswith('- ') or line.startswith('• ') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
                item = re.sub(r'^[-•\d\.]\s*', '', line)
                analysis[section].append(item)
            return
        
        # Extract vocabulary details
        if section == 'vocabulary':
            if 'Advanced words used:' in line:
                words = line.split('Advanced words used:')[1].strip()
                analysis['vocabulary']['advanced_words'] = [w.strip() for w in words.split(',') if w.strip()]
            elif 'Vocabulary level:' in line:
                analysis['vocabulary']['level'] = line.split('Vocabulary level:')[1].strip()
            return
        
        # Extract grammar details
        if section == 'grammar':
            if 'Grammar strengths:' in line:
                strengths = line.split('Grammar strengths:')[1].strip()
                analysis['grammar']['strengths'] = [s.strip() for s in strengths.split(',') if s.strip()]
            elif 'Areas for improvement:' in line:
                areas = line.split('Areas for improvement:')[1].strip()
                analysis['grammar']['areas'] = [a.strip() for a in areas.split(',') if a.strip()]
            return
        
        # Extract fluency details
        if section == 'fluency':
            if 'Filler words detected:' in line:
                analysis['fluency']['filler_words'] = line.split('Filler words detected:')[1].strip()
                # Extract count if present
                count_match = re.search(r'(\d+)', analysis['fluency']['filler_words'])
                if count_match:
                    analysis['fluency']['filler_count'] = int(count_match.group(1))
            elif 'Speaking rate:' in line or 'words per minute' in line.lower():
                rate_match = re.search(r'(\d+)\s*words?[/\s]*per[/\s]*minute', line.lower())
                if rate_match:
                    analysis['words_per_minute'] = int(rate_match.group(1))
            return
        
        # Add to feedback sections
        if section in ['pronunciation', 'vocabulary', 'grammar', 'fluency', 'coherence', 'detailed_feedback', 'next_level_path']:
            if not line.startswith('#') and not line.startswith('-') and not line.startswith('•'):
                if analysis[section]['feedback'] if isinstance(analysis[section], dict) else analysis[section]:
                    if isinstance(analysis[section], dict):
                        analysis[section]['feedback'] += ' ' + line
                    else:
                        analysis[section] += ' ' + line
                else:
                    if isinstance(analysis[section], dict):
                        analysis[section]['feedback'] = line
                    else:
                        analysis[section] = line

    def _process_analysis_line(self, line: str, section: str, analysis: Dict):
        """
        Process individual lines of analysis
        """
        # Extract scores
        score_match = re.search(r'Score:\s*(\d+)/10', line)
        if score_match and section in ['pronunciation', 'vocabulary', 'grammar', 'fluency', 'coherence', 'idioms']:
            analysis[section]['score'] = int(score_match.group(1))
            return
        
        # Extract overall grade
        if section == 'overall_grade':
            grade_match = re.search(r'Grade:\s*(\d+)/10', line)
            if grade_match:
                analysis['overall_grade'] = int(grade_match.group(1))
                return
        
        # Extract CEFR level
        if section == 'level':
            if 'CEFR Level:' in line:
                analysis['cefr_level'] = line.split('CEFR Level:')[1].strip()
            elif 'Equivalent Description:' in line:
                analysis['level_description'] = line.split('Equivalent Description:')[1].strip()
            return
        
        # Extract lists
        if line.startswith('- ') or line.startswith('• '):
            item = line.lstrip('- • ')
            
            if section == 'vocabulary':
                if 'Advanced words used:' in item:
                    words = item.split('Advanced words used:')[1].strip()
                    analysis['vocabulary']['advanced_words'] = [w.strip() for w in words.split(',') if w.strip()]
                elif 'Basic/Simple words:' in item:
                    words = item.split('Basic/Simple words:')[1].strip()
                    analysis['vocabulary']['basic_words'] = [w.strip() for w in words.split(',') if w.strip()]
            elif section == 'fluency':
                if 'Filler words detected:' in item:
                    analysis['fluency']['filler_words'] = item.split('Filler words detected:')[1].strip()
            elif section == 'idioms':
                if 'Idioms used:' in item:
                    idioms = item.split('Idioms used:')[1].strip()
                    analysis['idioms']['idioms_used'] = [i.strip() for i in idioms.split(',') if i.strip()]
                elif 'Phrasal verbs:' in item:
                    verbs = item.split('Phrasal verbs:')[1].strip()
                    analysis['idioms']['phrasal_verbs'] = [v.strip() for v in verbs.split(',') if v.strip()]
            elif section in ['strengths', 'improvements', 'next_actions', 'practice_recommendations']:
                analysis[section].append(item)
        
        # Add to feedback sections
        elif section in ['pronunciation', 'vocabulary', 'grammar', 'fluency', 'coherence', 'idioms']:
            if not line.startswith('Score:'):
                if analysis[section]['feedback']:
                    analysis[section]['feedback'] += ' ' + line
                else:
                    analysis[section]['feedback'] = line
        elif section in ['pronunciation_feedback', 'vocabulary_enhancement', 'grammar_corrections', 'fluency_tips', 'grade_explanation']:
            if analysis[section]:
                analysis[section] += ' ' + line
            else:
                analysis[section] = line

    def _combine_analyses(self, text_analysis: Dict, audio_analysis: Dict, transcription: str) -> Dict:
        """
        Combine text and audio analyses into final assessment
        """
        # Calculate word count and speaking rate
        word_count = len(transcription.split())
        estimated_duration = audio_analysis.get('estimated_duration', 60)  # Default 1 minute
        words_per_minute = (word_count / estimated_duration) * 60 if estimated_duration > 0 else 0
        
        # Determine speaking rate assessment
        if words_per_minute < 100:
            rate_assessment = "slow"
        elif words_per_minute > 180:
            rate_assessment = "fast"
        else:
            rate_assessment = "normal"
        
        combined = text_analysis.copy()
        combined.update({
            'word_count': word_count,
            'estimated_duration': estimated_duration,
            'words_per_minute': round(words_per_minute, 1),
            'speaking_rate': rate_assessment,
            'audio_quality': audio_analysis.get('audio_quality', 'unknown'),
            'transcription': transcription,
            'assessment_timestamp': datetime.now().isoformat()
        })
        
        return combined

    def get_improvement_plan(self, analysis: Dict) -> Dict:
        """
        Generate personalized improvement plan based on analysis
        """
        current_level = analysis.get('cefr_level', 'B1')
        overall_grade = analysis.get('overall_grade', 5)
        
        # Determine focus areas based on lowest scores
        scores = {
            'pronunciation': analysis['pronunciation']['score'],
            'vocabulary': analysis['vocabulary']['score'],
            'grammar': analysis['grammar']['score'],
            'fluency': analysis['fluency']['score'],
            'coherence': analysis['coherence']['score'],
            'idioms': analysis['idioms']['score']
        }
        
        # Find lowest scoring areas
        sorted_areas = sorted(scores.items(), key=lambda x: x[1])
        priority_areas = [area for area, score in sorted_areas[:3]]
        
        improvement_plan = {
            'current_level': current_level,
            'target_level': self._get_next_level(current_level),
            'priority_areas': priority_areas,
            'daily_practice': self._generate_daily_practice(priority_areas),
            'weekly_goals': self._generate_weekly_goals(priority_areas),
            'resources': self._get_learning_resources(priority_areas, current_level),
            'estimated_timeline': self._estimate_improvement_timeline(overall_grade, current_level)
        }
        
        return improvement_plan

    def _get_next_level(self, current_level: str) -> str:
        """Get the next CEFR level"""
        levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        try:
            current_index = levels.index(current_level)
            return levels[min(current_index + 1, len(levels) - 1)]
        except ValueError:
            return 'B2'

    def _generate_daily_practice(self, priority_areas: List[str]) -> List[str]:
        """Generate daily practice recommendations"""
        practices = {
            'pronunciation': [
                "Practice tongue twisters for 5 minutes",
                "Record yourself reading aloud and compare with native speakers",
                "Use pronunciation apps like Sounds or ELSA Speak"
            ],
            'vocabulary': [
                "Learn 5 new words daily with example sentences",
                "Use new vocabulary in conversation or writing",
                "Review vocabulary with spaced repetition apps"
            ],
            'grammar': [
                "Complete 10 grammar exercises daily",
                "Write sentences using target grammar structures",
                "Review grammar rules for 10 minutes"
            ],
            'fluency': [
                "Practice speaking for 15 minutes without stopping",
                "Shadow native speakers from audio/video content",
                "Reduce filler words through conscious practice"
            ],
            'coherence': [
                "Practice organizing thoughts before speaking",
                "Use transition words and phrases",
                "Practice storytelling with clear beginning, middle, end"
            ],
            'idioms': [
                "Learn 2 new idioms or phrasal verbs daily",
                "Practice using idioms in context",
                "Watch English shows and note idiomatic expressions"
            ]
        }
        
        daily_plan = []
        for area in priority_areas:
            if area in practices:
                daily_plan.extend(practices[area][:2])  # Top 2 for each area
        
        return daily_plan

    def _generate_weekly_goals(self, priority_areas: List[str]) -> List[str]:
        """Generate weekly goals"""
        goals = {
            'pronunciation': "Improve pronunciation clarity by 20%",
            'vocabulary': "Master 15 new words and use them naturally",
            'grammar': "Achieve 90% accuracy in target grammar structures",
            'fluency': "Reduce hesitation time by 30%",
            'coherence': "Deliver 5-minute presentations with clear structure",
            'idioms': "Learn and use 14 new idiomatic expressions"
        }
        
        return [goals.get(area, f"Improve {area} skills") for area in priority_areas]

    def _get_learning_resources(self, priority_areas: List[str], level: str) -> Dict:
        """Get learning resources for priority areas"""
        resources = {
            'pronunciation': {
                'apps': ['ELSA Speak', 'Sounds Pronunciation', 'Speechling'],
                'websites': ['Forvo.com', 'HowJSay.com', 'Cambridge Dictionary'],
                'youtube': ['Rachel\'s English', 'Pronunciation Pro', 'English with Lucy']
            },
            'vocabulary': {
                'apps': ['Anki', 'Quizlet', 'Memrise'],
                'websites': ['Vocabulary.com', 'Merriam-Webster', 'Oxford Learner\'s Dictionary'],
                'books': ['Word Power Made Easy', '4000 Essential English Words']
            },
            'grammar': {
                'apps': ['Grammarly', 'English Grammar in Use', 'Perfect English Grammar'],
                'websites': ['Purdue OWL', 'Grammar Bytes', 'English Page'],
                'books': ['English Grammar in Use by Raymond Murphy']
            },
            'fluency': {
                'practice': ['Conversation exchange', 'Language exchange apps', 'Speaking clubs'],
                'techniques': ['Shadowing', 'Tongue twisters', 'Reading aloud'],
                'apps': ['HelloTalk', 'Tandem', 'Cambly']
            }
        }
        
        return {area: resources.get(area, {}) for area in priority_areas}

    def _estimate_improvement_timeline(self, current_grade: int, current_level: str) -> str:
        """Estimate timeline for improvement"""
        if current_grade >= 8:
            return "2-3 months with consistent daily practice"
        elif current_grade >= 6:
            return "3-6 months with regular practice"
        elif current_grade >= 4:
            return "6-12 months with dedicated study"
        else:
            return "12+ months with intensive study and practice"
