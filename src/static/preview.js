$(function() {
  var content_changed = true;

  var writeButton = $('#write-button');
  var writeArea = $('#write-area');
  var previewButton = $('#preview-button');
  var previewParent = $('#preview-parent');
  var previewArea = $('#preview-area');

  writeArea.keypress(function() {
    content_changed = true;
  });

  writeArea.focus(function() {
    writeButton.addClass('write-focus');
    previewButton.addClass('write-focus');
  });

  writeArea.focusout(function() {
    writeButton.removeClass('write-focus');
    previewButton.removeClass('write-focus');
  });

  writeButton.click(function() {
    swap(previewButton, previewParent, writeButton, writeArea);
    writeArea.focus();
  });

  previewButton.click(function() {
    swap(writeButton, writeArea, previewButton, previewParent);
  });

  checkMarkdownUpdate = function() {
    if (content_changed && writeArea.outerHeight()) {
      previewParent.css('min-height', writeArea.outerHeight());
    }
    if(writeArea.val().trim() === '') {
      previewArea.html('<p>Nothing to preview<p>');
      return;
    }
    if (content_changed) {
      var csrf_token = Cookies.get('csrftoken');
      $.ajax({
          url: '/markdown/',
          type: 'post',
          data: { 'text': writeArea.val() },
          headers: { 'X-CSRFToken': csrf_token },
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
