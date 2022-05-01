use std::fmt::{Display, Formatter};
use std::fs;
use std::net::TcpStream;

use env_logger;
use log::{info, error, debug};
use serde::{Deserialize};
use clap::{Arg, Command};
use env_logger::Env;
use rustyline::error::ReadlineError;
use rustyline::Editor;

#[derive(Debug, Deserialize)]
struct ClientConfig {
    server_ip: String,
    port: String
}

impl Display for ClientConfig {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "Server IP {} on Port {}", self.server_ip, self.port)
    }
}

fn process_cli_input(stream: &mut TcpStream) {
    let mut rl = Editor::<()>::new();
    if rl.load_history("history_txt").is_err() {
        println!("No previous history.");
    }
    let prompt: &str = "[ratchet]>>";
    loop {
        let readline = rl.readline(prompt);
        match readline {
            Ok(line) => {
                if line.as_str() == "" {
                    continue;
                }
                rl.add_history_entry(line.as_str());
                println!("Input: {}", line);
            }
            Err(ReadlineError::Interrupted) => {
                println!("CTRL-C");
                break
            }
            Err(ReadlineError::Eof) => {
                println!("CTRL-D");
                break
            }
            Err(err) => {
                println!("Error: {:?}", err);
                break
            }
        }
    }
}

fn main() {
    // creat a logger with default "info" level
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();

    // use clap crate to get arguments from command-line interface
    let m = Command::new(env!("CARGO_PKG_NAME"))
        .version(env!("CARGO_PKG_VERSION"))
        .arg(Arg::new("config")
                .short('c')
                .long("config")
                .value_name("CONFIG_FILE")
                .help("Config file for client")
                .takes_value(true)
                .required(false))
        .arg(Arg::new("server")
                .short('s')
                .long("server")
                .value_name("SERVER_IP")
                .default_value("127.0.0.1")
                .help("Server IP address")
                .takes_value(true))
        .arg(Arg::new("port")
                .short('p')
                .long("port")
                .value_name("SERVER_PORT")
                .default_value("3333")
                .help("Server port number")
                .takes_value(true))
        .get_matches();

    let config:ClientConfig = if let Some(c) = m.value_of("config") {
        let config_path = c;
        let contents = fs::read_to_string(config_path).unwrap();
        serde_json::from_str(&contents).unwrap()
    } else {
        let server_ip = m.value_of("server").unwrap();
        let port = m.value_of("port").unwrap();
        ClientConfig {
            server_ip: server_ip.to_string(),
            port: port.to_string()
        }
    };

    info!("Starting client with config: {}", config);

    let mut bind_addr = config.server_ip.clone();
    bind_addr.push(':');
    bind_addr.push_str(&config.port);

    info!("Starting to connect {}", bind_addr);

    match TcpStream::connect(bind_addr) {
        Ok(mut stream) => {
            process_cli_input(&mut stream);
        }
        Err(e) => {
            error!("Failed to connect: {}", e);
        }
    }

    info!("Client is terminated.");
}
