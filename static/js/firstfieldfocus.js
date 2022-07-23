

function focusfirstinput() {
  let element = u('form').find('input');

  if (element.first())
  {
    element.first().focus();
  }
}
