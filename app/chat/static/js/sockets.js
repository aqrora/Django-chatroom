var url = 'ws://127.0.0.1:8001/ws/chat/' // TODO set .env variable
var chatSocket = null;




function messageHtml(user, message, lastAvatar, fromCurrentUser, showAuthor = true) {
    // Returns html code of message block

    var authorHtml = ''; // Hidden by default
    var editSign = ''; // Hidden by default
    var activeClass = fromCurrentUser ? 'active' : ''; // Disabled by default
    
    if (showAuthor === true) { // If it's the first time message from this user is shown
        authorHtml = `
<div class="message-row">  
    <div class="message-author" data-user-id = "${user.id}" style="color:${user.user_color}">
        ${user.username}:
    </div>
</div>
`
    } else { 
        lastAvatar.remove();
    }

    if (fromCurrentUser) { // Checks whether the current user have sent this specific message
        editSign = `
    <span class="edit">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z"/></svg>
    </span>`
    }

    
    var rawHtml = `
<div class="message">
    ${authorHtml}
    <div class="message-row">  
        <div class="avatar-container">
        
            <div class="avatar" style="background-image: url('${user.avatar}')"></div>
            
        </div>
        <div class="message-text-container">
            <div class="message-text ${activeClass}" data-message-id="${message.id}">
            ${message.text}
        <span class="sent">${message.created}</span>
        ${editSign}
        </div>
        </div>
    </div>
</div>
`
    return rawHtml
}

function messageEdited(data) {
    var element = $(`[data-message-id="${data.id}"]`).first()
    var sentEl = element.find('.sent')
    var sent = sentEl.text()
    element.text(data.text)
    $(`[data-message-id="${data.id}"]`).append($(`<span class='sent'>Edited | ${sent}</span>`))
}

function connectSocket() {
    // Connect to websocket
    chatSocket = new WebSocket(url)


    chatSocket.onerror = function(error) {
        connectSocket(); // reconnect
    };
    
    chatSocket.onclose = function(event) {
        connectSocket(); // reconnect
    };
    
    chatSocket.onmessage = (e) => {
        let data = JSON.parse(e.data)
    
        // When someon sends a message
        if (data.type === 'chat'){
            var messages = $('#chat-box').children();

            var lastAuthor = messages.find('.message-author').last()
            var lastAuthorId = parseInt(lastAuthor.data('user-id'))
            
            var lastAvatar = messages.find('.avatar').last()
            
            var sameAuthor = lastAuthorId !== data.user.id
            var fromCurrentUser = current_user_id === data.user.id
            
            // Displays a message
            $('#chat-box').append(messageHtml(data.user, data.message, lastAvatar, fromCurrentUser, sameAuthor))
            scrollToBottom();
        } else if (data.type === 'edit')
        {
            
            messageEdited(data);
        }
    }

}


