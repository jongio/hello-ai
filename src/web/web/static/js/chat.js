$(document).ready(() => {
    let sendingRequest = false;

    const scrollToBottom = () => {
        const chatContainer = $("#chat-container")[0];
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    const showLoading = () => {
        $("#chat-container").append(`
            <div class="loading-container text-start mb-2">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        `);
        scrollToBottom();
    };

    const hideLoading = () => {
        $(".loading-container").remove();
    };

    const toggleSendButtonIcon = (sending) => {
        const sendButton = $("#send");
        if (sending) {
            sendButton.html('<i class="bi bi-stop-fill"></i>'); // Change to stop icon
        } else {
            sendButton.html('<i class="bi bi-arrow-up"></i>'); // Change back to up arrow icon
        }
    };

    const sendMessageToAI = (userInput, searchDocuments) => {
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput, search_documents: searchDocuments }),
        })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                appendMessage(data.response, false);
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                $("#chat-container").append(`<div class="text-danger">Error: Could not get a response from the AI.</div>`);
            })
            .finally(() => {
                sendingRequest = false;
                toggleSendButtonIcon(false); // Change button icon back to up arrow
            });
    };

    const appendMessage = (message, isUser) => {
        const messageTypeClass = isUser ? "user-message" : "ai-message";
        const bubbleClass = isUser ? "user" : "ai";
        const alignClass = isUser ? "justify-content-end" : "justify-content-start";
        const htmlContent = `
            <div class="message-row ${messageTypeClass}">
                <div class="d-flex align-items-center ${alignClass}">
                    <div class="chat-bubble ${bubbleClass}">${message}</div>
                </div>
            </div>
        `;
        $("#chat-container").append(htmlContent);
        scrollToBottom();
    };

    $("#send").click(() => {
        if (sendingRequest) {
            // If already sending request, stop it
            // You may need to implement a way to abort the fetch request here
            sendingRequest = false;
            toggleSendButtonIcon(false);
            hideLoading(); // Hide loading animation if visible
            return;
        }

        const userInput = $("#userInput").val().trim();
        if (userInput === '') return;

        const searchDocuments = $("#toggleDocs").hasClass("btn-primary");

        appendMessage(userInput, true);
        $("#userInput").val('');
        showLoading();
        toggleSendButtonIcon(true); // Change button icon to stop

        sendingRequest = true;
        sendMessageToAI(userInput, searchDocuments);
    });

    $("#userInput").keyup((event) => {
        if (event.which === 13) {
            event.preventDefault();
            $("#send").click();
        }
    });

    $("#toggleDocs").click(function () {
        $(this).toggleClass("btn-primary btn-light");
    });
});
