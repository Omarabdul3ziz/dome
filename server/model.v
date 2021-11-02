// Grab it
import sqlite

// Define the schema of your table
struct Task {
	id        int    [primary; sql: serial]
	text      string [nonull]
	completed bool // are zerod by default
	user      string = 'Anon'
}

// constants are global and reachable any where
const (
	db = sqlite.connect('foo.db') ?
)

// Operation wrapper
fn draw() {
	sql db {
		create table Task
	}
}

fn erase() {
	sql db {
		drop table Task
	}
}

fn create(t Task) {
	sql db {
		insert t into Task
	}
}

fn read_task(id int) Task {
	return sql db {
		select from Task where id == id
	}
}

fn read_tasks(user string) []Task {
	return sql db {
		select from Task where user == user
	}
}

fn update(id int, new_text string) {
	sql db {
		update Task set text = new_text where id == id
	}
}

fn delete(id int) {
	sql db {
		delete from Task where id == id
	}
}

fn check(id int) {
	task := sql db {
		select from Task where id == id
	}

	status := task.completed
	new_status := !status

	sql db {
		update Task set completed = new_status where id == id
	}
}
