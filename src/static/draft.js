$(function() {

  var content_changed = false;

  var titleField = $('#title');
  var writeArea = $('#write-area');
  var timer = $('#draft-save-timer');
  var icon = $('#draft-store-icon');

  $.getJSON('/article/draft/', function(data) {
    if(data.title) {
      titleField.val(data.title);
    }
    if(data.content) {
      writeArea.val(data.content);
    }
  })

  attachTimer = function() {
    content_changed = true;
    timer.timer('resume');
  };

  writeArea.keypress(attachTimer);
  titleField.keypress(attachTimer);

  timer.timer({
      duration: '3s',
      callback: function() {
        checkMarkdownUpdate();
        if(content_changed) {
          timer.timer('reset');
        } else {
          timer.timer('pause');
        }
      },
      repeat: true
  });

  checkMarkdownUpdate = function() {
    if(writeArea.val().trim() === '') {
      return;
    }
    if(content_changed) {
      saveStart();
      var csrf_token = Cookies.get('csrftoken');
      $.ajax({
          url: '/article/draft/',
          type: 'post',
          data: {
            'title':   titleField.val(),
            'content': writeArea.val()
          },
          headers: { 'X-CSRFToken': csrf_token },
          success: function (data) {
            content_changed = false;
            saveFinish();
          },
          error: function(data) {
            timer.timer('remove');
          }
      });
    }
  };

  saveStart = function() {
    icon.show();
    icon.text('saving draft...');
  }

  saveFinish = function() {
    icon.text('draft stored');
    icon.fadeOut(2000);
  }
});
