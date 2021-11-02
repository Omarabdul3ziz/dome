<template>
  <div id="app">
    <div id="nav">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <ul class="navbar-nav">
            <li>
              <router-link class="navbar-link" id="left" to="/"
                >Home</router-link
              >
            </li>
            <li>
              <router-link class="navbar-link" id="left" to="/todo"
                >Todo</router-link
              >
            </li>
          </ul>
        </div>
      </nav>
    </div>

    <br />
    <br />
    <br />
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
* {
  box-sizing: border-box;
}

#left {
  float: left;
  margin-left: 10px;
}
#right {
  float: right;
  margin-right: 10px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

li {
  text-decoration: none;
  display: inline;
  margin: 10px;
}
ul {
  display: inline;
}

.navbar-link {
  text-decoration: none;
}
</style>
