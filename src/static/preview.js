$(function() {
  var content_changed = false;

  var writeButton = $('#write-button');
  var writeArea = $('#write-area');
  var previewButton = $('#preview-button');
  var previewArea = $('#preview-area');

  writeArea.keypress(function() {
    content_changed = true;
  });

  writeButton.click(function() {
    swap(previewButton, previewArea, writeButton, writeArea);
  });

  previewButton.click(function() {
    swap(writeButton, writeArea, previewButton, previewArea);
  });

  checkMarkdownUpdate = function() {
    if(writeArea.val().trim() === '') {
      previewArea.html('Nothing to preview');
      return;
    }
    if (content_changed) {
      var csrf_token = Cookies.get('csrftoken');
      $.ajax({ url: '/markdown/', type: 'post',
          data: writeArea.val(), headers: { 'X-CSRFToken': csrf_token },
          success: function (data) {
            content_changed = false;
//            previewArea.css('min-height', writeArea.height());
            previewArea.html(data);
          }
      });
    }
  };

  // initially request a preview (ie page was reloaded).
  previewButton.mouseenter(checkMarkdownUpdate);
  checkMarkdownUpdate();

  swap = function(fromButton, fromArea, toButton, toArea) {
    fromButton[0].disabled = '';
    fromArea.addClass('hidden');

    toButton[0].disabled = 'disabled';
    toArea.removeClass('hidden' );
  };
});
