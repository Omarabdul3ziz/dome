import sqlite
import vweb
import json

struct Task { // Define the schema of your table
	id        int    [primary; sql: serial]
	text      string [nonull]
	completed bool // are zerod by default
	user      string = 'Anon'
}

struct App {
	vweb.Context
pub mut:
	db sqlite.DB
}

struct DataBase {
pub mut:
	db sqlite.DB
}

// Operation wrapper
fn draw() {
	sql db.db {
		create table Task
	}
}

fn erase() {
	sql db.db {
		drop table Task
	}
}

fn create(t Task) {
	sql db.db {
		insert t into Task
	}
}

fn (mut db DataBase) read_task(id int) Task {
	return sql db.db {
		select from Task where id == id
	}
}

fn read_tasks(user string) []Task {
	return sql db.db {
		select from Task where user == user
	}
}

fn update(id int, new_text string) {
	sql db.db {
		update Task set text = new_text where id == id
	}
}

fn delete(id int) {
	sql db.db {
		delete from Task where id == id
	}
}

fn check(id int) {
	task := sql db.db {
		select from Task where id == id
	}

	status := task.completed
	new_status := !status

	sql db.db {
		update Task set completed = new_status where id == id
	}
}

// handlers
['/tasks']
fn (mut app App) get_task() vweb.Result {
	data := app.db.read_task(2)
	return app.json(json.encode(data))
}

fn main() {
	db := DataBase{
		db: sqlite.connect('foo.db') ?
	}
	vweb.run(&App{}, 5000)
}
