// Get a single subject by ID for the authenticated user
query "subjects/{subjects_id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id
  }

  stack {
    // Retrieve the subject record by ID
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $subject

    // Ensure the subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Verify ownership by the authenticated user
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied to this subject."
    }
  }

  response = $subject
}