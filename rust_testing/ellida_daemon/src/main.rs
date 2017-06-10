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

fn action_test() {
    let mut lg = syslog::unix(Facility::LOG_USER);

    match syslog::unix(Facility::LOG_USER) {
        Err(_)  => {},
        Ok(writer)   => {
            lg = writer;
        }
    }

    let sleep_time = time::Duration::from_millis(2000);
    while true {
        lg.send(Severity::LOG_ALERT, "test");
        thread::sleep(sleep_time);
    }
}

fn main() {

    let working_dir = "/tmp";
    let user_name = "smith";
    let group_name = "smith";

    syslog_test();

    let daemon = Daemonize::new()
        .pid_file("/tmp/ellida.pid")
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
