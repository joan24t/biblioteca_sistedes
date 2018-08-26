window.onload = function(){
// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var button_close = document.getElementById("close-form");


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
    document.getElementById('pass_user_1_wizard').value = '';
    document.getElementById('pass_user_2_wizard').value = '';
}

button_close.onclick = function() {
    modal.style.display = "none";
    document.getElementById('pass_user_1_wizard').value = '';
    document.getElementById('pass_user_2_wizard').value = '';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementById('pass_user_1_wizard').value = '';
        document.getElementById('pass_user_2_wizard').value = '';
    }
}
}

// When the user clicks the button, open the modal
function showWizardPassword(user_id) {
    var modal = document.getElementById('myModal');
    var user_id = document.getElementById('userId').value = user_id;
    modal.style.display = "block";
}
