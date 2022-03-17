$(document).ready(function () {
  $("body").on("keyup", "input", function (e) {
    var inputs = $("input");

    if (e.keyCode == 8) {
      var index = inputs.index(this);
      if (index != 0)
        inputs
          .eq(index - 1)
          .val("")
          .focus();
    } else {
      if ($(this).val().length === this.size) {
        inputs.eq(inputs.index(this) + 1).focus();
      }
    }
  });
});

document.querySelectorAll('input').forEach((input) => {
  input.oninput = function() {
    let { nextElementSibling } = this;
    while (nextElementSibling && nextElementSibling.tagName !== 'INPUT') {
      nextElementSibling = nextElementSibling.nextElementSibling;
    }
    if (nextElementSibling) {
      nextElementSibling.focus();
    }
  }
});

const submitBtn = document.getElementById('submit');
const one = document.getElementById('one');
const two = document.getElementById('two');
const three = document.getElementById('three');
const four = document.getElementById('four');
const five = document.getElementById('five');

function updateSubmitBtn(){
  const oneValue = one.value.trim();
  const twoValue = two.value.trim();
  const threeValue = three.value.trim();
  const fourValue = four.value.trim();
  const fiveValue = five.value.trim();
  debugger;
  if(oneValue && twoValue && threeValue && fourValue && fiveValue){
    submitBtn.removeAttribute('disabled');
  }else{
    submitBtn.setAttribute('disabled', 'disabled');
  }
}

one.addEventListener('change', updateSubmitBtn)
two.addEventListener('change', updateSubmitBtn)
three.addEventListener('change', updateSubmitBtn)
four.addEventListener('change', updateSubmitBtn)
five.addEventListener('change', updateSubmitBtn)
