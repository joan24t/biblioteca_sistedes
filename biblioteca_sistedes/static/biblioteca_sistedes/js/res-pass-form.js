window.onload = function(){
// Get the modal
var modal = document.getElementById('myModal');
var modal_file = document.getElementById('myModal-file');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span_file = document.getElementsByClassName("close-file")[0];

var button_close = document.getElementById("close-form");
var button_close_file = document.getElementById("close-form-file");


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
    document.getElementById('pass_user_1_wizard').value = '';
    document.getElementById('pass_user_2_wizard').value = '';
}

span_file.onclick = function() {
    modal_file.style.display = "none";
    document.getElementById('articleFile').value = '';
}

button_close.onclick = function() {
    modal.style.display = "none";
    document.getElementById('pass_user_1_wizard').value = '';
    document.getElementById('pass_user_2_wizard').value = '';
}

button_close_file.onclick = function() {
    modal_file.style.display = "none";
    document.getElementById('articleFile').value = '';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementById('pass_user_1_wizard').value = '';
        document.getElementById('pass_user_2_wizard').value = '';
    }
    else if (event.target == modal_file) {
        modal_file.style.display = "none";
        document.getElementById('articleFile').value = '';
    }
}
}

// When the user clicks the button, open the modal
function showWizardPassword(user_id) {
    var modal = document.getElementById('myModal');
    var user_id = document.getElementById('userId').value = user_id;
    modal.style.display = "block";
}

function showWizardArticleFile(articleid, objectType) {
    var modal_file = document.getElementById('myModal-file');
    document.getElementById('articleId').value = articleid;
    document.getElementById('objectType').value = objectType;
    modal_file.style.display = "block";
}
