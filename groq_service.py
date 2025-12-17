"""
Groq AI Service - Fast & Powerful AI Assistant
Handles chatbot, study plan generation, and AI assistance
"""

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
import json


class GroqAIService:
    """Groq AI service for study assistance"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        
        if self.api_key and self.api_key != 'your_groq_api_key_here':
            try:
                self.client = Groq(api_key=self.api_key)
                self.is_available = True
            except Exception as e:
                print(f"Groq initialization error: {e}")
                self.is_available = False
        else:
            self.is_available = False
    
    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """
        Send chat request to Groq
        
        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            temperature: Response creativity (0-2)
            max_tokens: Maximum response length
        
        Returns:
            AI response text or error message
        """
        if not self.is_available:
            return self._get_fallback_response()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"❌ Error: {str(e)}\n\nPlease check your API key and try again."
    
    def generate_study_plan(self, subjects, study_hours_per_day, exam_date, current_level):
        """
        Generate personalized study plan
        
        Args:
            subjects: List of subject names
            study_hours_per_day: Available study hours
            exam_date: Target exam date
            current_level: Student's current level (beginner/intermediate/advanced)
        
        Returns:
            Detailed study plan as dict
        """
        if not self.is_available:
            return self._get_fallback_study_plan(subjects)
        
        prompt = f"""You are an expert study planner. Create a detailed, personalized study plan.

**Student Information:**
- Subjects: {', '.join(subjects)}
- Available study time: {study_hours_per_day} hours per day
- Target exam date: {exam_date}
- Current level: {current_level}

**Please provide:**
1. Weekly study schedule (which subjects on which days)
2. Time allocation for each subject
3. Recommended study techniques for each subject
4. Milestones and checkpoints
5. Study tips and motivation

Format your response as a detailed, actionable plan."""

        messages = [
            {"role": "system", "content": "You are an expert educational advisor and study planner."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat(messages, temperature=0.8, max_tokens=2000)
        return response
    
    def get_study_tips(self, subject, topic, difficulty):
        """
        Get study tips for specific topic
        
        Args:
            subject: Subject name
            topic: Specific topic
            difficulty: easy/medium/hard
        
        Returns:
            Study tips and explanations
        """
        if not self.is_available:
            return self._get_fallback_tips(subject, topic)
        
        prompt = f"""Provide detailed study tips and explanations for:

**Subject:** {subject}
**Topic:** {topic}
**Difficulty:** {difficulty}

Please include:
1. Key concepts to understand
2. Study strategies for this topic
3. Common mistakes to avoid
4. Practice recommendations
5. Memory techniques

Keep it practical and actionable."""

        messages = [
            {"role": "system", "content": "You are a helpful study coach and subject expert."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.7, max_tokens=1500)
    
    def explain_concept(self, subject, concept, detail_level="medium"):
        """
        Explain a concept in detail
        
        Args:
            subject: Subject name
            concept: Concept to explain
            detail_level: simple/medium/detailed
        
        Returns:
            Detailed explanation
        """
        if not self.is_available:
            return self._get_fallback_explanation(concept)
        
        detail_instructions = {
            "simple": "Explain like I'm 10 years old, using simple language and examples.",
            "medium": "Provide a clear explanation with examples and key points.",
            "detailed": "Provide an in-depth explanation with examples, applications, and technical details."
        }
        
        prompt = f"""Explain the following concept in {subject}:

**Concept:** {concept}

**Instruction:** {detail_instructions.get(detail_level, detail_instructions['medium'])}

Include:
- Clear definition
- Real-world examples
- Key points to remember
- Visual descriptions if helpful"""

        messages = [
            {"role": "system", "content": "You are an expert educator who explains concepts clearly."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.6, max_tokens=1500)
    
    def generate_practice_questions(self, subject, topic, count=5, difficulty="medium"):
        """
        Generate practice questions
        
        Args:
            subject: Subject name
            topic: Specific topic
            count: Number of questions
            difficulty: easy/medium/hard
        
        Returns:
            List of practice questions with answers
        """
        if not self.is_available:
            return self._get_fallback_questions(subject, topic, count)
        
        prompt = f"""Generate {count} practice questions for studying:

**Subject:** {subject}
**Topic:** {topic}
**Difficulty:** {difficulty}

For each question, provide:
1. The question
2. Multiple choice options (if applicable)
3. Correct answer
4. Brief explanation

Format clearly with numbering."""

        messages = [
            {"role": "system", "content": "You are an experienced teacher creating practice materials."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.8, max_tokens=2000)
    
    def analyze_study_progress(self, study_data):
        """
        Analyze study progress and provide recommendations
        
        Args:
            study_data: Dict with study statistics
        
        Returns:
            Analysis and recommendations
        """
        if not self.is_available:
            return self._get_fallback_analysis()
        
        prompt = f"""Analyze this student's study progress and provide personalized recommendations:

