$().ready(function() {
  var editor = new Quill('#editor', {
    modules: {
      'toolbar': { container: '#formatting-container' },
      'link-tooltip': true,
      'image-tooltip': true
    },
    styles: false,
    theme: 'snow'
  });
});
