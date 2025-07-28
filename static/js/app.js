class EnglishFluencyCoach {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.recordingTimer = null;
        this.recordingStartTime = null;
        this.currentAssessmentType = null;
        this.currentPracticeType = null;
        
        this.init();
    }

    init() {
        console.log('🎤 Initializing English Fluency Coach...');
        this.setupEventListeners();
        this.checkMicrophonePermission();
        this.showSection('home');
    }

    setupEventListeners() {
        console.log('📝 Setting up event listeners...');
        
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href').substring(1);
                this.showSection(target);
            });
        });

        // Hero buttons
        document.getElementById('startAssessmentBtn')?.addEventListener('click', () => this.showSection('assessment'));
        document.getElementById('startPracticeBtn')?.addEventListener('click', () => this.showSection('practice'));

        // Assessment buttons
        document.getElementById('quickAssessmentBtn')?.addEventListener('click', () => this.startAssessment('quick'));
        document.getElementById('comprehensiveAssessmentBtn')?.addEventListener('click', () => this.startAssessment('comprehensive'));
        document.getElementById('topicAssessmentBtn')?.addEventListener('click', () => this.startTopicAssessment());

        // Recording controls
        document.getElementById('recordBtn')?.addEventListener('click', () => this.toggleRecording());
        document.getElementById('retryBtn')?.addEventListener('click', () => this.resetRecording());

        // Results buttons
        document.getElementById('goToPracticeBtn')?.addEventListener('click', () => this.showSection('practice'));
        document.getElementById('retakeAssessmentBtn')?.addEventListener('click', () => this.resetAssessment());

        // Practice cards
        document.querySelectorAll('.practice-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const practiceType = e.currentTarget.getAttribute('data-practice-type');
                if (practiceType) {
                    this.selectPracticeType(practiceType);
                }
            });
        });

        // Practice controls
        document.getElementById('practiceRecordBtn')?.addEventListener('click', () => this.togglePracticeRecording());
        document.getElementById('getNewPromptBtn')?.addEventListener('click', () => this.getNewPracticePrompt());
        document.getElementById('getCoachingBtn')?.addEventListener('click', () => this.getCoaching());
        document.getElementById('continuePracticeBtn')?.addEventListener('click', () => this.continuePractice());
        document.getElementById('changePracticeTypeBtn')?.addEventListener('click', () => this.changePracticeType());
    }

    async checkMicrophonePermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            console.log('✅ Microphone permission granted');
        } catch (error) {
            console.error('❌ Microphone permission denied:', error);
            this.showToast('Microphone access is required. Please allow microphone access and refresh.', 'error');
        }
    }

    showSection(sectionId) {
        console.log(`📍 Showing section: ${sectionId}`);
        
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        document.querySelector(`[href="#${sectionId}"]`)?.classList.add('active');

        // Show section
        document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
        document.getElementById(sectionId)?.classList.add('active');

        // Reset interfaces
        if (sectionId === 'assessment') {
            this.resetRecording();
            document.getElementById('recordingInterface')?.classList.add('hidden');
            document.getElementById('analysisResults')?.classList.add('hidden');
        } else if (sectionId === 'practice') {
            this.resetPracticeInterface();
        }
    }

    // ASSESSMENT FUNCTIONS
    startAssessment(type) {
        console.log(`🎯 Starting ${type} assessment`);
        this.currentAssessmentType = type;
        
        const assessmentConfig = {
            'quick': {
                title: 'Quick English Assessment',
                instructions: 'Speak for 2-3 minutes about any topic. Talk about your hobbies, work, or daily life. We\'ll analyze your English proficiency.'
            },
            'comprehensive': {
                title: 'Comprehensive English Assessment',
                instructions: 'Speak for 5-7 minutes. Cover different topics and show your full range of English skills. Talk about experiences, opinions, and future plans.'
            }
        };

        const config = assessmentConfig[type] || assessmentConfig['quick'];
        
        document.getElementById('recordingTitle').textContent = config.title;
        document.getElementById('recordingInstructions').textContent = config.instructions;
        document.getElementById('recordingInterface').classList.remove('hidden');
        
        this.resetRecording();
        this.showToast(`${config.title} ready! Click the microphone to start.`, 'success');
    }

    startTopicAssessment() {
        const topic = document.getElementById('assessmentTopic').value;
        console.log(`🎯 Starting topic assessment: ${topic}`);
        this.currentAssessmentType = 'topic';
        
        const topicName = topic.charAt(0).toUpperCase() + topic.slice(1);
        
        document.getElementById('recordingTitle').textContent = `Topic Assessment: ${topicName}`;
        document.getElementById('recordingInstructions').textContent = `Speak about ${topicName.toLowerCase()} for 3-5 minutes. Share your thoughts, experiences, and opinions naturally.`;
        document.getElementById('recordingInterface').classList.remove('hidden');

        this.resetRecording();
        this.showToast(`Topic assessment ready! Talk about ${topicName.toLowerCase()}.`, 'success');
    }

    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            console.log('🎤 Starting recording...');
            
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: { echoCancellation: true, noiseSuppression: true, sampleRate: 44100 }
            });

            this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
            this.audioChunks = [];
            this.isRecording = true;
            this.recordingStartTime = Date.now();

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => this.processRecording();
            this.mediaRecorder.start(1000);
            
            this.updateRecordingUI(true);
            this.startRecordingTimer();
            this.showToast('Recording started! Speak naturally.', 'success');

        } catch (error) {
            console.error('❌ Recording failed:', error);
            this.showToast('Failed to start recording. Check microphone permissions.', 'error');
        }
    }

    stopRecording() {
        console.log('⏹️ Stopping recording...');
        
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            this.isRecording = false;
            this.updateRecordingUI(false);
            this.stopRecordingTimer();
            this.showToast('Recording stopped! Processing...', 'info');
        }
    }

    updateRecordingUI(recording) {
        const recordBtn = document.getElementById('recordBtn');
        const recordingStatus = document.getElementById('recordingStatus');

        if (recordBtn) {
            if (recording) {
                recordBtn.classList.add('recording');
                recordBtn.innerHTML = '<i class="fas fa-stop"></i><span>Stop Recording</span>';
            } else {
                recordBtn.classList.remove('recording');
                recordBtn.innerHTML = '<i class="fas fa-microphone"></i><span>Start Recording</span>';
            }
        }

        if (recordingStatus) {
            recordingStatus.classList.toggle('hidden', !recording);
        }
    }

    startRecordingTimer() {
        this.recordingTimer = setInterval(() => {
            const elapsed = Date.now() - this.recordingStartTime;
            const minutes = Math.floor(elapsed / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            const timerDisplay = document.querySelector('.recording-timer');
            if (timerDisplay) {
                timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }

    stopRecordingTimer() {
        if (this.recordingTimer) {
            clearInterval(this.recordingTimer);
            this.recordingTimer = null;
        }
    }

    async processRecording() {
        if (this.audioChunks.length === 0) {
            this.showToast('No audio recorded. Please try again.', 'error');
            return;
        }

        console.log('🔄 Processing recording...');
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        await this.transcribeAndAnalyze(audioBlob);
    }

    async transcribeAndAnalyze(audioBlob) {
        this.showLoading('Analyzing your speech...');

        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        formData.append('type', this.currentAssessmentType || 'general');

        try {
            const response = await fetch('/analyze_speech', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.displayTranscription(result.transcription);
                if (result.analysis) {
                    this.displayAnalysis(result.analysis);
                }
                this.showToast('Speech analysis complete!', 'success');
            } else {
                this.showToast(result.error || 'Analysis failed. Please try again.', 'error');
            }

        } catch (error) {
            this.hideLoading();
            console.error('❌ Analysis error:', error);
            this.showToast('Failed to analyze speech. Check connection and try again.', 'error');
        }
    }

    displayTranscription(transcription) {
        document.getElementById('transcriptionText').textContent = transcription;
        document.getElementById('transcriptionResult').classList.remove('hidden');
        document.getElementById('retryBtn').classList.remove('hidden');
    }

    displayAnalysis(analysis) {
        console.log('📊 Displaying professional analysis:', analysis);
        
        // Update level and grade
        document.getElementById('overallGrade').textContent = analysis.overall_grade || '5.0';
        document.getElementById('cefrLevel').textContent = analysis.cefr_level || 'B1';
        document.getElementById('levelDescription').textContent = analysis.level_description || 'Intermediate';

        // Update detailed professional analysis
        document.getElementById('pronunciationAnalysis').textContent = 
            analysis.pronunciation?.feedback || 'Your pronunciation shows good clarity with room for improvement in stress patterns and intonation.';
        
        document.getElementById('vocabularyAnalysis').textContent = 
            analysis.vocabulary?.feedback || 'You demonstrate solid vocabulary usage. Focus on incorporating more sophisticated expressions and idiomatic language.';
        
        document.getElementById('grammarAnalysis').textContent = 
            analysis.grammar?.feedback || 'Your grammar foundation is strong. Work on complex sentence structures and advanced tense usage.';
        
        document.getElementById('fluencyAnalysis').textContent = 
            analysis.fluency?.feedback || 'Your speech flows naturally with minimal hesitation. Focus on reducing filler words and smoother transitions.';

        // Update vocabulary breakdown
        if (analysis.vocabulary?.advanced_words) {
            document.getElementById('advancedWords').textContent = analysis.vocabulary.advanced_words.join(', ');
        }

        // Update grammar strengths and areas
        this.updateList('grammarStrengths', analysis.grammar?.strengths || ['Accurate basic tense usage', 'Good sentence structure']);
        this.updateList('grammarAreas', analysis.grammar?.areas || ['Complex conditionals', 'Advanced connectors']);

        // Update fluency metrics
        document.getElementById('speakingRate').textContent = `${analysis.words_per_minute || 145} words/minute`;
        document.getElementById('fillerCount').textContent = `${analysis.fluency?.filler_count || 5} instances`;

        // Update improvement plans
        this.updateList('pronunciationPlan', analysis.pronunciation_plan || [
            'Practice tongue twisters daily for 10 minutes',
            'Record yourself reading and compare with native speakers',
            'Focus on word stress patterns'
        ]);

        this.updateList('vocabularyPlan', analysis.vocabulary_plan || [
            'Learn 5 advanced synonyms daily',
            'Study collocations and phrasal verbs',
            'Read academic articles in your field'
        ]);

        this.updateList('grammarPlan', analysis.grammar_plan || [
            'Practice conditional sentences daily',
            'Study advanced connectors',
            'Write complex sentences and get feedback'
        ]);

        this.updateList('fluencyPlan', analysis.fluency_plan || [
            'Practice speaking without filler words',
            'Use transition phrases between ideas',
            'Record yourself and identify patterns'
        ]);

        // Update next level path
        const nextLevelPath = document.getElementById('nextLevelPath');
        if (nextLevelPath) {
            nextLevelPath.innerHTML = `<p>${analysis.next_level_path || 'Continue practicing consistently to reach the next proficiency level. Focus on the priority areas identified above.'}</p>`;
        }

        document.getElementById('analysisResults').classList.remove('hidden');
        setTimeout(() => document.getElementById('analysisResults').scrollIntoView({ behavior: 'smooth' }), 100);
    }

    updateList(listId, items) {
        const list = document.getElementById(listId);
        if (list && Array.isArray(items) && items.length > 0) {
            list.innerHTML = items.map(item => `<li>${item}</li>`).join('');
        }
    }

    updateScoreBar(type, score, feedback) {
        const scoreElement = document.getElementById(`${type}Score`);
        const feedbackElement = document.getElementById(`${type}Feedback`);
        
        if (scoreElement) {
            scoreElement.style.width = `${(score / 10) * 100}%`;
            const scoreText = scoreElement.nextElementSibling;
            if (scoreText) scoreText.textContent = `${score}/10`;
        }
        
        if (feedbackElement) feedbackElement.textContent = feedback;
    }

    updateFeedbackList(listId, items) {
        const list = document.getElementById(listId);
        if (list && Array.isArray(items) && items.length > 0) {
            list.innerHTML = items.map(item => `<li>${item}</li>`).join('');
        }
    }

    resetRecording() {
        this.audioChunks = [];
        this.isRecording = false;
        this.stopRecordingTimer();
        this.updateRecordingUI(false);
        
        document.getElementById('transcriptionResult')?.classList.add('hidden');
        document.getElementById('analysisResults')?.classList.add('hidden');
        document.getElementById('retryBtn')?.classList.add('hidden');
    }

    resetAssessment() {
        this.resetRecording();
        document.getElementById('recordingInterface')?.classList.add('hidden');
        this.showToast('Assessment reset. Choose a new test type.', 'info');
    }

    // PRACTICE FUNCTIONS
    selectPracticeType(type) {
        console.log(`🎯 Selected practice type: ${type}`);
        this.currentPracticeType = type;
        
        // Update UI
        document.querySelectorAll('.practice-category').forEach(card => card.classList.remove('selected'));
        document.querySelector(`[data-practice-type="${type}"]`)?.classList.add('selected');

        const typeNames = {
            'conversation': 'Conversation Mastery',
            'pronunciation': 'Pronunciation Perfection',
            'vocabulary': 'Advanced Vocabulary',
            'storytelling': 'Narrative Excellence',
            'presentation': 'Professional Presentation',
            'song_analysis': 'Musical Language Learning'
        };

        document.getElementById('practiceTitle').textContent = typeNames[type] || 'Practice Session';
        document.getElementById('sessionType').textContent = typeNames[type] || 'Practice Session';
        document.getElementById('practiceInterface').classList.remove('hidden');
        
        this.getNewPracticePrompt();
        this.showToast(`${typeNames[type]} selected! Loading your personalized challenge...`, 'success');
    }

    async getNewPracticePrompt() {
        if (!this.currentPracticeType) return;

        this.showLoading('Generating practice prompt...');

        const level = document.getElementById('practiceLevel').value;
        const topic = document.getElementById('practiceTopic').value;

        try {
            const response = await fetch('/get_practice_prompt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: this.currentPracticeType,
                    topic: topic,
                    level: level
                })
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                document.getElementById('promptText').textContent = result.prompt.prompt;
                document.getElementById('promptInstructions').textContent = result.prompt.instructions;
                
                // Reset practice session
                document.getElementById('practiceTranscription')?.classList.add('hidden');
                document.getElementById('coachingFeedback')?.classList.add('hidden');
            } else {
                this.showToast(result.error || 'Failed to generate prompt', 'error');
            }

        } catch (error) {
            this.hideLoading();
            console.error('❌ Prompt generation error:', error);
            this.showToast('Failed to generate practice prompt', 'error');
        }
    }

    async togglePracticeRecording() {
        const btn = document.getElementById('practiceRecordBtn');
        const status = document.getElementById('practiceRecordingStatus');
        
        if (this.isRecording) {
            this.stopRecording();
            btn.innerHTML = `
                <div class="btn-icon"><i class="fas fa-microphone"></i></div>
                <div class="btn-content">
                    <span class="btn-text">Start Speaking</span>
                    <span class="btn-subtext">Click to begin recording</span>
                </div>
            `;
            status?.classList.add('hidden');
            this.stopPracticeTimer();
        } else {
            await this.startPracticeRecording();
            btn.innerHTML = `
                <div class="btn-icon"><i class="fas fa-stop"></i></div>
                <div class="btn-content">
                    <span class="btn-text">Stop Recording</span>
                    <span class="btn-subtext">Click to finish</span>
                </div>
            `;
            btn.classList.add('recording');
            status?.classList.remove('hidden');
            this.startPracticeTimer();
        }
    }

    startPracticeTimer() {
        const timer = document.getElementById('practiceTimer');
        let seconds = 0;
        
        this.practiceTimer = setInterval(() => {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            if (timer) {
                timer.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }

    stopPracticeTimer() {
        if (this.practiceTimer) {
            clearInterval(this.practiceTimer);
            this.practiceTimer = null;
        }
    }

    async startPracticeRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: { echoCancellation: true, noiseSuppression: true, sampleRate: 44100 }
            });

            this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
            this.audioChunks = [];
            this.isRecording = true;

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => this.processPracticeRecording();
            this.mediaRecorder.start(1000);

        } catch (error) {
            console.error('❌ Practice recording failed:', error);
            this.showToast('Failed to start recording', 'error');
        }
    }

    async processPracticeRecording() {
        if (this.audioChunks.length === 0) {
            this.showToast('No audio recorded', 'error');
            return;
        }

        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        await this.transcribePracticeAudio(audioBlob);
    }

    async transcribePracticeAudio(audioBlob) {
        this.showLoading('Transcribing your speech...');

        const formData = new FormData();
        formData.append('audio', audioBlob, 'practice.wav');

        try {
            const response = await fetch('/transcribe_audio', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                document.getElementById('practiceTranscriptionText').textContent = result.transcription;
                document.getElementById('practiceTranscription').classList.remove('hidden');
                document.getElementById('coachingFeedback')?.classList.add('hidden');
            } else {
                this.showToast(result.error || 'Transcription failed', 'error');
            }

        } catch (error) {
            this.hideLoading();
            console.error('❌ Practice transcription error:', error);
            this.showToast('Failed to transcribe audio', 'error');
        }
    }

    async getCoaching() {
        const transcription = document.getElementById('practiceTranscriptionText').textContent;
        if (!transcription) {
            this.showToast('No transcription available', 'error');
            return;
        }

        this.showLoading('Getting personalized coaching...');

        const level = document.getElementById('practiceLevel').value;
        const topic = document.getElementById('practiceTopic').value;

        try {
            const response = await fetch('/practice_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: this.currentPracticeType,
                    topic: topic,
                    input: transcription,
                    level: level
                })
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.displayCoaching(result.coaching);
            } else {
                this.showToast(result.error || 'Coaching failed', 'error');
            }

        } catch (error) {
            this.hideLoading();
            console.error('❌ Coaching error:', error);
            this.showToast('Failed to get coaching feedback', 'error');
        }
    }

    displayCoaching(coaching) {
        // Update coaching sections
        document.getElementById('immediateFeedback').textContent = coaching.immediate_feedback || 'Great effort!';
        document.getElementById('pronunciationTips').textContent = coaching.pronunciation_notes || 'Keep practicing your pronunciation';
        document.getElementById('vocabularyTips').textContent = coaching.vocabulary_enhancement?.join('. ') || 'Expand your vocabulary';
        document.getElementById('fluencyTips').textContent = coaching.fluency_tips || 'Work on fluency';
        document.getElementById('encouragementText').textContent = coaching.encouragement || 'Keep up the good work!';
        document.getElementById('nextChallenge').textContent = coaching.next_challenge || 'Try more complex sentences';

        // Update corrections
        const correctionsList = document.getElementById('correctionsList');
        if (coaching.corrections && coaching.corrections.length > 0) {
            correctionsList.innerHTML = coaching.corrections.map(correction => `
                <div class="correction-item">
                    <div class="correction-original">Original: ${correction}</div>
                </div>
            `).join('');
        } else {
            correctionsList.innerHTML = '<p>No major corrections needed!</p>';
        }

        document.getElementById('coachingFeedback').classList.remove('hidden');
        setTimeout(() => document.getElementById('coachingFeedback').scrollIntoView({ behavior: 'smooth' }), 100);
    }

    continuePractice() {
        this.getNewPracticePrompt();
    }

    changePracticeType() {
        document.getElementById('practiceInterface')?.classList.add('hidden');
        document.querySelectorAll('.practice-card').forEach(card => card.classList.remove('selected'));
        this.currentPracticeType = null;
    }

    resetPracticeInterface() {
        this.currentPracticeType = null;
        document.querySelectorAll('.practice-category').forEach(card => card.classList.remove('selected'));
        document.getElementById('practiceInterface')?.classList.add('hidden');
    }

    // UTILITY FUNCTIONS
    showLoading(message = 'Processing...') {
        document.getElementById('loadingText').textContent = message;
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }

    showToast(message, type = 'info') {
        console.log(`📢 Toast: ${message} (${type})`);
        
        const container = document.getElementById('toastContainer');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const iconMap = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-${iconMap[type] || 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        container.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }, 5000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fluencyCoach = new EnglishFluencyCoach();
    console.log('🎤 English Fluency Coach initialized and ready!');
});