**Study Statistics:**
- Total study hours: {study_data.get('total_hours', 0)}
- Number of sessions: {study_data.get('sessions', 0)}
- Subjects studied: {', '.join(study_data.get('subjects', []))}
- Current streak: {study_data.get('streak', 0)} days
- Average session length: {study_data.get('avg_session', 0)} minutes

Provide:
1. Progress assessment
2. Strengths and areas for improvement
3. Specific recommendations
4. Motivation and encouragement"""

        messages = [
            {"role": "system", "content": "You are a supportive study coach analyzing student performance."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.7, max_tokens=1200)
    
    def create_study_summary(self, subject, topics_covered, time_spent):
        """
        Create study session summary
        
        Args:
            subject: Subject name
            topics_covered: List of topics studied
            time_spent: Time in minutes
        
        Returns:
            Study summary and next steps
        """
        if not self.is_available:
            return self._get_fallback_summary(subject, topics_covered)
        
        prompt = f"""Create a study session summary:

**Subject:** {subject}
**Topics Covered:** {', '.join(topics_covered)}
**Time Spent:** {time_spent} minutes

Provide:
1. Session recap
2. Key achievements
3. What to review next
4. Recommendations for next session"""

        messages = [
            {"role": "system", "content": "You are a study coach providing session feedback."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.7, max_tokens=800)
    
    # ==================== FALLBACK RESPONSES ====================
    
    def _get_fallback_response(self):
        """Fallback when API not available"""
        return """⚠️ AI Assistant Not Configured

To use Groq AI features:

1. Get free API key from: https://console.groq.com
2. Add it to config.py file
3. Restart the application

**In the meantime, here are some study tips:**

📚 **Active Learning:**
- Take notes by hand for better retention
- Explain concepts to yourself or others
- Practice retrieval (test yourself)

⏰ **Time Management:**
- Use Pomodoro technique (25 min focus + 5 min break)
- Study during your peak energy hours
- Take regular breaks to stay fresh

🎯 **Goal Setting:**
- Break large goals into smaller tasks
- Set specific, measurable targets
- Review progress weekly

💪 **Consistency:**
- Study a little bit every day
- Build a study routine
- Track your streaks"""
    
    def _get_fallback_study_plan(self, subjects):
        """Fallback study plan"""
        return f"""📚 Basic Study Plan Template

**Subjects:** {', '.join(subjects)}

**Weekly Schedule:**

Monday-Wednesday: Focus on {subjects[0] if subjects else 'Subject 1'}
Thursday-Friday: Focus on {subjects[1] if len(subjects) > 1 else 'Subject 2'}
Weekend: Review and practice all subjects

**Daily Routine:**
- Morning: 2 hours of focused study
- Evening: 1 hour of review and practice
- Before bed: 15 minutes of flashcard review

**Tips:**
1. Start with most difficult subjects when fresh
2. Use active recall techniques
3. Take regular breaks
4. Stay consistent

*Configure Groq API for personalized AI-generated plans!*"""
    
    def _get_fallback_tips(self, subject, topic):
        """Fallback study tips"""
        return f"""📖 General Study Tips for {subject} - {topic}

**Understanding:**
- Read the material thoroughly first
- Identify key concepts and definitions
- Look for patterns and connections

**Practice:**
- Solve practice problems regularly
- Explain concepts in your own words
- Create summary notes

**Review:**
- Review notes within 24 hours
- Use spaced repetition
- Test yourself frequently

*Configure Groq API for detailed, personalized tips!*"""
    
    def _get_fallback_explanation(self, concept):
        """Fallback explanation"""
        return f"""💡 About {concept}

This is a general placeholder explanation.

For detailed, AI-powered explanations:
1. Get Groq API key (free)
2. Add to config.py
3. Restart application

**Study Tips:**
- Break down complex concepts
- Use multiple resources
- Practice with examples
- Teach it to someone else"""
    
    def _get_fallback_questions(self, subject, topic, count):
        """Fallback questions"""
        return f"""❓ Practice Questions for {subject} - {topic}

To generate AI-powered practice questions:
1. Configure Groq API key
2. Restart application

**Study Recommendations:**
- Review your textbook exercises
- Look for online practice tests
- Create your own questions
- Join study groups

*AI-generated questions available with Groq API!*"""
    
    def _get_fallback_analysis(self):
        """Fallback analysis"""
        return """📊 Study Progress Analysis

Configure Groq API for personalized AI analysis!

**General Tips:**
- Consistency is key
- Track your study hours
- Review difficult topics more
- Celebrate small wins
- Stay motivated"""
    
    def _get_fallback_summary(self, subject, topics):
        """Fallback summary"""
        return f"""📝 Study Session Summary

**Subject:** {subject}
**Topics:** {', '.join(topics)}

Good work! Keep it up!

Configure Groq API for detailed AI-powered summaries."""


# Create global instance
groq_ai = GroqAIService()