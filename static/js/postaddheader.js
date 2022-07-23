function addpostheaders()
{

  u('form#ajaxpost').on('submit', function(e){
    e.preventDefault();

    fetch(e.target.action, { body: u(this).serialize(), method: "POST", headers: {'authorization': u(this).first().getAttribute('authentication')} })
    .then(
      function(response) {
        console.log(response.text())
      }
    );

  });
}
