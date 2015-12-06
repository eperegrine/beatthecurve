$(document).ready(function () {
   // Initialize collapse button
  $(".button-collapse").sideNav();
  // Initialize collapsible (uncomment the line below if you use the dropdown variation)
  //$('.collapsible').collapsible();
  $("li.tab a").on("click", function (e) {
      window.location = $(this).attr('href');
  });
});
