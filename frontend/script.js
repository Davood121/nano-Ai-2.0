const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const statusIndicator = document.getElementById('status-indicator');
const moodText = document.getElementById('mood-text');
const thinkingIndicator = document.getElementById('thinking-indicator');
const voiceToggle = document.getElementById('voice-toggle');
const voiceIcon = document.getElementById('voice-icon');
const speakingIndicator = document.getElementById('speaking-indicator');

let socket;
let isConnected = false;
let voiceEnabled = false;
let currentEmotion = { calm: 0.5, stress: 0.1, focus: 0.5, joy: 0.3, curiosity: 0.4 };

// Initialize Speech Synthesis
const synth = window.speechSynthesis;
let selectedVoice = null;

// Load available voices
function loadVoices() {
    const voices = synth.getVoices();
    // Prefer natural-sounding English voices
    selectedVoice = voices.find(v => v.lang.startsWith('en') && v.name.includes('Natural'))
        || voices.find(v => v.lang.startsWith('en'))
        || voices[0];
}

// Load voices when available
if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = loadVoices;
}
loadVoices();

function connectWebSocket() {
    socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
        console.log("Connected to AI Core");
        isConnected = true;
        statusIndicator.classList.add('bg-emerald-500', 'shadow-[0_0_10px_#10b981]');
        statusIndicator.classList.remove('bg-red-500');
        moodText.innerText = "ONLINE - LISTENING";
    };

    socket.onclose = () => {
        console.log("Disconnected");
        isConnected = false;
        statusIndicator.classList.remove('bg-emerald-500', 'shadow-[0_0_10px_#10b981]');
        statusIndicator.classList.add('bg-red-500');
        moodText.innerText = "OFFLINE - RECONNECTING...";
        setTimeout(connectWebSocket, 3000);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleAIResponse(data);
    };
}

function handleAIResponse(data) {
    // Hide thinking indicator
    gsap.to(thinkingIndicator, { opacity: 0, duration: 0.3, display: 'none' });

    // Update Mood/UI based on emotion
    updateEmotionUI(data.emotion_state);

    // Add Message with sources and images if search was performed
    addMessage(data.text, 'ai', data.sources || [], data.images || []);

    // Play audio if voice is enabled and audio URL is provided
    if (voiceEnabled && data.audio_url) {
        playAudio(data.audio_url);
    }
}

function playAudio(audioUrl) {
    // Show speaking indicator
    speakingIndicator.classList.remove('hidden');
    speakingIndicator.classList.add('flex');

    const audio = new Audio(`http://localhost:8000${audioUrl}`);

    audio.onended = () => {
        speakingIndicator.classList.add('hidden');
        speakingIndicator.classList.remove('flex');
    };

    audio.onerror = (e) => {
        console.error('Audio playback error:', e);
        speakingIndicator.classList.add('hidden');
        speakingIndicator.classList.remove('flex');
    };

    audio.play().catch(err => {
        console.error('Failed to play audio:', err);
        speakingIndicator.classList.add('hidden');
        speakingIndicator.classList.remove('flex');
    });
}

