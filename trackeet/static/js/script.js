$(document).ready(function() {
    validator = new EntryFormValidator();
});

function EntryFormValidator() {

    // find form fields
    this.duration = $('#new_entry_form #duration');
    this.formatted_duration = $('#new_entry_form #formatted_duration');
    this.project = $('#new_entry_form #project');
    this.stub = $('#new_entry_form #stub');


    // Bind functions to different events
    this.bindEvents = function() {
        this.formatted_duration.bind('blur', {caller: this}, this.convertDurationField);
    }

    // Configure the different autocompletes
    this.bindAutocompletes = function() {
        this.project.autocomplete({
            source: '/ajax/project/list'
        });
    }

    /**
     * Take the submitted duration, and convert it to the 'hh:mm' format
     */
    this.convertDurationField = function(event) {
        caller = event.data.caller;
        input = $(this);
        value = input.val();
        duration = parseInt(value);
        lastChar = value.charAt(value.length - 1);

        if(isNaN(duration))
        {
            return
        }

        // Strings ends with 'h', we're talking about hours
        if(lastChar == 'h')
        {
            duration *= 60;
        }

        // Convert duration (s) in a formatted hh:mm string
        if(duration < 60)
        {
            hh = 0;
            mm = duration;
        }
        else
        {
            hh = Math.floor(duration/60);
            mm = duration - (hh * 60);
        }

        prefix = '';
        if(mm < 10)
            prefix = '0';
        formattedDuration = '' + hh + ':' + prefix + mm;

        caller.duration.val(duration);
        $(this).val(formattedDuration);
    }

    this.bindEvents();
    this.bindAutocompletes();
}
