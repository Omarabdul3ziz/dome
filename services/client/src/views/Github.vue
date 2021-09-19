<template>
  <div>
    <div>
      <button type="submit" class="btn btn-primary">
        <a href="https://127.0.0.1:5000/auth/github">Login with GitHub</a>
      </button>
    </div>
    <br />
    <!-- <div>
      <button type="submit" class="btn btn-primary" @click="githubLogin">
        Login with GitHub
      </button>
    </div> -->
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
export default {
  name: "Github",
  // data() {
  //   return {
  //     baseUrl: this.$store.state.api_url,
  //   };
  // },
  // created() {
  //   // this.githubLogin();
  // },
  // methods: {
  //   fetchTocken() {
  //     const path = this.baseUrl + "/auth/github";
  //     fetch(path).then((response) => console.log(response));
  //   },

  //   githubLogin() {
  //     const path = this.baseUrl + "/auth/github";
  //     Vue.axios.get(path).then((response) => {
  //       const token = response.data.access_token;
  //       console.log(token);

  //       // add to local storage
  //       localStorage.setItem("access_token", token);

  //       // update the store state token
  //       this.$store.commit("updateToken", token);

  //       // redirect for next route
  //       this.$router.push({ name: "Todo" });
  //     });
  //   },
  // },
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: white;
}
a:hover {
  text-decoration: none;
  color: white;
}
</style>
