$().ready(function() {

  // fade in the top bar when the user scrolls down
  $(document).scroll(function() {
    var topBar = $('.top-bar');
    if($(document).scrollTop() > 0) {
      if(!topBar.hasClass('scrolled')) {
        topBar.addClass('scrolled');
      }
    }
    else {
      topBar.removeClass('scrolled');
    }
  });

  // create an editor object when the user is on an add story page
  if($('#editor').length) {
    var editor = new Quill('#editor', {
      modules: {
        'toolbar': { container: '#formatting-container' },
        'link-tooltip': true,
        'image-tooltip': true
      },
      styles: false,
      theme: 'snow'
    });
  }
});
