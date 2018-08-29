window.onload = function(){
// Get the modal
var modal = document.getElementById('myModal');
var modal_file = document.getElementById('myModal-file');
var modal_keyword = document.getElementById('myModal-keyword');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span_file = document.getElementsByClassName("close-file")[0];
var span_keyword = document.getElementsByClassName("close-keyword")[0];

var button_close = document.getElementById("close-form");
var button_close_file = document.getElementById("close-form-file");
var button_close_keyword = document.getElementById("close-form-keyword");


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

span_keyword.onclick = function() {
    modal_keyword.style.display = "none";
    document.getElementById('keywordWizard').value = '';
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

button_close_keyword.onclick = function() {
    modal_keyword.style.display = "none";
    document.getElementById('keywordWizard').value = '';
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
    else if (event.target == modal_keyword) {
        modal_keyword.style.display = "none";
        document.getElementById('keywordWizard').value = '';
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

function showWizardKeyWord(keyid, keyname) {
    var modal_keyword = document.getElementById('myModal-keyword');
    var key_id = document.getElementById('keywordId');
    if (keyname != null && keyid != null){
         document.getElementById('keywordWizard').value = keyname;
         document.getElementById('keywordId').value = keyid;
    }
    else document.getElementById('keywordWizard').value = '';
    modal_keyword.style.display = "block";
}
