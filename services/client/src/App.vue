<template>
  <div id="app">
    <div id="nav">
      <nav class="navbar navbar-dark bg-dark">
        <div class="navbar-collapse">
          <ul class="navbar-nav">
            <li>
              <router-link class="navbar-link" id="left" to="/"
                >Home</router-link
              >
            </li>
            <li v-if="loggedIn">
              <router-link class="navbar-link" id="left" to="/todo"
                >Todo</router-link
              >
            </li>
            <li v-if="!loggedIn">
              <router-link class="navbar-link" id="right" to="/register"
                >Register</router-link
              >
            </li>
            <li v-if="!loggedIn">
              <router-link class="navbar-link" id="right" to="/login"
                >Login</router-link
              >
            </li>
            <li v-if="!loggedIn">
              <router-link class="navbar-link" id="right" to="/github"
                >GitHub</router-link
              >
            </li>
            <li v-if="!loggedIn">
              <router-link class="navbar-link" id="right" to="/tribot"
                >3Bot</router-link
              >
            </li>
            <li v-if="loggedIn">
              <router-link class="navbar-link" id="right" to="/logout"
                >Logout</router-link
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

  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn;
    },
  },
};
</script>

<style lang="scss">
* {
  box-sizing: border-box;
}
.container {
  max-width: 600px;
  margin: 0 auto;
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

#nav {
  a {
    color: #ffffff;

    &.router-link-exact-active {
      color: #43aeec;
    }
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
}
</style>
