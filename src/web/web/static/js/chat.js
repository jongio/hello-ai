$(document).ready(() => {
    const scrollToBottom = () => {
        const chatContainer = $("#chat-container")[0];
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    const appendMessage = (message, isUser) => {
        const iconClass = isUser ? "bi-person-fill" : "bi-robot";
        const bubbleClass = isUser ? "user" : "ai";
        $("#chat-container").append(`
            <div class="d-flex align-items-start mb-2">
                <i class="bi ${iconClass} me-2"></i>
                <div class="chat-bubble ${bubbleClass}">${message}</div>
            </div>
        `);
        scrollToBottom();
    };

    $("#send").click(() => {
        const userInput = $("#userInput").val().trim();
        if (userInput === '') return;

        appendMessage(userInput, true);
        $("#userInput").val('');

        const dataToSend = JSON.stringify({ message: userInput });

        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: dataToSend,
        })
            .then(response => response.json())
            .then(data => appendMessage(data.response, false))
            .catch(error => {
                console.error('Error:', error);
                $("#chat-container").append(`<div class="text-danger">Error: Could not get a response from the AI.</div>`);
            });
    });

    $("#userInput").keyup((event) => {
        if (event.which === 13) {
            event.preventDefault();
            $("#send").click();
        }
    });
});
