$(document).ready(function() {
    // New entry form autocomplete
    $('#new_entry_form #project').autocomplete({
        source: '/ajax/project/list'
    });
});
