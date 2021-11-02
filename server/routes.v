import vweb
// import json

struct App {
	vweb.Context
}

['/tasks']
fn (mut app App) get_all() vweb.Result {
	data := read_tasks('Anon')
	println(data)
	return app.json({
		'hi': 'hi'
	})
}

fn main() {
	vweb.run(&App{}, 5000)
}
