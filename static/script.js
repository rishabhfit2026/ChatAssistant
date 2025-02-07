function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");

    // Add user message to chatbox
    let userMessage = `<div class='message user-message'><strong>You:</strong> ${userInput}</div>`;
    chatBox.innerHTML += userMessage;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show typing indicator
    let typingIndicator = `<div id="typing" class='typing'>Assistant is typing...</div>`;
    chatBox.innerHTML += typingIndicator;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send request to Flask backend
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("typing").remove(); // Remove typing indicator
        let botMessage = `<div class='message bot-message'><strong>Assistant:</strong> ${data.response}</div>`;
        chatBox.innerHTML += botMessage;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    document.getElementById("user-input").value = ""; // Clear input
}
