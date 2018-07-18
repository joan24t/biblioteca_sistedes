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


        if(key){
            var content = document.querySelectorAll('[id=text-hightlight]');
            for(var i=0; i<content.length; i++) {
              var matches = content[i].innerHTML.match(new RegExp(key.toString(), 'gi'))
              for (var j in matches){

                    content[i].innerHTML = content[i].innerHTML.replace(new RegExp(matches[j], 'gi'), "<span class='highlight'>" + matches[j] + '</span>');
                }
            }


        }
        var parts = String(window.location.href).split('/');
        var section = parts[parts.length - 2];
        var section2 = parts[parts.length - 3];
        var current = jQuery("." + String(section))
        var current2 = jQuery("." + String(section2))
        if (current2.length){
            activate_tree(jQuery(".first-child"), jQuery(".conferencias-selected"), jQuery(".first-hit" + "-li-hitarea"), jQuery(".first-hit-li"));
            activate_tree(jQuery(".child-" + section2), current2, jQuery(".hit-" + section2 + "-li-hitarea"), jQuery(".hit-" + section2 + "-li"));
            activate_tree(jQuery(".child-" + section2 + "-" + section), jQuery("." + section2 + "-" + section), jQuery(".hit-" + section2 + "-" + section + "-li-hitarea"), jQuery(".hit-" + section2 + "-" + section + "-li"));

        }
        else if (current.length){
            activate_tree(jQuery(".first-child"), jQuery(".conferencias-selected"), jQuery(".first-hit" + "-li-hitarea"), jQuery(".first-hit-li"));
            activate_tree(jQuery(".child-" + section), current, jQuery(".hit-" + section + "-li-hitarea"), jQuery(".hit-" + section + "-li"));

        }



//                jQuery.ajax({
//      url: "/biblioteca/conferencias/"
//    }).done(function() {
//        alert("PathName  ="+ window.location.pathname);
//      jQuery("#pepe").addClass( "selected" );
//    });



});