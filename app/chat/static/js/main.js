

function sendLogin(username) {
    console.log("sending login")
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
        console.log(response)
        $("#overlay").hide();
        $("#popup-container").hide();
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("An error occurred: " + errorThrown);
      }
    });
  }


function showPopup() {
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
    var chatBox = $('.chat-box');
    chatBox.scrollTop(chatBox[0].scrollHeight);
  }

  
$(document).ready(function() {
    var $inputField = $('input[name="message_text"]');
    var submitButton = $('.submit-message');
    submitButton.hide();

    $inputField.on('input', function() {
        var inputValue = $(this).val();
        if (inputValue.trim().length > 0) {
        submitButton.show();
        } else {
        submitButton.hide();
        }
    });

    $('#message-form').submit(function(event) {
        event.preventDefault(); // отменяем стандартное поведение формы
    
        var formData = $(this).serialize(); // получаем данные формы в виде строки
    
        $.ajax({
          url: "/submit_message",
          type: "POST",
          data: formData,
          dataType: 'json', // указываем, что ждем ответ в формате JSON
          success: function(response) {
            if (response.success && response.success === true) {
                console.log("Message sent")
                $inputField.val("");
              } else {
                alert(response.errors);
                // обрабатываем ошибку
              }
          },
          error: function(response) {
            // обрабатываем ошибку
            console.log(response);
          }
        });
    });


});