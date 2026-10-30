table academic_tasks {
  auth = false

  schema {
    int id
    text title filters=trim
    text description
    date due_date
    text status

    int subject_id {
      table = "subjects"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]
}
