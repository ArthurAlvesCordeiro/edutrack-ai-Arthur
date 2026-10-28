// Delete a subject by ID for the authenticated user
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id
  }

  stack {
    // Retrieve existing subject record
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $subject

    // Verify record exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Verify ownership by authenticated user
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied to this subject."
    }

    // Delete the subject record
    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }

    // Log deletion action
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "delete_subject"
        metadata: $subject
      }
    } as $event_log
  }

  response = {
    success: true
    message: "Subject deleted successfully"
    id     : $input.subjects_id
  }
}