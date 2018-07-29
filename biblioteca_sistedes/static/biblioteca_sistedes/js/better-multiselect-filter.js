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
});


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
