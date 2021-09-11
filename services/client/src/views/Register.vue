<template>
  <div class="login container">
    <form @submit.prevent="submit">
      <div>
        <input
          type="text"
          class="form-control"
          placeholder="Username"
          v-model="username"
          required
        />
      </div>
      <div>
        <input
          type="password"
          class="form-control"
          placeholder="Password"
          v-model="password"
          required
        />
      </div>
      <div>
        <button type="submit" class="btn btn-primary">Login</button>
      </div>
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
  name: "Register",
  data() {
    return {
      username: "",
      password: "",
      baseUrl: this.$store.state.api_url,
    };
  },
  methods: {
    submit() {
      const path = this.baseUrl + "/auth/register";
      const auth = { username: this.username, password: this.password };
      Vue.axios.post(path, auth).then((response) => {
        const token = response.data.access_token;
        localStorage.setItem("access_token", token);
        this.$store.commit("updateToken", token);
        console.log(token);
        this.$router.push({ name: "Todo" });
      });
    },
  },
};
</script>

<style scoped>
.login {
  width: 50%;
}
.form-control {
  margin: 10px;
}
</style>
