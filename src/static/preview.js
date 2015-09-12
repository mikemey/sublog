$(function() {
  var content_changed = true;

  var writeButton = $('#write-button');
  var writeArea = $('#write-area');
  var previewButton = $('#preview-button');
  var previewArea = $('#preview-area');

  writeArea.keypress(function() {
    content_changed = true;
  });

  writeButton.click(function() {
    swap(previewButton, previewArea, writeButton, writeArea);
    writeArea.focus();
  });

  previewButton.click(function() {
    swap(writeButton, writeArea, previewButton, previewArea);
  });

  checkMarkdownUpdate = function() {
    if (content_changed && writeArea.outerHeight()) {
      previewArea.css('min-height', writeArea.outerHeight());
    }
    if(writeArea.val().trim() === '') {
      previewArea.html('<p>Nothing to preview<p>');
      return;
    }
    if (content_changed) {
      var csrf_token = Cookies.get('csrftoken');
      $.ajax({ url: '/markdown/', type: 'post',
          data: writeArea.val(), headers: { 'X-CSRFToken': csrf_token },
          success: function (data) {
            content_changed = false;
            previewArea.html(data);
          }
      });
    }
  };

  // initially request a preview (ie page was reloaded).
  previewButton.mouseenter(checkMarkdownUpdate);
  previewButton.click(checkMarkdownUpdate);
  checkMarkdownUpdate();

  swap = function(fromButton, fromArea, toButton, toArea) {
    fromButton.addClass('active-btn');
    fromArea.addClass('hidden');

    toButton.removeClass('active-btn');
    toArea.removeClass('hidden');
  };
});
