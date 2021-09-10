<template>
  <div class="login">
    <form>
      <input
        type="text"
        class="form-control"
        placeholder="Enter email"
        v-model="username"
      />
      <input
        type="password"
        class="form-control"
        placeholder="Password"
        v-model="password"
      />
      <button type="submit" class="btn btn-primary" @click="submit">
        Login
      </button>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src

import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";


Vue.use(VueAxios, axios);
export default {
  name: "Login",
  data() {
    return {
      // loggedIn: true,
      username: "",
      password: "",
      baseUrl: process.env.VUE_APP_ROOT_API,
    };
  },
  methods: {
    submit() {
      const path = this.baseUrl + "/auth/login";
      const auth = { username: this.username, password: this.password };
      Vue.axios.post(path, auth);
    },
  },
};
</script>
