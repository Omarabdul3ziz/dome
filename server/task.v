module main

struct Task {
	id        int    [primary; sql: serial]
	text      string [nonull]
	completed bool
	user      string
}

pub fn (app &App) read_all_tasks() []Task {
	return sql app.db {
		select from Task
	}
}

pub fn (app &App) read_one_task(id int) Task {
	return sql app.db {
		select from Task where id == id
	}
}

pub fn (app &App) create_task(task Task) {
	sql app.db {
		insert task into Task
	}
}

pub fn (app &App) delete_task(id int) {
	sql app.db {
		delete from Task where id == id
	}
}

pub fn (app &App) update_task(id int, new_content string) {
	sql app.db {
		update Task set text = new_content where id == id
	}
}

pub fn (app &App) check_task(id int) {
	task := sql app.db {
		select from Task where id == id
	}
	new_status := !task.completed
	sql app.db {
		update Task set completed = new_status where id == id
	}
}
