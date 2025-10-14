function showTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
        typingIndicator.style.display = "block";
    }
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
        typingIndicator.style.display = "none";
    }
}

function addMessage(content, isUser = false) {
    const chatHistory = document.getElementById("chat-history");
    if (!chatHistory) return;
    
    const messageDiv = document.createElement("div");
    messageDiv.className = `message animated-message ${isUser ? 'user-message' : 'bot-message'} new-message`;
    messageDiv.innerHTML = content;
    
    const messageCount = chatHistory.children.length;
    messageDiv.style.animationDelay = `${messageCount * 0.1}s`;
    
    chatHistory.appendChild(messageDiv);
    
    smoothScrollToBottom();
    
    setTimeout(() => {
        messageDiv.style.animation = 'float 3s ease-in-out infinite';
    }, 500);
    
    return messageDiv;
}

function smoothScrollToBottom() {
    const chatHistory = document.getElementById("chat-history");
    if (!chatHistory) return;
    
    chatHistory.scrollTo({
        top: chatHistory.scrollHeight,
        behavior: 'smooth'
    });
}

function autoScrollToBottom() {
    const chatHistory = document.getElementById("chat-history");
    if (!chatHistory) return;
    
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function simulateTyping(content, callback) {
    const chatHistory = document.getElementById("chat-history");
    if (!chatHistory) return;
    
    const messageDiv = document.createElement("div");
    messageDiv.className = "message bot-message new-message";
    chatHistory.appendChild(messageDiv);
    
    autoScrollToBottom();
    
    let i = 0;
    const speed = 20;
    
    function typeWriter() {
        if (i < content.length) {
            messageDiv.innerHTML += content.charAt(i);
            i++;
            
            autoScrollToBottom();
            
            setTimeout(typeWriter, speed);
        } else {
            if (callback) callback();
        }
    }
    
    typeWriter();
}

function processAIQuery(query) {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('world') || lowerQuery.includes('global') || 
        lowerQuery.includes('legal system') || lowerQuery.includes('law system')) {
        return {
            type: 'world_info',
            content: generateWorldLegalInfo(lowerQuery)
        };
    }
    
    if (lowerQuery.includes('statistic') || lowerQuery.includes('data') || 
        lowerQuery.includes('number') || lowerQuery.includes('how many')) {
        return {
            type: 'statistics',
            content: generateLegalStatistics(lowerQuery)
        };
    }
    
    if (lowerQuery.includes('compare') || lowerQuery.includes('difference') || 
        lowerQuery.includes('vs') || lowerQuery.includes('versus')) {
        return {
            type: 'comparison',
            content: generateLegalComparison(lowerQuery)
        };
    }
    
    return {
        type: 'chat',
        content: null
    };
}

function generateWorldLegalInfo(query) {
    return `
        <div class="ai-response-card">
            <h3><i class="fas fa-globe-americas"></i> Global Legal Systems Overview</h3>
            <p>Based on your query about world legal information, here's what I can tell you:</p>
            <div class="ai-insight-grid">
                <div class="ai-insight-item">
                    <h4><i class="fas fa-balance-scale"></i> Common Law</h4>
                    <p>Used in UK, USA, Canada, Australia, India. Based on precedent and judicial decisions.</p>
                </div>
                <div class="ai-insight-item">
                    <h4><i class="fas fa-landmark"></i> Civil Law</h4>
                    <p>Used in most of Europe, Latin America. Based on comprehensive legal codes.</p>
                </div>
                <div class="ai-insight-item">
                    <h4><i class="fas fa-umbrella-beach"></i> Religious Law</h4>
                    <p>Based on religious texts. Examples: Sharia law, Halakha, Canon law.</p>
                </div>
                <div class="ai-insight-item">
                    <h4><i class="fas fa-chess-board"></i> Customary Law</h4>
                    <p>Based on customs and traditions. Often found in indigenous communities.</p>
                </div>
            </div>
            <div class="ai-recommendation">
                <p><strong>AI Recommendation:</strong> For international legal research, understanding these fundamental differences is crucial for cross-border legal matters.</p>
            </div>
        </div>
    `;
}

