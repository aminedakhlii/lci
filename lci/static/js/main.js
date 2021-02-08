
(function ($) {
    "use strict";
})(jQuery);

let get = function(url,array) {

  $.get(url=url,
  data={'key':array},
  success=function(data) {
     console.log(array) ;
  });
}

$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});
