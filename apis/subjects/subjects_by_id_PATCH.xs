// Update an existing subject for the authenticated user
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id
    text name? filters=trim
    text teacher? filters=trim
    int hours?
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

    var $name_to_save {
      value = $input.name
    }

    conditional {
      if ($name_to_save == null || $name_to_save == "") {
        var.update $name_to_save {
          value = $subject.name
        }
      }
    }

    var $teacher_to_save {
      value = $input.teacher
    }

    conditional {
      if ($teacher_to_save == null || $teacher_to_save == "") {
        var.update $teacher_to_save {
          value = $subject.teacher
        }
      }
    }

    var $hours_to_save {
      value = $input.hours
    }

    conditional {
      if ($hours_to_save == null || $hours_to_save <= 0) {
        var.update $hours_to_save {
          value = $subject.hours
        }
      }
    }

    // Update subject record in the database
    db.edit subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = {
        name   : $name_to_save
        teacher: $teacher_to_save
        hours  : $hours_to_save
      }
    } as $updated_subject

    // Log update action
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "update_subject"
        metadata: $updated_subject
      }
    } as $event_log
  }

  response = $updated_subject
}