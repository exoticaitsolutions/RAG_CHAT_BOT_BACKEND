(function() {
   
    document.head.insertAdjacentHTML('beforeend', 
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.16/tailwind.min.css" rel="stylesheet" />'
    );


    var chatbotContainer = document.createElement("div");
    chatbotContainer.id = "chatbot-container";
    chatbotContainer.style.position = "fixed";
    chatbotContainer.style.bottom = "73px";
    chatbotContainer.style.right = "60px";
    chatbotContainer.style.width = "350px";
    chatbotContainer.style.height = "500px";
    chatbotContainer.style.background = "rgb(221 211 211)";
    chatbotContainer.style.border = "2px solid #ccc";
    chatbotContainer.style.borderRadius = "10px";
    chatbotContainer.style.overflow = "hidden";
    chatbotContainer.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
    chatbotContainer.style.display = "none";  // Initially hidden
    chatbotContainer.innerHTML = `
        <div id="chat-header" 
         style="background: #d77496; color: white;
          padding: 12px; text-align: center; font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    display: flex; align-items: center; justify-content: center;">
    <img src="/static/backend/image/ai_logo.png" alt="Profile" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
            Chatbot
        </div>
        <div id="chat-messages" style="height: 386px; overflow-y: auto; padding: 10px;">
            <p>Welcome! Ask me anything.</p>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between;">
        <input type="text" id="chat-input" placeholder="Type your message..." 
            style="width: 80%; padding: 10px; border: none; border-top: 1px solid #ccc;">
        <button id="chat-submit" style="width: 20%; padding: 10px; border: none; background: #d77496; color: #7476e0; cursor: pointer; text-align: center; font-weight: bold">Send</button>
        </div>
    `;
    document.body.appendChild(chatbotContainer);

    // Create the launcher icon
    var launcherIcon = document.createElement("div");
    launcherIcon.id = "launcher-icon";
    launcherIcon.style.position = "fixed";
    launcherIcon.style.bottom = "20px";
    launcherIcon.style.right = "20px";
    launcherIcon.style.width = "60px";
    launcherIcon.style.height = "60px";
    launcherIcon.style.backgroundColor = "#d77496";
    launcherIcon.style.borderRadius = "50%";
    launcherIcon.style.cursor = "pointer";
    launcherIcon.style.display = "flex";
    launcherIcon.style.alignItems = "center";
    launcherIcon.style.justifyContent = "center";
    launcherIcon.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
    launcherIcon.innerHTML = `<span style="color: white; font-size: 24px;">💬</span>`;  // You can replace this with an image
    document.body.appendChild(launcherIcon);

    // Function to send a message to the API
    function sendMessageToAPI(message) {
        // Get chatbot ID and base URL from script attributes
        let chatbotId = document.querySelector('script[chatbot-id]')?.getAttribute('chatbot-id');
        let base_url = document.querySelector('script[base_url]')?.getAttribute('base_url');
    
        if (!chatbotId || !base_url) {
            console.error("Missing chatbot ID or base URL.");
            displayMessage("Configuration error: Missing chatbot ID or base URL.", "bot");
            return;
        }
    
        // Construct the API URL
        const apiUrl = `${base_url}/api/v2/chatbot/query/?chat_id=${chatbotId}`;
        console.log("API URL:", apiUrl);
    
        // Send the POST request
        fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("API Response:", data);
            
            // Extract and display chatbot's response
            if (data.results) {
                displayMessage(data.results.response, "bot");
            } else {
                displayMessage("No response from chatbot.", "bot");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            displayMessage("Error fetching response.", "bot");
        });
    }
    

    // Function to display messages
    function displayMessage(message, sender) {
        var chatMessages = document.getElementById("chat-messages");
        var msgDiv = document.createElement("div");
        msgDiv.textContent = message;
        msgDiv.style.padding = "10px";
        msgDiv.style.margin = "5px";
        msgDiv.style.borderRadius = "5px";

        if (sender === "bot") {
            msgDiv.style.background = "#f1f1f1";
            msgDiv.style.textAlign = "left";
        } else {
            msgDiv.style.background = "#d77496";
            msgDiv.style.color = "white";
            msgDiv.style.textAlign = "right";
        }

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listener for the send button
    document.getElementById("chat-submit").addEventListener("click", function() {
        var chatInput = document.getElementById("chat-input");
        var userMessage = chatInput.value.trim();
        
        if (userMessage) {
            displayMessage(userMessage, "user");
            // Get the dynamic base URL
            // Pass the base URL to the function if needed
            sendMessageToAPI(userMessage);
    
            // Clear input field after sending message
            chatInput.value = "";
        }
    });

    // Event listener for the launcher icon click to toggle chatbot visibility
    launcherIcon.addEventListener("click", function() {
        if (chatbotContainer.style.display === "none") {
            chatbotContainer.style.display = "block";  
        } else {
            chatbotContainer.style.display = "none"; 
        }
    });


    document.getElementById("chat-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            document.getElementById("chat-submit").click();
        }
    });

})();
