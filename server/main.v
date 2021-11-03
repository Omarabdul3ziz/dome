module main

import vweb
import sqlite

struct App {
	vweb.Context
pub mut:
	db sqlite.DB
}

fn init_table(app &App) {
	sql app.db {
		create table Task
	}
}

fn main() {
	app := App{
		db: sqlite.connect('/database/tasks.db') ?
	}

	init_table(app)

	vweb.run(app, 5000)
}
