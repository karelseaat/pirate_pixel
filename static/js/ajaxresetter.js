
function resetajax(url)
{
  fetch(url)
    .then((response) => {
    })
    .then((data) => {
    });

    u('div#maincontent').html('<div class="row">Het device is nu aan het resetten, probeer over enkele momenten te herverbinden naar het orginele ip of het nieuwe ip dat aan dit device gegeven is na een verbinding met je Accespoint !</div>');

    // setTimeout(function(){
    //   window.location.href = 'http://localhost:8080';
    // }, 5000);
}
