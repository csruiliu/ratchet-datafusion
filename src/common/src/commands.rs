
pub enum Commands {
    // it is a enum member with tuple
    /// create a database
    CreateDB(String),
    /// Connect to a database
    ConnectDB(String),
    /// Import a database
    ImportDB(String)
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub enum Response {
    Ok,
    Msg(String),
    Err(String)
}