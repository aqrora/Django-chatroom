var current_user_id = undefined;


function sendLogin(username) {
    // Sends request to endpoint and sets jwt_token cookie if request succeded
    $.ajax({
      url: "/login",
      method: "POST",
      data: {
        username: username,
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // include the CSRF token
      },
      success: function(response) {

        // Set the JWT token in a cookie
        document.cookie = "jwt_token=" + response.token;
        // Hide popup
        $("#overlay").hide();
        $("#popup-container").hide();
        // Set global variable and connect to websocket
        current_user_id = parseInt(response.user_id);
        connectSocket();
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("An error occurred: " + errorThrown);
      }
    });
  }


function showPopup() {
    // Displays popup that prompts user to login
    $("#overlay").show();
    $("#popup-container").show();
    
    // Submit the form
    $("#username-form").submit(function(e) {
      e.preventDefault();
      var username = $("#username").val();
      if (username) {
        sendLogin(username);
      } else {
        alert("Please enter a username.");
      }
    });
    
    // Log in anonymously
    $("#anonymous-button").click(function() {
        sendLogin("Anonymous");
    });
}


function scrollToBottom() {
    // Scroll's the .chat-box container to the bottom
    var chatBox = $('.chat-box');
    chatBox.scrollTop(chatBox[0].scrollHeight);
  }

  
$(document).ready(function() {

    var inputField = $('input[name="message_text"]');
    var submitButton = $('.submit-message');
    // hides the submit button when page loads
    submitButton.hide();

    inputField.on('input', checkInputField);

    function checkInputField() {
        // hides the submit button if the field is empty
        var inputValue = $(this).val();
        if (inputValue.trim().length > 0) {
          submitButton.show();
        } else {
          submitButton.hide();
        }
    }

    $('#message-form').off('submit').submit(function(event) {
      event.preventDefault(); 
      submitButton.prop('disabled', true); // Disables the submit button until request completes

      var form = $(this);
      var formData = form.serialize();
      // Sends request to the endpoint, and if succided - clears the form and hides the submit button
      $.ajax({
          url: "/submit_message",
          type: "POST",
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.success && response.success === true) {
                  inputField.val("");
                  submitButton.hide();
                } 
                else {
                  alert("Can't send the message - Its empty")
                }
              },
            error: function(response) {
              alert("Can't send the message - ratelimit exceeded")
            },
            complete: function() {
              submitButton.prop('disabled', false); // enabled the submit button 
            }

          });
        });
        
      
});


function getMessageContents(element) {
  // Removes all unnecessary spaces from text
  return element.contents().filter(function() {
    return this.nodeType === 3; // NodeType 3 - это текстовые узлы
  }).text().trim();
}


function setInputField(messageContainer, messageText) {
  // Replaces html of an messageContainer to input field
  var sent = messageContainer.find('.sent').text();
    messageContainer.html(
    `<input type="text" maxlength="32" class="edit-message-input" data-old-msg="${messageText}" value="${messageText}"">
      
      <button class="edit-message-save">Save</button>
      <button class="edit-message-cancel">Cancel</button>
    <span class="sent">${sent}</span>`
  );
}

function setMessageContents(messageContainer, messageText) {
  // Replaces html of an messageContainer back to its original
  var sent = messageContainer.find('.sent').text();
  messageContainer.html(
    `
      ${messageText}
      <span class="sent">${sent}</span>
      <span class="edit">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z"/></svg>
      </span>
    `
  )
}

$(document).on('click', '.edit', function() {
  // Handles edit button presses
  var messageTextContainer = $(this).parent();
  var messageText = getMessageContents(messageTextContainer)
  setInputField(messageTextContainer, messageText)
});


$(document).on('click', '.edit-message-save', function() {
  // Handles edit button's submission
  var messageTextContainer = $(this).parent();

  var inputField = messageTextContainer.find('.edit-message-input')
  var inputValue = inputField.val()
  
  var old_msg = inputField.data('old-msg');
  var message_id = messageTextContainer.data('message-id');

  // If message wasn't changed - there is no need to make a request
  if (old_msg == inputValue) {
    return 
  }
  
  var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
  // Sends request to an endpoint that changes message in the database
  // If succeeded - sets message container to new content
  $.ajax({
    url: `/edit_message/${message_id}/`,
    method: "POST",
    data: {
      message_text: inputValue,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // include the CSRF token
    },
    success: function(response) {
      setMessageContents(messageTextContainer, inputValue);
      // alert('message updated')
    },
    error: function(jqXHR, textStatus, errorThrown) {
      alert("An error occurred: " + errorThrown);
    }
  });
});


$(document).on('click', '.edit-message-cancel', function() {

  var messageTextContainer = $(this).parent();
  var messageText = messageTextContainer.find(".edit-message-input").data("old-msg");
  setMessageContents(messageTextContainer, messageText)
});
