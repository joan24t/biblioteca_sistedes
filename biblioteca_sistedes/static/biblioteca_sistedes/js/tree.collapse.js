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
});