// Create a new academic subject for the authenticated user
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text teacher filters=trim
    int hours
  }

  stack {
    // Validate required fields
    precondition ($input.name != null && $input.name != "") {
      error_type = "badrequest"
      error = "Subject name is required."
    }

    precondition ($input.teacher != null && $input.teacher != "") {
      error_type = "badrequest"
      error = "Teacher name is required."
    }

    precondition ($input.hours != null && $input.hours > 0) {
      error_type = "badrequest"
      error = "Hours must be greater than zero."
    }

    // Persist new subject record associated with the authenticated user
    db.add subjects {
      data = {
        name   : $input.name
        teacher: $input.teacher
        hours  : $input.hours
        user_id: $auth.id
      }
    } as $new_subject

    // Create event log for subject creation
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "create_subject"
        metadata: $new_subject
      }
    } as $event_log
  }

  response = $new_subject
}