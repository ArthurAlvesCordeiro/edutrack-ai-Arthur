// Stores academic subjects associated with users.
table subjects {
  auth = false

  schema {
    int id
    text name filters=trim
    text teacher filters=trim
    int hours

    // Reference to the user who owns or is associated with the subject.
    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]
}
