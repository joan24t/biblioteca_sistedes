jQuery(document).ready(function() {

    var table = document.getElementById("myTable");
    if (table) {
        sortTable();
    }
    jQuery('[name="username"]').keyup(function(){
        var username = jQuery(this).val();
        check_data(username, 'username');
        });

    jQuery('[name="email"]').keyup(function(){
        var email = jQuery(this).val();
        check_data(email, 'email');
    });

    jQuery('#name_con').keyup(function(){
        var nameconference = jQuery(this).val();
        check_data(nameconference, 'name-conference');
    });

    jQuery('#dom_con').keyup(function(){
        var domainconference = jQuery(this).val();
        check_data(domainconference, 'domain-conference');
    });

    jQuery('#pass_user_2').keyup(function(){
        var password_1 = jQuery('[name="password"]').val();
        var password_2 = jQuery(this).val();
        check_password(password_1, password_2, 'n');
    });

    jQuery('[name="password"]').keyup(function(){
        var password_1 = jQuery(this).val();
        var password_2 = jQuery('#pass_user_2').val();
        check_password(password_1, password_2, 'n');

    });

    jQuery('#pass_user_1_wizard').keyup(function(){
        var password_2 = jQuery('#pass_user_2_wizard').val();
        var password_1 = jQuery(this).val();
        check_password(password_1, password_2, 'w');
    });

    jQuery('#pass_user_2_wizard').keyup(function(){
        var password_2 = jQuery(this).val();
        var password_1 = jQuery('#pass_user_1_wizard').val();
        check_password(password_1, password_2, 'w');

    });
});

function check_error(object){
    if (object == 'u'){
        if(jQuery('.error-username').css('display') == 'block' || jQuery('.error-email').css('display') == 'block' || jQuery('.match-password').css('display') == 'block')
        {
            jQuery(".form-submit").prop('disabled', true);
        }
        else{
            jQuery(".form-submit").prop('disabled', false);
        }
    }
    else if (object == 'c'){
        if(jQuery('.error-name-conference').css('display') == 'block' || jQuery('.error-domain-conference').css('display') == 'block')
        {
            jQuery(".form-submit").prop('disabled', true);
        }
        else{
            jQuery(".form-submit").prop('disabled', false);
        }
    }
}

function check_password(pass1, pass2, type){
    if (type == 'n'){
        if (pass1 != pass2){
            jQuery(".form-submit").prop('disabled', true);
            jQuery(".match-password").css("display", "block");
            jQuery(".text-match-password").text("Las contraseñas no coinciden");
            check_error('u')
        }
        else{
            jQuery(".form-submit").prop('disabled', false);
            jQuery(".match-password").css("display", "none");
            check_error('u')
        }
    }
    else if (type == 'w'){
        if (pass1 != pass2){
            jQuery(".form-submit-wizard").prop('disabled', true);
            jQuery(".match-password-wizard").css("display", "block");
            jQuery(".text-match-password-wizard").text("Las contraseñas no coinciden");
        }
        else{
            jQuery(".form-submit-wizard").prop('disabled', false);
            jQuery(".match-password-wizard").css("display", "none");
        }
    }
}


function check_data(value, object){
    var text = ''
    if (object == 'email') text = 'Email no disponible.'
    else if (object == 'username') text = 'Nombre de usuario no disponible'
    else if (object == 'name-conference') text = 'Nombre de conferencia no disponible.'
    else if (object == 'domain-conference') text = 'Abreviatura no disponible.'
    jQuery.ajax({
      url: '/check_data/',
      data: {
        'value': value,
        'object': object,
      },
      dataType: 'json',
      success: function (data) {
        if (data.is_taken) {
          jQuery(".error-" + object).css("display", "block");
          jQuery(".form-submit").prop('disabled', true);
          jQuery(".text-error-" + object).text(text);
          if (object == 'email' || object == 'username'){
              check_error('u')
            }
          else if (object == 'name-conference' || object == 'domain-conference'){
              check_error('c')
          }
        }
        else{
            jQuery(".form-submit").prop('disabled', false);
            jQuery(".error-" + object).css("display", "none");
            if (object == 'email' || object == 'username'){
                check_error('u')
              }
            else if (object == 'name-conference' || object == 'domain-conference'){
                check_error('c')
            }
        }
      }
    });
}

function check_rol(){
    jQuery.ajax({
      url: '/check_rol/',
      dataType: 'json',
      success: function (data) {
        if (data.rol == 2) {
          document.getElementById("arrow-menu").style= "display:block; position: relative; height: 160px;";
        }
        else if (data.rol == 3){
            document.getElementById("arrow-menu").style= "display:block; position: relative; height: 135px;";
        }
        else{
            document.getElementById("arrow-menu").style= "display:block; position: relative; height: 260px;";
        }
      }
    });
}

document.onclick = function(event) {
    if (!jQuery(event.target).hasClass( "focusout-except" ) && !jQuery(event.target).hasClass( "fa" )) {
        jQuery("#arrow-menu").css("display", "none");
    }
};


function showHint(str) {
    if (str.length == 0) {
        document.getElementById("txtHint").innerHTML = "";
        return;
    } else {
        document.getElementById("txtHint").innerHTML = str;
    }
}

function search_table() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}


function dropdown(){
    var element = document.getElementById('arrow-menu'),
    style = window.getComputedStyle(element),
    display = style.getPropertyValue('display');
    if (display === 'none'){
        check_rol();
    }
    else {
        document.getElementById("arrow-menu").style= "display:none; position: relative;";
    }
}

function close_cookies(){
    document.getElementById("cookies").style= "display:none;";
}

function clicked(e)
{
    if(!confirm('¿Estás seguro de eliminar el registro?'))e.preventDefault();
}

function sortTable() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("myTable");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      //check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
    }
}
