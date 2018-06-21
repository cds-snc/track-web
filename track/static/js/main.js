$(function(){

  var KEYCODE_ESC = 27;

  // Mobile menu

  $('#menu-btn, .overlay, .sliding-panel-close').on('click touchstart',function (e) {
    $('#menu-content, .overlay').toggleClass('is-visible');

    if($('#menu-content').hasClass('is-visible')) {
      $('#menu-content a').attr('tabindex', '0');
    }
    else {
      $('#menu-content a').attr('tabindex', '-1');
    }

    e.preventDefault();
  });

  // Modal

  $('#modal-btn').on('click touchstart', function (e) {
    if ($('#modal').hasClass('hidden')) toggleModal('show');

    e.preventDefault();
  });

  // $("#modal").on('click touchstart', function (e) {
  //   if ($('#modal').hasClass('flex')) console.log("this works");

  //   e.preventDefault();
  // });

  $('#close-btn').on('click touchstart', function (e) {
    toggleModal('hide');

    e.preventDefault();
  });

  $(document).click(function(e) {
    if (!$(event.target).closest("#modal-content, #modal-btn").length && $('#modal').hasClass('flex')){
      toggleModal('hide');
    }
  });

  $(document).keyup(function(e) {
    if(e.keyCode === KEYCODE_ESC && $('#modal').hasClass('flex')) {
      toggleModal('hide');
    }
  })

  $(document).focusin(function(e) {
    var modal = document.getElementById("modal");
    
    if($('#modal').hasClass('flex') && !$.contains(modal, e.target)) {
      e.stopPropagation();
      $('#modal-content').focus();
    }

  });

  var toggleModal = function(sh){ 
    if(sh == "show") {
      $('#modal').toggleClass('hidden flex');

      $('#modal-header').focus();

      $('#header, #main-content, #goc-footer').attr('aria-hidden', 'true');
      
    }

    else {
      $('#modal').toggleClass('hidden flex');

      $('#header, #main-content, #goc-footer').attr('aria-hidden', 'false');

      $('#close-btn').focus();
    }

  };

});