function generateLegalStatistics(query) {
    return `
        <div class="ai-response-card">
            <h3><i class="fas fa-chart-bar"></i> Global Legal Statistics</h3>
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="stat-number">200+</div>
                    <div class="stat-label">Countries with Legal Systems</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">~30%</div>
                    <div class="stat-label">Common Law Systems</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">~70%</div>
                    <div class="stat-label">Civil Law Systems</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">10M+</div>
                    <div class="stat-label">Legal Professionals</div>
                </div>
            </div>
            <div class="ai-analysis">
                <p><strong>AI Analysis:</strong> The majority of countries use civil law systems, which are based on comprehensive legal codes rather than judicial precedent. Common law systems, while fewer in number, include some of the world's largest economies.</p>
            </div>
        </div>
    `;
}

function generateLegalComparison(query) {
    return `
        <div class="ai-response-card">
            <h3><i class="fas fa-balance-scale"></i> Legal System Comparison</h3>
            <div class="comparison-container">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th>Common Law</th>
                            <th>Civil Law</th>
                            <th>Religious Law</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Primary Source</td>
                            <td>Judicial Precedent</td>
                            <td>Statutory Codes</td>
                            <td>Religious Texts</td>
                        </tr>
                        <tr>
                            <td>Role of Judges</td>
                            <td>Law Creators</td>
                            <td>Law Appliers</td>
                            <td>Interpreters</td>
                        </tr>
                        <tr>
                            <td>Flexibility</td>
                            <td>High</td>
                            <td>Moderate</td>
                            <td>Low</td>
                        </tr>
                        <tr>
                            <td>Examples</td>
                            <td>USA, UK, India</td>
                            <td>France, Germany, Japan</td>
                            <td>Saudi Arabia, Iran, Vatican</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="ai-recommendation">
                <p><strong>AI Recommendation:</strong> For international legal research, understanding the fundamental differences between legal systems is crucial. Common law systems offer more flexibility through judicial interpretation, while civil law systems provide more predictability through codified statutes.</p>
            </div>
        </div>
    `;
}

async function sendQuery() {
    const queryInput = document.getElementById("username");
    if (!queryInput) return;
    
    const query = queryInput.value;
    if (!query || !query.trim()) return;
    
    const userMessage = `<strong>You:</strong> ${query}`;
    addMessage(userMessage, true);
    
    const aiResponse = processAIQuery(query);
    
    showTypingIndicator();
    
    autoScrollToBottom();
    
    queryInput.value = "";
    
    try {
        if (aiResponse.type !== 'chat') {
            hideTypingIndicator();
            addMessage(`<strong>Legal Assistant:</strong> ${aiResponse.content}`, false);
            return;
        }
        
        // Add a small delay to simulate thinking
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });
        
        hideTypingIndicator();
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Format the response for better readability
        const formattedResponse = data.response.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
        const botMessage = `<strong>Legal Assistant:</strong> <p>${formattedResponse}</p>`;
        
        simulateTyping(botMessage, () => {
            if (data.sources && data.sources.length > 0) {
                const sourcesDiv = document.createElement("div");
                sourcesDiv.className = "message bot-message new-message";
                sourcesDiv.innerHTML = `<strong>Relevant Acts:</strong><br>${data.sources.join("<br>")}`;
                sourcesDiv.style.fontSize = "0.9rem";
                sourcesDiv.style.marginTop = "5px";
                sourcesDiv.style.padding = "10px";
                sourcesDiv.style.backgroundColor = "rgba(255, 255, 255, 0.7)";
                sourcesDiv.style.borderLeft = "3px solid #4299e1";
                
                const chatHistory = document.getElementById("chat-history");
                if (chatHistory) {
                    chatHistory.appendChild(sourcesDiv);
                    smoothScrollToBottom();
                }
            }
        });
    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        
        const errorMessage = `<strong>Legal Assistant:</strong> Sorry, I encountered an error processing your request. Please try again.`;
        addMessage(errorMessage, false);
    }
}

