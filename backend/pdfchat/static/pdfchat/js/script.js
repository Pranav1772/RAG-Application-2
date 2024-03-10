document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector("#sidebar");
    const hideSidebar = document.querySelector(".hide-sidebar");
    const newChatButton = document.querySelector(".new-chat");
    const userMenu = document.querySelector(".user-menu ul");
    const showUserMenu = document.querySelector(".user-menu button");
    const models = document.querySelectorAll(".model-selector button");

    hideSidebar.addEventListener("click", () => sidebar.classList.toggle("hidden"));

    showUserMenu.addEventListener("click", () => {
        userMenu.classList.toggle("show");
        setTimeout(() => userMenu.classList.toggle("show-animate"), 200);
    });

    models.forEach((model) => {
        model.addEventListener("click", () => {
            const selectedButton = document.querySelector(".model-selector button.selected");
            selectedButton?.classList.remove("selected");
            model.classList.add("selected");
        });
    });

    newChatButton.addEventListener("click", handleNewChatButtonClick);

    function handleNewChatButtonClick() {
        const mainTag = document.querySelector("main");
        const dynamicHTML = `
            <div id="message-form">
                <form id="upload-form" action="/new_chat/" method="post" enctype="multipart/form-data">
                    <div class="upload-field">
                        Upload file: <input type="file" id="upload-file" name="file" />
                        <button type="submit" id="hidden-submit-button"></button>
                    </div>                       
                </form>
            </div>
        `;
        mainTag.innerHTML = dynamicHTML;

        const uploadForm = document.getElementById("upload-form");
        uploadForm.addEventListener("submit", handleUploadFormSubmit);
    }

    function handleUploadFormSubmit(event) {
        event.preventDefault();
        const fileInput = document.getElementById("upload-file");
        const file = fileInput.files[0];

        if (file) {
            const csrfToken = getCookie("csrftoken");
            const formData = new FormData();
            formData.append("file", file);

            axios
                .post("/new_chat/", formData, {
                    headers: { "X-CSRFToken": csrfToken },
                })
                .then(handleUploadSuccess)
                .catch(handleUploadError);

            document.getElementById("hidden-submit-button").click();
        } else {
            console.log("Please select a file before creating a new chat.");
        }
    }

    function handleUploadSuccess(response) {
        console.log("File uploaded successfully:", response.data);
        createNewConversation(response.data.id, response.data.title);
    }

    function handleUploadError(error) {
        console.error("Error uploading file:", error);
    }

    function getCookie(name) {
        const cookieValue = document.cookie.split("; ").find((cookie) => cookie.startsWith(`${name}=`));
        return cookieValue ? decodeURIComponent(cookieValue.split("=")[1]) : null;
    }

    function createNewConversation(chatId, title) {
        const conversationButton = document.createElement("button");
        conversationButton.className = "conversation-button";
        conversationButton.dataset.chatId = chatId;
        conversationButton.innerHTML = `<i class="fa fa-message fa-regular"></i> ${title}`;

        const newConversation = document.createElement("li");
        newConversation.appendChild(conversationButton);
        newConversation.appendChild(createFadeElement());
        newConversation.appendChild(createEditButtonsElement());

        const todayGrouping = document.querySelector(".conversations .grouping");
        todayGrouping.parentNode.insertBefore(newConversation, todayGrouping.nextSibling);

        conversationButton.addEventListener("click", () => {
            const mainTag = document.querySelector("main");
            const dynamicHTML = `
                <div class="view new-chat-view">
                    <div class="logo">ChatWTF</div>
                </div>
                <div class="view conversation-view"></div>
                <div id="message-form">
                    <div class="message-wrapper">
                        <input type="hidden" id="hidden-chatId" value="${chatId}" />
                        <textarea id="message" rows="1" placeholder="Send a message"></textarea>
                        <button class="send-button"><i class="fa fa-paper-plane"></i></button>
                    </div>
                    <div class="disclaimer">
                        This is a ChatGPT UI Clone for personal use and educational purposes only.
                    </div>
                </div>
            `;
            mainTag.innerHTML = dynamicHTML;
            showView(".conversation-view");
            const sendButton = document.querySelector(".send-button");
            sendButton.addEventListener("click", handleSendButtonClick);
        });

        conversationButton.click();
    }

    function createFadeElement() {
        const fade = document.createElement("div");
        fade.className = "fade";
        return fade;
    }

    function createEditButtonsElement() {
        const editButtons = document.createElement("div");
        editButtons.className = "edit-buttons";
        editButtons.innerHTML = '<button><i class="fa fa-edit"></i></button>' + '<button><i class="fa fa-trash"></i></button>';
        return editButtons;
    }

    function handleSendButtonClick() {
        const hiddenChatId = document.getElementById("hidden-chatId").value;
        const messageText = document.getElementById("message").value;
        console.log(hiddenChatId, messageText);
        const conversationView = document.querySelector(".view.conversation-view");
        const userMessageElement = createMessageElement("user", messageText);
        conversationView.appendChild(userMessageElement);

        const csrfToken = getCookie("csrftoken");
        console.log("this worked1");
        const formData = new FormData();
        formData.append("chatId", hiddenChatId);
        formData.append("messageText", messageText);

        axios
            .post("/get_response/", formData, {
                headers: { "X-CSRFToken": csrfToken },
            })
            .then(handleServerResponse)
            .catch(handleServerError);
        console.log("this worked2");
    }

    function handleServerResponse(response) {
        const assistantMessageElement = createMessageElement("assistant", response.data.status);
        const conversationView = document.querySelector(".view.conversation-view");
        conversationView.appendChild(assistantMessageElement);
        console.log("Server response:", response.data);
    }

    function handleServerError(error) {
        console.error("Error sending data to the server:", error);
    }

    function showView(viewSelector) {
        document.querySelectorAll(".view").forEach((view) => {
            view.style.display = "none";
        });

        document.querySelector(viewSelector).style.display = "flex";
    }

    document.querySelectorAll(".conversation-button").forEach((button) => {
        button.addEventListener("click", function () {
            showView(".conversation-view");
            const chatId = button.dataset.chatId;
            console.log(chatId);
            loadChatMessages(chatId);
        });
    });

    function loadChatMessages(chatId) {
        axios
            .get(`/load_chat/${chatId}/`)
            .then((response) => {
                const id = response.data.id;
                const messages = response.data.messages;

                const conversationView = document.querySelector(".view.conversation-view");
                conversationView.innerHTML = "";

                messages.forEach((message) => {
                    const messageElement = createMessageElement(message.role, message.content);
                    conversationView.appendChild(messageElement);
                });

                const messageWrapper = document.createElement("div");
                messageWrapper.className = "message-wrapper";

                const hiddenChatIdInput = document.createElement("input");
                hiddenChatIdInput.type = "hidden";
                hiddenChatIdInput.id = "hidden-chatId";
                hiddenChatIdInput.value = id;

                const textarea = document.createElement("textarea");
                textarea.id = "message";
                textarea.rows = "1";
                textarea.placeholder = "Send a message";

                const sendButton = document.createElement("button");
                sendButton.className = "send-button";
                sendButton.innerHTML = '<i class="fa fa-paper-plane"></i>';

                messageWrapper.appendChild(hiddenChatIdInput);
                messageWrapper.appendChild(textarea);
                messageWrapper.appendChild(sendButton);

                const messageForm = document.getElementById("message-form");
                messageForm.innerHTML = "";
                messageForm.appendChild(messageWrapper);

                sendButton.addEventListener("click", handleSendButtonClick);
            })
            .catch((error) => console.error("Error loading chat messages:", error));
    }

    function createMessageElement(role, content) {
        const messageElement = document.createElement("div");
        messageElement.className = `${role} message`;

        const identityElement = document.createElement("div");
        identityElement.className = "identity";

        const userIconElement = document.createElement("i");
        userIconElement.className = role === "user" ? "user-icon" : "gpt user-icon";
        userIconElement.textContent = role === "user" ? "u" : "G";

        const contentElement = document.createElement("div");
        contentElement.className = "content";

        const paragraphElement = document.createElement("p");
        paragraphElement.textContent = content;

        contentElement.appendChild(paragraphElement);
        identityElement.appendChild(userIconElement);
        messageElement.appendChild(identityElement);
        messageElement.appendChild(contentElement);

        return messageElement;
    }
});
