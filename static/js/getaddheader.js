function getafetch(targ)
{
  fetch(targ.first().getAttribute('url'), {
      method: "GET",
      headers: {
        'authorization': targ.first().getAttribute('authentication')
      }
    })
    .then(function(response) {
    response.text().then(function(text) {
        u(targ.first()).text(text)
      })
  })
}

function getaddheaders() {

  var target = u('#blonk');

  // console.log(target.nodes.length)

  if (target.nodes.length > 0) {
    setInterval(getafetch, 1000, target);


  }

}
