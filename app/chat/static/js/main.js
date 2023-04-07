

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

    $inputField.on('input', checkInputField);

    function checkInputField() {
        var inputValue = $(this).val();
        if (inputValue.trim().length > 0) {
        submitButton.show();
        } else {
        submitButton.hide();
        }
    }

    $('#message-form').off('submit').submit(function(event) {
      event.preventDefault();
      var $form = $(this);
      var $submitButton = $form.find('button[type="submit"]');
      $submitButton.prop('disabled', true); // отключаем кнопку отправки формы
  
      var formData = $form.serialize();
      $.ajax({
          url: "/submit_message",
          type: "POST",
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.success && response.success === true) {
                  console.log("Message sent")
                  $inputField.val(""); // устанавливаем пустое значение в поле ввода
                  submitButton.hide(); // скрываем кнопку
                } else {
                  alert(response.errors);
                }
              },
            error: function(response) {
              console.log(response);
            },
            complete: function() {
              $submitButton.prop('disabled', false); // включаем кнопку отправки формы после получения ответа
            }

          });
        });


});