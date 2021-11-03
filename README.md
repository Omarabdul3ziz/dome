### Usage

According to comment in this [question](https://stackoverflow.com/questions/61541970/vue-axios-api-call-doesnt-work-when-using-docker-networking-hostname), there is no issue.

`curl http://api:5000/tasks` works, because it runs from container sh.
`axios.get("http://api:5000/tasks")` does not, because it runs from browser.
