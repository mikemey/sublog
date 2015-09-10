$(function() {
  var ids = ['#user-input', '#user-preview'];
  var write_active = true;
  var content_changed = true;

  var test = 0;

  $('#write-button').click(function() {
    swapTo(0);
  });

  $('#preview-button').click(function() {
      swapTo(1);
  });

  $('#user-input').keypress(function() {
    content_changed = true;
  });

  $('#preview-button').mouseenter(function() {
    if (content_changed) {
      var csrf_token = Cookies.get('csrftoken');
      $.ajax({
          url: '/markdown/',
          type: 'post',
          data: $(ids[0]).val(),
          headers: { 'X-CSRFToken': csrf_token },
          success: function (data) {
            content_changed = false;
            $(ids[1]).html(data);
          }
      });
    }
  });

  function swapTo(toIx) {
    var from = ids[write_active ? 0: 1];
    var to = ids[write_active ? 1: 0];
    $(from).addClass('hidden');
    $(to).removeClass('hidden');
    write_active = to == ids[0];
  };
});