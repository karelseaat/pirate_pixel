
function listener(element) {
  u(element.target).parent().find('p').first().classList.toggle("show");
  // elem3ent.target
}

function showfaqclick() {
  let elements = u('h2.clickshow')
  elements.each(function(node, i){
    u(node).on('click', listener);
  });


}
