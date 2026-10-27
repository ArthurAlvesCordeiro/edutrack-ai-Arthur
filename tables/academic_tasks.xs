// Stores academic tasks and assignments associated with subjects.
table academic_tasks {
  auth = false

  schema {
    int id
    text title filters=trim
    text description
    date due_date
    text status filters=trim

    // Reference to the subject associated with the academic task.
    int subject_id {
      table = "subjects"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
  ]
}