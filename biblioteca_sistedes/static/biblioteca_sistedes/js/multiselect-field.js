window.onload = function() {
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
}
