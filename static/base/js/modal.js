
function modal_func(modal_id, close_id) {
  var modal = document.getElementById(modal_id);
  var closer = document.getElementById(close_id);

  modal.style.display = "block";

  closer.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}