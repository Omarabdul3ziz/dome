<template>
  <div id="app">
    <div id="nav">
      <div v-if="loggedIn">
        <router-link to="/todo">Home</router-link> |
        <router-link to="/logout">Logout</router-link>
      </div>
      <div v-else>
        <router-link to="/register">Register</router-link> |
        <router-link to="/login">Login</router-link> |
        <router-link to="/github">With GitHub</router-link>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",

  data() {
    return {
      loggedIn: false,
    };
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
