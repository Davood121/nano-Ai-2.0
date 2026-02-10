// ===== SETTINGS PANEL FUNCTIONALITY =====

const settingsBtn = document.getElementById('settings-btn');
const settingsPanel = document.getElementById('settings-panel');
const closeSettings = document.getElementById('close-settings');
const saveSettings = document.getElementById('save-settings');
const resetSettings = document.getElementById('reset-settings');
const modelSelect = document.getElementById('model-select');

// Sliders
const contextSlider = document.getElementById('context-slider');
const tokensSlider = document.getElementById('tokens-slider');
const tempSlider = document.getElementById('temp-slider');
const toppSlider = document.getElementById('topp-slider');

// Value displays
const contextValue = document.getElementById('context-value');
const tokensValue = document.getElementById('tokens-value');
const tempValue = document.getElementById('temp-value');
const toppValue = document.getElementById('topp-value');

// Preset buttons
const presetBtns = document.querySelectorAll('.preset-btn');

// Toggle settings panel
settingsBtn.addEventListener('click', () => {
    settingsPanel.classList.add('open');
    loadCurrentSettings();
    loadAvailableModels();
});

closeSettings.addEventListener('click', () => {
    settingsPanel.classList.remove('open');
});

// Update slider value displays
contextSlider.addEventListener('input', (e) => {
    contextValue.textContent = e.target.value;
});

tokensSlider.addEventListener('input', (e) => {
    tokensValue.textContent = e.target.value;
});

tempSlider.addEventListener('input', (e) => {
    tempValue.textContent = parseFloat(e.target.value).toFixed(1);
});

toppSlider.addEventListener('input', (e) => {
    toppValue.textContent = parseFloat(e.target.value).toFixed(1);
});

// Load available Ollama models
async function loadAvailableModels() {
    try {
        const response = await fetch('http://localhost:8000/api/models');
        const data = await response.json();

        if (data.models && data.models.length > 0) {
            modelSelect.innerHTML = '';
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.name;
                option.textContent = `${model.name} (${model.size})`;
                modelSelect.appendChild(option);
            });
        } else {
            modelSelect.innerHTML = '<option value="">No models found</option>';
        }
    } catch (error) {
        console.error('Failed to load models:', error);
        modelSelect.innerHTML = '<option value="">Error loading models</option>';
    }
}

// Load current settings from backend
async function loadCurrentSettings() {
    try {
        const response = await fetch('http://localhost:8000/api/settings');
        const settings = await response.json();

        // Update UI with current settings
        if (settings.model_name) {
            modelSelect.value = settings.model_name;
        }
        contextSlider.value = settings.context_window || 2048;
        contextValue.textContent = settings.context_window || 2048;

        tokensSlider.value = settings.max_tokens || 512;
        tokensValue.textContent = settings.max_tokens || 512;

        tempSlider.value = settings.temperature || 0.7;
        tempValue.textContent = (settings.temperature || 0.7).toFixed(1);

        toppSlider.value = settings.top_p || 0.9;
        toppValue.textContent = (settings.top_p || 0.9).toFixed(1);
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
}

// Save settings to backend
saveSettings.addEventListener('click', async () => {
    const settings = {
        model_name: modelSelect.value,
        context_window: parseInt(contextSlider.value),
        max_tokens: parseInt(tokensSlider.value),
        temperature: parseFloat(tempSlider.value),
        top_p: parseFloat(toppSlider.value)
    };

    try {
        const response = await fetch('http://localhost:8000/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        const result = await response.json();

        if (result.status === 'success') {
            // Show success feedback
            saveSettings.textContent = '✓ Saved!';
            saveSettings.classList.add('bg-emerald-500');

            setTimeout(() => {
                saveSettings.textContent = 'Save Settings';
                saveSettings.classList.remove('bg-emerald-500');
                settingsPanel.classList.remove('open');
            }, 1500);

            // Save to localStorage
            localStorage.setItem('nanoai_settings', JSON.stringify(settings));
        } else {
            alert('Failed to save settings: ' + result.message);
        }
    } catch (error) {
        console.error('Failed to save settings:', error);
        alert('Failed to save settings. Check console for details.');
    }
});

// Reset to defaults
resetSettings.addEventListener('click', () => {
    contextSlider.value = 2048;
    contextValue.textContent = '2048';

    tokensSlider.value = 512;
    tokensValue.textContent = '512';

    tempSlider.value = 0.7;
    tempValue.textContent = '0.7';

    toppSlider.value = 0.9;
    toppValue.textContent = '0.9';
});

// Preset configurations
const presets = {
    speed: {
        context_window: 1024,
        max_tokens: 256,
        temperature: 0.3,
        top_p: 0.8
    },
    balanced: {
        context_window: 2048,
        max_tokens: 512,
        temperature: 0.7,
        top_p: 0.9
    },
    quality: {
        context_window: 4096,
        max_tokens: 1024,
        temperature: 0.9,
        top_p: 0.95
    }
};

// Apply presets
presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const preset = btn.dataset.preset;
        const config = presets[preset];

        if (config) {
            contextSlider.value = config.context_window;
            contextValue.textContent = config.context_window;

            tokensSlider.value = config.max_tokens;
            tokensValue.textContent = config.max_tokens;

            tempSlider.value = config.temperature;
            tempValue.textContent = config.temperature.toFixed(1);

            toppSlider.value = config.top_p;
            toppValue.textContent = config.top_p.toFixed(1);

            // Visual feedback
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = 'scale(1)';
            }, 100);
        }
    });
});

// Load settings from localStorage on page load
window.addEventListener('load', () => {
    const saved = localStorage.getItem('nanoai_settings');
    if (saved) {
        const settings = JSON.parse(saved);
        // Settings will be loaded when panel opens
    }
});
