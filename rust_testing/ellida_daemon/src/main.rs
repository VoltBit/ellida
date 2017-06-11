extern crate daemonize;
extern crate syslog;
#[macro_use] extern crate log;

use daemonize::{Daemonize};
use syslog::{Facility,Severity};
use std::{thread, time};

fn syslog_test() {
    match syslog::unix(Facility::LOG_USER) {
        Err(e)      => println!("impossible to connect to syslog: {:?}", e),
        Ok(writer)  => {
            let r = writer.send(Severity::LOG_ALERT, "syslog test OK");
            if r.is_err() {
                println!("error sending the log {}", r.err().expect("got error"));
            }
        }
    }
}

let local_logger: Box<Logger>;
let external_logger: Box<Logger>;

fn action_test() {

    local_logger = syslog::unix(Facility::LOG_USER).unwrap();
    external_logger = syslog::tcp("127.0.0.1:9779",
                                      "localhost".to_string(),
                                      Facility::LOG_USER).unwrap();

    let sleep_time = time::Duration::from_millis(2000);
    loop {
        logger.send(Severity::LOG_ALERT, "test");
        external_logger.send(Severity::LOG_ALERT, "test");
        thread::sleep(sleep_time);
    }
}

fn handle_client(stream: TcpStream) {
    let mut buffer = [0; 4096];
    let x = stream.read(&mut buffer);
    local_logger.write(x);
    external_logger.write(x);
}

fn command_listener() {
    let listener = TcpListener::bind("127.0.0.1:9778").unwrap();
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                handle_client(stream);
            }
            Err(e) => { /* connection failed */ }
        }
    }
}

fn main() {

    let working_dir = "/tmp";
    let user_name = "smith";
    let group_name = "smith";

    syslog_test();

    let daemon = Daemonize::new()
        .pid_file("/home/smith/Dropbox/ellida/res/ellida.pid")
        .chown_pid_file(true)
        .working_directory(working_dir)
        .user(user_name)
        .group(group_name)
        .umask(0o777)
        .privileged_action(action_test);

    match daemon.start() {
        Ok(_) => info!("Success, daemonized"),
        Err(e) => error!("{}", e),
    }
}