function speak(text, emotion) {
    if (!synth || !selectedVoice) return;

    // Preprocess text to remove markdown and clean it up
    let cleanText = text
        // Remove markdown headers (##, ###, etc.)
        .replace(/^#{1,6}\s+/gm, '')
        // Remove bold/italic markers
        .replace(/\*\*(.+?)\*\*/g, '$1')
        .replace(/\*(.+?)\*/g, '$1')
        .replace(/__(.+?)__/g, '$1')
        .replace(/_(.+?)_/g, '$1')
        // Remove code blocks
        .replace(/```[\s\S]*?```/g, '')
        .replace(/`(.+?)`/g, '$1')
        // Remove links but keep text
        .replace(/\[(.+?)\]\(.+?\)/g, '$1')
        // Remove list markers
        .replace(/^\s*[-*+]\s+/gm, '')
        .replace(/^\s*\d+\.\s+/gm, '')
        // Clean up extra whitespace
        .replace(/\n{3,}/g, '\n\n')
        .trim();

    if (!cleanText) return;

    // Cancel any ongoing speech
    synth.cancel();

    // Small delay to ensure cancel completes
    setTimeout(() => {
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.voice = selectedVoice;

        // Emotion-adaptive voice parameters
        let pitch = 1.0;
        let rate = 1.0;
        let volume = 1.0;

        // Adjust based on emotion
        if (emotion.stress > 0.6) {
            rate = 1.15; // Slightly faster when stressed (reduced from 1.2)
            pitch = 1.05;
        } else if (emotion.calm > 0.6) {
            rate = 0.92; // Slower when calm
            pitch = 0.97;
        } else if (emotion.joy > 0.6) {
            pitch = 1.1; // Higher pitch when joyful
            rate = 1.08;
        } else if (emotion.focus > 0.6) {
            rate = 0.95; // Measured when focused
            pitch = 1.0;
        }

        utterance.pitch = pitch;
        utterance.rate = rate;
        utterance.volume = volume;

        // Show speaking indicator
        speakingIndicator.classList.remove('hidden');
        speakingIndicator.classList.add('flex');

        utterance.onend = () => {
            speakingIndicator.classList.add('hidden');
            speakingIndicator.classList.remove('flex');
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            speakingIndicator.classList.add('hidden');
            speakingIndicator.classList.remove('flex');
        };

        synth.speak(utterance);
    }, 100);
}

function updateEmotionUI(emotion) {
    // Store current emotion
    currentEmotion = emotion;

    // Update emotion bars
    updateEmotionBar('calm', emotion.calm || 0.5);
    updateEmotionBar('stress', emotion.stress || 0.1);
    updateEmotionBar('joy', emotion.joy || 0.3);
    updateEmotionBar('focus', emotion.focus || 0.5);
    updateEmotionBar('curiosity', emotion.curiosity || 0.4);

    // Determine dominant emotion
    let color = '#10b981';
    let moodStatus = "Balanced";

    if (emotion.stress > 0.6) {
        color = '#ef4444';
        moodStatus = "Stressed";
    } else if (emotion.joy > 0.6) {
        color = '#f59e0b';
        moodStatus = "Joyful";
    } else if (emotion.focus > 0.6) {
        color = '#8b5cf6';
        moodStatus = "Focused";
    } else if (emotion.calm > 0.6) {
        color = '#06b6d4';
        moodStatus = "Calm";
    }

    // Update status indicator
    gsap.to(statusIndicator, {
        backgroundColor: color,
        boxShadow: `0 0 20px ${color}`,
        duration: 1
    });

    // Update mood text
    moodText.innerText = moodStatus;

    // Update background orbs based on emotion
    updateBackgroundOrbs(emotion);
}

function updateEmotionBar(emotionName, value) {
    const percentage = Math.round(value * 100);
    const bar = document.getElementById(`${emotionName}-bar`);
    const valueText = document.getElementById(`${emotionName}-value`);

    if (bar && valueText) {
        gsap.to(bar, {
            width: `${percentage}%`,
            duration: 0.8,
            ease: "power2.out"
        });
        valueText.innerText = `${percentage}%`;
    }
}

function updateBackgroundOrbs(emotion) {
    const orb1 = document.getElementById('bg-orb-1');
    const orb2 = document.getElementById('bg-orb-2');
    const orb3 = document.getElementById('bg-orb-3');

    if (emotion.stress > 0.6) {
        gsap.to(orb1, { opacity: 0.4, duration: 2 });
        gsap.to(orb2, { opacity: 0.3, duration: 2 });
    } else if (emotion.calm > 0.6) {
        gsap.to(orb1, { opacity: 0.25, duration: 2 });
        gsap.to(orb3, { opacity: 0.3, duration: 2 });
    } else {
        gsap.to(orb1, { opacity: 0.3, duration: 2 });
        gsap.to(orb2, { opacity: 0.3, duration: 2 });
        gsap.to(orb3, { opacity: 0.2, duration: 2 });
    }
}

function addMessage(text, sender, sources = []) {
    const div = document.createElement('div');
    div.className = sender === 'ai' ? 'ai-message opacity-0 translate-y-2' : 'user-message opacity-0 translate-y-2';

    if (sender === 'ai') {
        // AI message with avatar
        let sourcesHTML = '';
        if (sources && sources.length > 0) {
            sourcesHTML = '<div class="mt-3 pt-3 border-t border-white/10">';
            sourcesHTML += '<div class="text-xs text-white/50 mb-2">🔍 Sources:</div>';
            sources.slice(0, 3).forEach((url, i) => {
                const domain = new URL(url).hostname.replace('www.', '');
                sourcesHTML += `<a href="${url}" target="_blank" class="inline-block text-xs text-cyan-400 hover:text-cyan-300 mr-3 mb-1 hover:underline">${i + 1}. ${domain}</a>`;
            });
            sourcesHTML += '</div>';
        }

        div.innerHTML = `
            <div class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center flex-shrink-0">
                    <span class="text-xs font-bold">AI</span>
                </div>
                <div class="message-bubble ai-bubble">
                    <p class="text-white/90 leading-relaxed">${text}</p>
                    ${sourcesHTML}
                </div>
            </div>
        `;
    } else {
        // User message with avatar
        div.innerHTML = `
            <div class="flex items-start gap-3 justify-end">
                <div class="message-bubble user-bubble">
                    <p class="text-white/90 leading-relaxed">${text}</p>
                </div>
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center flex-shrink-0">
                    <span class="text-xs font-bold">U</span>
                </div>
            </div>
        `;
    }

    chatContainer.appendChild(div);

    // GSAP Entry Animation
    gsap.to(div, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" });

    // Scroll to bottom smoothly
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    if (isConnected) {
        addMessage(text, 'user');
        socket.send(text);
        userInput.value = '';

        // Show thinking
        thinkingIndicator.style.display = 'flex';
        gsap.to(thinkingIndicator, { opacity: 1, duration: 0.3 });
    } else {
        addMessage("System offline. Connecting...", 'user');
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Voice Toggle
voiceToggle.addEventListener('click', () => {
    voiceEnabled = !voiceEnabled;

    if (voiceEnabled) {
        voiceIcon.classList.add('text-cyan-400');
        voiceIcon.classList.remove('text-white/60');
        // Optional: speak a confirmation
        const testUtterance = new SpeechSynthesisUtterance("Voice output enabled.");
        testUtterance.voice = selectedVoice;
        synth.speak(testUtterance);
    } else {
        voiceIcon.classList.remove('text-cyan-400');
        voiceIcon.classList.add('text-white/60');
        synth.cancel(); // Stop any ongoing speech
    }
});

// Initial Connection
connectWebSocket();
