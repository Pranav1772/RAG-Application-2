const sidebar = document.querySelector("#sidebar");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");

hide_sidebar.addEventListener("click", function () {
    sidebar.classList.toggle("hidden");
});

const user_menu = document.querySelector(".user-menu ul");
const show_user_menu = document.querySelector(".user-menu button");

show_user_menu.addEventListener("click", function () {
    if (user_menu.classList.contains("show")) {
        user_menu.classList.toggle("show");
        setTimeout(function () {
            user_menu.classList.toggle("show-animate");
        }, 200);
    } else {
        user_menu.classList.toggle("show-animate");
        setTimeout(function () {
            user_menu.classList.toggle("show");
        }, 50);
    }
});

const models = document.querySelectorAll(".model-selector button");

for (const model of models) {
    model.addEventListener("click", function () {
        document.querySelector(".model-selector button.selected")?.classList.remove("selected");
        model.classList.add("selected");
    });
}

const message_box = document.querySelector("#message");

message_box.addEventListener("keyup", function () {
    message_box.style.height = "auto";
    let height = message_box.scrollHeight + 2;
    if (height > 200) {
        height = 200;
    }
    message_box.style.height = height + "px";
});

document.addEventListener("DOMContentLoaded", function () {
    // Function to create a new conversation button
    function createNewConversation(chatId, title) {
        // Create a new list item for the conversation
        var newConversation = document.createElement("li");

        // Create a button for the conversation
        var conversationButton = document.createElement("button");
        conversationButton.className = "conversation-button";
        conversationButton.dataset.chatId = chatId;
        conversationButton.innerHTML = `<i class="fa fa-message fa-regular"></i> ${title}`;

        // Create elements for fading effect and edit buttons
        var fade = document.createElement("div");
        fade.className = "fade";
        var editButtons = document.createElement("div");
        editButtons.className = "edit-buttons";
        editButtons.innerHTML = '<button><i class="fa fa-edit"></i></button>' + '<button><i class="fa fa-trash"></i></button>';

        // Append elements to the new conversation list item
        newConversation.appendChild(conversationButton);
        newConversation.appendChild(fade);
        newConversation.appendChild(editButtons);

        // Find the "Today" grouping
        var todayGrouping = document.querySelector(".conversations .grouping");

        // Insert the new conversation under the "Today" grouping
        todayGrouping.parentNode.insertBefore(newConversation, todayGrouping.nextSibling);

        conversationButton.addEventListener("click", function () {
            var mainTag = document.querySelector("main");

            // Your HTML code to be added
            var dynamicHTML = `
                <div class="view new-chat-view">
                    <div class="logo">ChatWTF</div>
                </div>
                <div class="view conversation-view">
                    <!-- <div class="model-name"><i class="fa fa-bolt"></i> Default (GPT-3.5)</div> -->
                </div>

                <div id="message-form">
                <input type="hidden" name="chat_id" value="{{ chat_id }}" />
                <div class="upload-field">
                    Upload file: <input type="file" id="upload-file" name="file" />
                </div>
                    <div class="message-wrapper">
                        <textarea id="message" rows="1" placeholder="Send a message"></textarea>
                        <button class="send-button"><i class="fa fa-paper-plane"></i></button>
                    </div>
                    <div class="disclaimer">This is a ChatGPT UI Clone for personal use and educational purposes only.</div>
                </div>
            `;

            // Append the dynamic HTML to the main tag
            mainTag.innerHTML = dynamicHTML;
        });
        conversationButton.click();
    }

    // Event listener for the "New chat" button
    var newChatButton = document.querySelector(".new-chat");
    newChatButton.addEventListener("click", function () {
        axios
            .get("/new_chat/")
            .then((response) => {
                createNewConversation(response.data.id, response.data.title);
            })
            .catch((error) => console.error("Error fetching conversation:", error));
    });
});

//Load conversations with event listeners to the conversation buttons
function show_view(view_selector) {
    document.querySelectorAll(".view").forEach((view) => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

document.querySelectorAll(".conversation-button").forEach((button) => {
    button.addEventListener("click", function () {
        show_view(".conversation-view");
        var chatId = button.dataset.chatId;
        chatId = 1;
        // Load chat messages based on the chatId
        loadChatMessages(chatId);
    });
});

// Function to create a message element
function createMessageElement(role, content) {
    var messageElement = document.createElement("div");
    messageElement.className = role + " message";

    var identityElement = document.createElement("div");
    identityElement.className = "identity";
    var userIconElement = document.createElement("i");
    userIconElement.className = role === "user" ? "user-icon" : "gpt user-icon";
    userIconElement.textContent = role === "user" ? "u" : "G";
    identityElement.appendChild(userIconElement);

    var contentElement = document.createElement("div");
    contentElement.className = "content";
    var paragraphElement = document.createElement("p");
    paragraphElement.textContent = content;
    contentElement.appendChild(paragraphElement);
    console.log("here 2");
    messageElement.appendChild(identityElement);
    messageElement.appendChild(contentElement);

    return messageElement;
}

// Function to load chat messages
function loadChatMessages(chatId) {
    // Make a request to the Django backend using Axios
    console.log("this works");
    axios
        .get(`/load_chat/${chatId}/`)
        .then((response) => {
            // Get the conversation view element
            var conversationView = document.querySelector(".view.conversation-view");

            // Clear existing messages
            conversationView.innerHTML = "";

            // Iterate through the received messages and create message elements
            response.data.forEach((message) => {
                var messageElement = createMessageElement(message.role, message.content);
                console.log("here");
                conversationView.appendChild(messageElement);
            });
        })
        .catch((error) => console.error("Error loading chat messages:", error));
}

// document.addEventListener("DOMContentLoaded", function () {
//     // Event listener for the "conversationButtons" button
//     var conversationButtons = document.querySelectorAll(".conversation-button");
//     conversationButtons.forEach(function (button) {
//         button.addEventListener("click", function () {
//             var chatId = button.dataset.chatId;
//             chatId = 1;
//             // Load chat messages based on the chatId
//             loadChatMessages(chatId);
//         });
//     });

//     // Function to create a message element
//     function createMessageElement(role, content) {
//         var messageElement = document.createElement("div");
//         messageElement.className = role + " message";

//         var identityElement = document.createElement("div");
//         identityElement.className = "identity";
//         var userIconElement = document.createElement("i");
//         userIconElement.className = role === "user" ? "user-icon" : "gpt user-icon";
//         userIconElement.textContent = role === "user" ? "u" : "G";
//         identityElement.appendChild(userIconElement);

//         var contentElement = document.createElement("div");
//         contentElement.className = "content";
//         var paragraphElement = document.createElement("p");
//         paragraphElement.textContent = content;
//         contentElement.appendChild(paragraphElement);

//         messageElement.appendChild(identityElement);
//         messageElement.appendChild(contentElement);

//         return messageElement;
//     }

//     // Function to load chat messages
//     function loadChatMessages(chatId) {
//         // Make a request to the Django backend using Axios
//         axios
//             .get(`/load_chat/${chatId}/`)
//             .then((response) => {
//                 // Get the conversation view element
//                 var conversationView = document.querySelector(".view.conversation-view");

//                 // Clear existing messages
//                 conversationView.innerHTML = "";

//                 // Iterate through the received messages and create message elements
//                 response.data.forEach((message) => {
//                     var messageElement = createMessageElement(message.role, message.content);
//                     console.log("here");
//                     conversationView.appendChild(messageElement);
//                 });
//             })
//             .catch((error) => console.error("Error loading chat messages:", error));
//     }
// });
