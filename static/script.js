document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");
    const micBtn = document.getElementById("mic-button");

    let fullscreenRequested = false;
    const openFullscreen = () => {
        if (!fullscreenRequested) {
            const elem = document.documentElement;
            if (elem.requestFullscreen) elem.requestFullscreen().catch(() => {});
            fullscreenRequested = true;
        }
    };
    document.addEventListener("click", openFullscreen, { once: true });

    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendBtn.click();
        }
    });

    // Chatbot toggle logic
    const toggleBtn = document.getElementById("chatbot-toggle");
    const chatbotFrame = document.getElementById("chatbot-frame");
    toggleBtn.addEventListener("click", () => {
        chatbotFrame.classList.toggle("active");
    });

    input.addEventListener("input", function () {
        const typingId = "user-typing";
        const exists = document.getElementById(typingId);
        if (input.value.trim() !== "") {
            if (!exists) {
                const div = document.createElement("div");
                div.classList.add("message", "user-msg");
                div.id = typingId;
                div.innerHTML = `<span>Typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></span><img src="/static/user.png" class="avatar">`;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        } else {
            if (exists) exists.remove();
        }
    });

    function addMessage(message, type) {
        const div = document.createElement("div");
        div.classList.add("message", type === "user" ? "user-msg" : "bot-msg");
        if (type === "user") {
            div.innerHTML = `<span>${message}</span><img src="/static/user.png" class="avatar">`;
        } else {
            div.innerHTML = `<img src="/static/bot.png" class="avatar"><span class="typing-text"></span>`;
            typeBotMessage(message, div.querySelector(".typing-text"));
        }
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showBotTyping() {
        const div = document.createElement("div");
        div.classList.add("message", "bot-msg");
        div.id = "bot-typing";
        div.innerHTML = `<img src="/static/bot.png" class="avatar"><span>Typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></span>`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTyping() {
        const typingBot = document.getElementById("bot-typing");
        if (typingBot) typingBot.remove();
        const typingUser = document.getElementById("user-typing");
        if (typingUser) typingUser.remove();
    }

    function typeBotMessage(message, targetElement) {
        let index = 0;
        const speed = 20;

        function type() {
            if (index < message.length) {
                targetElement.textContent += message.charAt(index);
                index++;
                setTimeout(type, speed);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        type();
    }

    function speak(text) {
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-IN";
        speechSynthesis.speak(utterance);
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";

    let listeningMsg = null;

    recognition.onstart = function () {
        micBtn.classList.add("listening");

        listeningMsg = document.createElement("div");
        listeningMsg.classList.add("message", "bot-msg");
        listeningMsg.id = "listening-msg";
        listeningMsg.innerHTML = `<img src="/static/bot.png" class="avatar"><span>Listening...</span>`;
        chatBox.appendChild(listeningMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    recognition.onresult = function (event) {
        let spokenText = event.results[0][0].transcript;
        input.value = spokenText;
        sendBtn.click();
    };

    recognition.onend = function () {
        micBtn.classList.remove("listening");
        if (listeningMsg) {
            listeningMsg.remove();
            listeningMsg = null;
        }
    };

    micBtn.addEventListener("click", () => {
        recognition.start();
    });

    sendBtn.addEventListener("click", function () {
        const message = input.value.trim();
        if (!message) return;

        removeTyping();
        addMessage(message, "user");
        input.value = "";

        showBotTyping();

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                removeTyping();
                addMessage(data.response, "bot");
                speak(data.response);
            }, 1500);
        });
    });
});