function setQuestion(question) {
    document.getElementById("username").value = question;
    sendQuery();
}

document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById("username");
    if (usernameInput) {
        usernameInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendQuery();
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    messages.forEach((message, index) => {
        message.style.animationDelay = `${index * 0.1}s`;
    });
    
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        chatContainer.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }
    
    const title = document.querySelector('.animated-title');
    if (title) {
        title.addEventListener('mouseover', function() {
            this.style.animation = 'none';
            setTimeout(() => {
                this.style.animation = 'pulse 2s infinite, textGlow 3s infinite';
            }, 10);
        });
    }
    
    const quickButtons = document.querySelectorAll('.quick-btn');
    quickButtons.forEach((button, index) => {
        button.style.setProperty('--delay', index);
    });
    
    const inputs = document.querySelectorAll('.animated-input, .animated-select, .animated-btn');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    const socialIcons = document.querySelectorAll('.social-icons i');
    socialIcons.forEach((icon, index) => {
        icon.style.animationDelay = `${index * 0.2}s`;
    });
    
    const chatHistory = document.getElementById("chat-history");
    if (chatHistory) {
        chatHistory.addEventListener('scroll', function() {
        });
    }
});

function createCustomPointer() {
    const pointer = document.createElement('div');
    pointer.id = 'custom-pointer';
    pointer.innerHTML = `
        <div class="pointer-ring"></div>
        <div class="pointer-dot"></div>
    `;
    
    pointer.style.position = 'fixed';
    pointer.style.pointerEvents = 'none';
    pointer.style.zIndex = '9999';
    pointer.style.transform = 'translate(-50%, -50%)';
    pointer.style.transition = 'transform 0.2s ease, opacity 0.3s ease';
    
    const ring = pointer.querySelector('.pointer-ring');
    ring.style.width = '30px';
    ring.style.height = '30px';
    ring.style.border = '2px solid #4299e1';
    ring.style.borderRadius = '50%';
    ring.style.position = 'absolute';
    ring.style.top = '0';
    ring.style.left = '0';
    ring.style.transform = 'translate(-50%, -50%)';
    ring.style.boxSizing = 'border-box';
    ring.style.opacity = '0.7';
    
    const dot = pointer.querySelector('.pointer-dot');
    dot.style.width = '8px';
    dot.style.height = '8px';
    dot.style.backgroundColor = '#d69e2e';
    dot.style.borderRadius = '50%';
    dot.style.position = 'absolute';
    dot.style.top = '0';
    dot.style.left = '0';
    dot.style.transform = 'translate(-50%, -50%)';
    
    document.body.appendChild(pointer);
    
    document.addEventListener('mousemove', (e) => {
        pointer.style.left = e.clientX + 'px';
        pointer.style.top = e.clientY + 'px';
    });
    
    const interactiveElements = document.querySelectorAll('button, input, select, a, .quick-btn, .animated-btn');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            pointer.style.transform = 'translate(-50%, -50%) scale(1.5)';
            ring.style.borderColor = '#d69e2e';
            ring.style.boxShadow = '0 0 10px #d69e2e';
            dot.style.backgroundColor = '#4299e1';
        });
        
        element.addEventListener('mouseleave', () => {
            pointer.style.transform = 'translate(-50%, -50%) scale(1)';
            ring.style.borderColor = '#4299e1';
            ring.style.boxShadow = 'none';
            dot.style.backgroundColor = '#d69e2e';
        });
    });
    
    document.addEventListener('mousedown', () => {
        pointer.style.transform = 'translate(-50%, -50%) scale(0.8)';
        ring.style.borderColor = '#ffffff';
        dot.style.backgroundColor = '#ffffff';
    });
    
    document.addEventListener('mouseup', () => {
        pointer.style.transform = 'translate(-50%, -50%) scale(1)';
        ring.style.borderColor = '#4299e1';
        dot.style.backgroundColor = '#d69e2e';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    createCustomPointer();

    window.addEventListener('resize', function() {
        const chatHistory = document.getElementById("chat-history");
        if (chatHistory) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    });
});