$(document).ready(function () {
    $("#chat-icon").click(function () {
        $(".chat-container").toggle();
    });

    $("#close-chat").click(function () {
        $(".chat-container").hide();
    });

    $("#send-btn").click(function () {
        sendMessage();
    });

    $("#copy-btn").click(function () {
        copyLastResponse();
    });

    $("#user-input").keypress(function (event) {
        if (event.which == 13) {
            sendMessage();
        }
    });

    $("#clear-chat").click(function () {
        $("#chat-box").empty(); // Clears the chatbox
    });

    function sendMessage() {
        let userMessage = $("#user-input").val().trim();
        if (userMessage === "") return;

        $("#chat-box").append(`<div class="user-message">${userMessage} 
            <span class="edit-query" onclick="editQuery('${userMessage}')">✏️</span></div>`);
        $("#user-input").val("");

        $.ajax({
            type: "POST",
            url: "/chat",
            contentType: "application/json",
            data: JSON.stringify({ message: userMessage }),
            success: function (response) {
                $("#chat-box").append(`<div class="bot-message">${response.response}</div>`);
                $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
            },
            error: function () {
                $("#chat-box").append(`<div class="bot-message">Sorry, something went wrong.</div>`);
            }
        });
    }

    window.editQuery = function (message) {
        $("#user-input").val(message);
        $("#user-input").focus();
    };

    function copyLastResponse() {
        let lastResponse = $(".bot-message").last().text().trim();
        if (lastResponse === "") {
            alert("No response to copy!");
            return;
        }

        let tempInput = $("<textarea>");
        $("body").append(tempInput);
        tempInput.val(lastResponse).select();
        document.execCommand("copy");
        tempInput.remove();
        alert("Response copied!");
    }
});
