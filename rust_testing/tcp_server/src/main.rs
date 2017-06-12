extern crate daemonize;
use std::io::Write;
use std::net::TcpListener;
use std::thread;

fn ellida_daemon_listener() {
    let listener = TcpListener::bind("127.0.0.1:9123").unwrap();
    println!("listening started, ready to accept");
    for stream in listener.incoming() {
        thread::spawn(|| {
            let mut stream = stream.unwrap();
            stream.write(b"Hello World\r\n").unwrap();
        });
    }
}

fn main() {
    ellida_daemon_listener();
}
