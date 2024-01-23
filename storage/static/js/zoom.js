window.addEventListener('keydown', function(event) {
    if (event.ctrlKey == true && (event.which == 61 || event.which == 107 || event.which == 173 || event.which == 109 || event.which == 187 || event.which == 189)) {
      event.preventDefault();
    }
  }, false);
  
  window.addEventListener('wheel', function(event) {
    if (event.ctrlKey == true) {
      event.preventDefault();
    }
  }, {passive: false});
  