function activate_tree(section, current, exp, li){
        current.addClass( "selected" );
        section.css({ display: "block" });
        exp.removeClass("expandable-hitarea");
        exp.removeClass("lastExpandable-hitarea");
        li.removeClass("expandable");
        li.removeClass("lastExpandable");
        exp.addClass("collapsable-hitarea");
        exp.addClass("lastCollapsable-hitarea");
        li.addClass("collapsable");
        li.addClass("lastCollapsable");
}

jQuery(document).ready( function( ) {
        jQuery("#tree1").treeview({
            persist: "location",
            cookieId: "treeview1",
            animated: "fast",
            collapsed: true
        });
        jQuery("#tree2").treeview({
            persist: "location",
            cookieId: "treeview1",
            animated: "fast",
            collapsed: true
        });


        var current_url = window.location.href;
        var str_url = new URL(current_url);
        var key = str_url.searchParams.get("s");
        var txtAutor = str_url.searchParams.get("txtAutor");
        var txtTitulo= str_url.searchParams.get("txtTitulo");
        var txtKeyword = str_url.searchParams.get("txtKeyword");
        var txtAfiliacion = str_url.searchParams.get("txtAfiliacion");


        if(key || txtAutor || txtTitulo || txtKeyword || txtAfiliacion){
            var list = []
            if (key) list.push(key);
            if (txtAutor) list.push(txtAutor);
            if (txtTitulo) list.push(txtTitulo);
            if (txtKeyword) list.push(txtKeyword);
            if (txtAfiliacion) list.push(txtAfiliacion);

            list.forEach(function(element) {
            var content = document.querySelectorAll('[id=text-hightlight]');
            for(var i=0; i<content.length; i++) {
              var matches = content[i].innerHTML.match(new RegExp(element.toString(), 'gi'))
                  for (var j in matches){

                        content[i].innerHTML = content[i].innerHTML.replace(new RegExp(matches[j], 'gi'), "<span class='highlight'>" + matches[j] + '</span>');
                    }
                }
            });

        }


        var parts = String(window.location.href).split('/');
        var section = parts[parts.length - 2];
        var section2 = parts[parts.length - 3];
        var section3 = parts[parts.length - 4];
        var section4 = parts[parts.length - 5];
        var current = jQuery('.' + String(section))
        var current2 = jQuery('.' + String(section2))
        var current3 = jQuery('.' + String(section3))
        var bulletin = jQuery(".boletines-" + String(section))
        var bulletin2 = jQuery(".boletines-" + String(section2))
        if (current3.length && (section4 == 'conferencias')){
            activate_tree(jQuery(".first-child"), jQuery(".conferencias-selected"), jQuery(".first-hit-li-hitarea"), jQuery(".first-hit-li"));
            activate_tree(jQuery(".child-" + section3), current3, jQuery(".hit-" + section3 + "-li-hitarea"), jQuery(".hit-" + section3 + "-li"));
            activate_tree(jQuery(".child-" + section3 + "-" + section2), jQuery("." + section3 + "-" + section2), jQuery(".hit-" + section3 + "-" + section2 + "-li-hitarea"), jQuery(".hit-" + section3 + "-" + section2 + "-li"));
            jQuery(".track-to-select-" + section).addClass( "selected" );
        }
        else if (current2.length && (section3 == 'conferencias')){
            activate_tree(jQuery(".first-child"), jQuery(".conferencias-selected"), jQuery(".first-hit-li-hitarea"), jQuery(".first-hit-li"));
            activate_tree(jQuery(".child-" + section2), current2, jQuery(".hit-" + section2 + "-li-hitarea"), jQuery(".hit-" + section2 + "-li"));
            activate_tree(jQuery(".child-" + section2 + "-" + section), jQuery("." + section2 + "-" + section), jQuery(".hit-" + section2 + "-" + section + "-li-hitarea"), jQuery(".hit-" + section2 + "-" + section + "-li"));

        }
        else if (current.length && (section2 == 'conferencias')){
            activate_tree(jQuery(".first-child"), jQuery(".conferencias-selected"), jQuery(".first-hit-li-hitarea"), jQuery(".first-hit-li"));
            activate_tree(jQuery(".child-" + section), current, jQuery(".hit-" + section + "-li-hitarea"), jQuery(".hit-" + section + "-li"));

        }
        else if (bulletin2.length && (section3 == 'boletines-prensa')){
            activate_tree(jQuery(".first-child-boletin"), jQuery(".boletines-selected"), jQuery(".first-hit-li-hitarea"), jQuery(".first-hit-li-boletines"));
            activate_tree(jQuery(".child-" + section2), bulletin2, jQuery(".hit-" + section2 + "-li-hitarea"), jQuery(".hit-" + section2 + "-li"));
            jQuery(".bulletin-to-select-" + section).addClass( "selected" );
        }
        else if (bulletin.length && (section2 == 'boletines-prensa')){
            activate_tree(jQuery(".first-child-boletin"), jQuery(".boletines-selected"), jQuery(".first-hit-li-hitarea"), jQuery(".first-hit-li-boletines"));
            activate_tree(jQuery(".child-" + section), bulletin, jQuery(".hit-" + section + "-li-hitarea"), jQuery(".hit-" + section + "-li"));

        }
        else if (current.length && (section2 == 'documentos-sistedes')){
            activate_tree(jQuery(".first-child-documentos"), jQuery(".documentos-selected"), jQuery(".first-hit-li-documentos-hitarea"), jQuery(".first-hit-li-documentos"));
            jQuery("." + section).addClass( "selected" );

        }



//                jQuery.ajax({
//      url: "/biblioteca/conferencias/"
//    }).done(function() {
//        alert("PathName  ="+ window.location.pathname);
//      jQuery("#pepe").addClass( "selected" );
//    });



});
