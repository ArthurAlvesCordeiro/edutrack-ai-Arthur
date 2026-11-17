query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text q? filters=trim
    bool has_overdue?
    date reference_date?
  }

  stack {
    precondition (($input.q != null && $input.q != "") || $input.has_overdue == true) {
      error_type = "inputerror"
      error = "Provide either a non-empty query or set has_overdue=true."
    }

    // Retrieve only subjects owned by the authenticated user.
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      output = ["id", "name"]
      return = {type: "list"}
    } as $search_subjects

    // Retrieve tasks only when their related subject belongs to this user.
    db.query academic_tasks {
      join = {
        subjects: {
          table: "subjects",
          type: "inner",
          where: $db.academic_tasks.subject_id == $db.subjects.id
        }
      }
      where = $db.subjects.user_id == $auth.id
      output = ["id", "subject_id", "due_date", "status"]
      return = {type: "list"}
    } as $search_tasks

    // Build the payload expected by the Python FastAPI service.
    var $search_payload {
      value = {
        subjects: $search_subjects,
        tasks: $search_tasks,
        query: $input.q,
        has_overdue: $input.has_overdue ?? false,
        reference_date: $input.reference_date
      }
    }

    // Execute the real HTTP request to the Python service.
    api.request {
      url = $env.SEARCH_API_URL
      method = "POST"
      params = $search_payload
      headers = [
        "Content-Type: application/json",
        "X-API-Key: " ~ $env.SEARCH_API_KEY
      ]
      timeout = 30
    } as $python_search

    // Ensure the Python service returned a successful HTTP status.
    precondition ($python_search.response.status >= 200 && $python_search.response.status < 300) {
      error_type = "standard"
      error = "Python search service failed. HTTP " ~ ($python_search.response.status|to_text)
    }
  }

  response = $python_search.response.result
}
