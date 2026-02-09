(function () {
    // Configuration
    const API_URL = "http://localhost:8000/api/chat";
    const THEME_COLOR = "#6d28d9"; // Purple-ish

    // Create Styles
    const style = document.createElement('style');
    style.innerHTML = `
        .orbit-chat-widget-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 10000;
        }

        .orbit-chat-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, ${THEME_COLOR}, #4c1d95);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s, box-shadow 0.2s;
            border: none;
        }

        .orbit-chat-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        .orbit-chat-button svg {
            width: 30px;
            height: 30px;
            fill: white;
        }

        .orbit-chat-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid rgba(0,0,0,0.05);
            transition: opacity 0.3s ease, transform 0.3s ease;
            transform: translateY(20px);
            opacity: 0;
        }

        .orbit-chat-window.open {
            display: flex;
            opacity: 1;
            transform: translateY(0);
        }

        .orbit-chat-header {
            background: linear-gradient(135deg, ${THEME_COLOR}, #4c1d95);
            color: white;
            padding: 16px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .orbit-chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .orbit-message {
            max-width: 80%;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.4;
        }

        .orbit-message.bot {
            background: #f3f4f6;
            color: #1f2937;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }

        .orbit-message.user {
            background: ${THEME_COLOR};
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }

        .orbit-chat-input-area {
            padding: 16px;
            border-top: 1px solid #f3f4f6;
            display: flex;
            gap: 8px;
        }

        .orbit-chat-input {
            flex: 1;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            padding: 8px 16px;
            outline: none;
            transition: border-color 0.2s;
        }

        .orbit-chat-input:focus {
            border-color: ${THEME_COLOR};
        }

        .orbit-send-btn {
            background: transparent;
            border: none;
            color: ${THEME_COLOR};
            cursor: pointer;
            padding: 4px;
        }
        
        .orbit-send-btn:disabled {
            color: #9ca3af;
            cursor: not-allowed;
        }

        /* Loading Dots */
        .typing-indicator {
            display: flex;
            gap: 4px;
            padding: 4px 0;
        }
        .typing-dot {
            width: 6px;
            height: 6px;
            background: #6b7280;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);

    // Create Container
    const container = document.createElement('div');
    container.className = 'orbit-chat-widget-container';

    // Create Button
    const button = document.createElement('button');
    button.className = 'orbit-chat-button';
    button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
    `;

    // Create Window
    const windowEl = document.createElement('div');
    windowEl.className = 'orbit-chat-window';
    windowEl.innerHTML = `
        <div class="orbit-chat-header">
            <span>OrbitThink Assistant</span>
            <span style="cursor:pointer; font-size: 18px;" id="orbit-close-btn">&times;</span>
        </div>
        <div class="orbit-chat-messages" id="orbit-messages">
            <div class="orbit-message bot">Hello! How can I help you with OrbitThink services today?</div>
        </div>
        <div class="orbit-chat-input-area">
            <input type="text" class="orbit-chat-input" placeholder="Type a message..." id="orbit-input" />
            <button class="orbit-send-btn" id="orbit-send">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
            </button>
        </div>
    `;

    container.appendChild(windowEl);
    container.appendChild(button);
    document.body.appendChild(container);

    // Logic
    let isOpen = false;
    const messagesEl = windowEl.querySelector('#orbit-messages');
    const inputEl = windowEl.querySelector('#orbit-input');
    const sendBtn = windowEl.querySelector('#orbit-send');
    const closeBtn = windowEl.querySelector('#orbit-close-btn');

    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            windowEl.classList.add('open');
            inputEl.focus();
        } else {
            windowEl.classList.remove('open');
        }
    }

    button.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `orbit-message ${sender}`;
        div.textContent = text;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function addTypingIndicator() {
        const div = document.createElement('div');
        div.className = 'orbit-message bot typing-message';
        div.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
         `;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return div;
    }

    async function sendMessage() {
        const text = inputEl.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        inputEl.value = '';
        inputEl.disabled = true;
        sendBtn.disabled = true;

        const typingParams = addTypingIndicator();

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            typingParams.remove();

            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage("I'm having trouble connecting to my brain right now.", 'bot');
            }
        } catch (e) {
            typingParams.remove();
            addMessage("Sorry, I couldn't reach the server.", 'bot');
            console.error(e);
        } finally {
            inputEl.disabled = false;
            sendBtn.disabled = false;
            inputEl.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    inputEl.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

})();
