use serde::{Serialize, Deserialize};
use log::{info, error, debug};

#[derive(Debug, Serialize, Deserialize)]
pub enum Commands {
    // it is a enum member with tuple
    /// create a database
    CreateDB(String),
    /// Connect to a database
    ConnectDB(String)
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub enum Response {
    Ok,
    Msg(String),
    Err(String)
}

pub fn parse_command(mut cmd: String) -> Option<Commands> {
    if cmd.ends_with('\n') {
        // remove the last character '\n'
        cmd.pop();
        if cmd.ends_with('\r') {
            cmd.pop();
        }
    }
    if cmd.ends_with('\r') {
        cmd.pop();
    }

    if cmd.starts_with("create ") {
        return Some(Commands::CreateDB(cmd[7..].to_string()));
    }
    else if cmd.starts_with("connect ") {
        return Some(Commands::ConnectDB(cmd[8..].to_string()));
    }
    else {
        return None;
    }
}