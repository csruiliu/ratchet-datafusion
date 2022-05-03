use std::fmt::{Display, Formatter};
use std::fs;
use std::io::{Read, BufWriter, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::mpsc;

use clap::{Arg, Command};
use serde::{Deserialize};
use log::{info, error, debug};


#[derive(Debug, Deserialize)]
struct ServerConfig {
    server_ip: String,
    port: String,
    db_path: String
}

impl Display for ServerConfig {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "Server IP {} on Port {}", self.server_ip, self.port)
    }
}

fn handle_request(stream: TcpStream) {
    info!("Client connected");
    let mut writer = BufWriter::new(&stream);
    writer.write_all("Red".as_bytes());
    let mut reader = BufReader::new(&stream);
    let mut response = String::new();
    reader.read_to_string(&mut response);
    info!("Server received {}", response);
}

fn main() {
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
        .arg(Arg::new("db_path")
                .short('d')
                .long("db_path")
                .value_name("DB_PATH")
                .default_value("persist/db/")
                .help("Path where DB is stored")
                .takes_value(true))
        .get_matches();

    let config = if let Some(c) = m.value_of("config") {
        let config_path = c;
        let contents = fs::read_to_string(config_path).unwrap();
        serde_json::from_str(&contents).unwrap()
    } else {
        let server_ip = m.value_of("server").unwrap();
        let port = m.value_of("port").unwrap();
        let db_path = m.value_of("db_path").unwrap();
        ServerConfig {
            server_ip: server_ip.to_string(),
            port: port.to_string(),
            db_path: db_path.to_string()
        }
    };

    info!("Starting Ratchet at {} ...", config);

    // Create channel / queue for jobs
    // let (sender, receiver) = mpsc::channel();

    let mut bind_addr = config.server_ip.clone();
    bind_addr.push(':');
    bind_addr.push_str(&config.port);
    let listener = TcpListener::bind(bind_addr).unwrap();

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                debug!("New connection: {}", stream.peer_addr().unwrap());
                handle_client(stream);
            }
            Err(e) => {
                error!("Error: {}", e);
            }
        }
    }
}
