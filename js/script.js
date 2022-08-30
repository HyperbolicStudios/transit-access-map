jQuery(document).on("keypress", 'form', function(e) {
  var code = e.keyCode || e.which;
  if (code == 13) {
    e.preventDefault();
    return false;
  }
});

function openNav() {
  document.getElementById("menu").style.transform = "translateX(0)";
  console.log("open");
}

function closeNav() {
  document.getElementById("menu").style.transform = "translateX(100%)";
}

var selected_mode = "Bus";
var selected_destination = "UVic";

function swapMap() {
  $('#main-title').text("Travel time to " + selected_destination + " by " + selected_mode);
  var path = "maps/" + selected_destination + "_" + selected_mode + " Time.html";
  console.log(path);
  $(".map").each(function(i) {
    if ($(this).attr('src') == path) {
      $(this).css("display", "block");
    } else {
      $(this).css("display", "none");
    }
  });

}

function update(sel) {
  console.log("Processing");
  if (sel.className == 'destination') {
    $(".destination").css("background-color", "#ebebeb");
    $('.destination').attr("aria-pressed", "false")
    $(sel).css("background-color", "#c4c4c4");
    $(sel).attr("aria-pressed", "true")
    selected_destination = $(sel).text();
    console.log(selected_destination);
    swapMap();
  }

  if (sel.className == 'mode') {
    $(".mode").css("background-color", "#ebebeb");
    $('.mode').attr("aria-pressed", "false")
    $(sel).css("background-color", "#c4c4c4");
    $('.mode').attr("aria-pressed", "true");
    selected_mode = $(sel).text();
    console.log(selected_mode);
    swapMap();

  }
}

$('.destination').first().css("background-color", "#c4c4c4");
$('.mode').first().css("background-color", "#c4c4c4");
$('.map').first().css("display", "block");
