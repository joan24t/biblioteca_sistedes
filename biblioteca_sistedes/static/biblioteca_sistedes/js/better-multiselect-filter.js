jQuery(document).ready(function() {
   var inp = document.getElementsByClassName("multiselect");
        for(i = 0; i < inp.length; i++){
               multi( inp[i],{
          // enable search
          enable_search: true,
          // placeholder of search input
          search_placeholder: 'Search...',
          non_selected_header: null,
          selected_header: null,
                });

            }

    jQuery('[name="username"]').keyup(function(){
        var username = jQuery(this).val();
        check_data(username, 'username');
        });

    jQuery('[name="email"]').keyup(function(){
        var email = jQuery(this).val();
        check_data(email, 'email');
    });

    jQuery('#pass_user_2').keyup(function(){
        var password_1 = jQuery('[name="password"]').val();
        var password_2 = jQuery(this).val();
        check_password(password_1, password_2);
    });

    jQuery('[name="password"]').keyup(function(){
        var password_1 = jQuery(this).val();
        var password_2 = jQuery('#pass_user_2').val();
        check_password(password_1, password_2);

    });
});
function check_password(pass1, pass2){
    if (pass1 != pass2){
        jQuery(".match-password").css("display", "block");
        jQuery(".text-match-password").text("Las contraseñas no coinciden");
    }
    else{
        jQuery(".match-password").css("display", "none");
    }
}


function check_data(value, object){
    var text = object == 'email' ? 'Email no disponible.' : 'Nombre de usuario no disponible'
    jQuery.ajax({
      url: '/check_user/',
      data: {
        'value': value,
        'object': object,
      },
      dataType: 'json',
      success: function (data) {
        if (data.is_taken) {
          jQuery(".error-" + object).css("display", "block");
          jQuery(".text-error-" + object).text(text);
        }
        else{
           jQuery(".error-" + object).css("display", "none");
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
//        var xmlhttp = new XMLHttpRequest();
//        xmlhttp.onreadystatechange = function() {
//            if (this.readyState == 4 && this.status == 200) {
//                document.getElementById("txtHint").innerHTML = this.responseText;
//            }
//        }
//        xmlhttp.open("GET", "gethint.php?q="+str, true);
//        xmlhttp.send();
    }
}

function search_table() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
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
        document.getElementById("arrow-menu").style= "display:block; position: relative;";
    }
    else {
        document.getElementById("arrow-menu").style= "display:none; position: relative;";
    }
}

function close_cookies(){
    document.getElementById("cookies").style= "display:none;";
}
