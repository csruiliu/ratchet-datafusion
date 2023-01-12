use std::fmt::{Display, Formatter};
use std::fs;
use std::io::{Read, BufWriter, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::mpsc;

use clap::{Arg, Command};
use serde::{Deserialize};
use log::{info, error, debug};
use datafusion::prelude::*;

#[tokio::main]
async fn main() -> datafusion::error::Result<()> {
    // register the table
    let ctx = SessionContext::new();
    ctx.register_csv("example", "test/example.csv", CsvReadOptions::new()).await?;

    // create a plan to run a SQL query
    let df = ctx.sql("SELECT a, MIN(b) FROM example GROUP BY a LIMIT 100").await?;

    // execute and print results
    df.show().await?;
    Ok(())
}
