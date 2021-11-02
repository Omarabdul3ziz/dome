module main

import vweb
import json

['/tasks']
pub fn (mut app App) read_all() vweb.Result {
	tasks := app.read_all_tasks()

	return app.json({
		'tasks': tasks
	})
}

['/tasks/:id']
pub fn (mut app App) read_one(id int) vweb.Result {
	task := app.read_one_task(id)

	return app.json({
		'task': task
	})
}

['/tasks'; post]
fn (mut app App) add() vweb.Result {
	data := app.req.data
	task := json.decode(Task, data) or { return app.text('json decoding error') }
	app.create_task(task)
	return app.text('success')
}

['/tasks/:id'; delete]
fn (mut app App) delete(id int) vweb.Result {
	app.delete_task(id)
	return app.text('success')
}

['/tasks/:id'; put]
fn (mut app App) update(id int) vweb.Result {
	data := app.req.data
	task := json.decode(Task, data) or { return app.text('json decoding error') }
	app.update_task(id, task.text)
	return app.text('success')
}

['/tasks/:id/check'; put]
fn (mut app App) check(id int) vweb.Result {
	app.check_task(id)
	return app.text('success')
}
