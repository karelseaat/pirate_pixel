

function showWhenError() {
  let element = u('div#snackbar')

  if (element.text() !== "")
  {
    element.addClass("show");
    setTimeout(function(){ element.removeClass("show"); }, 2900);
  }
}
