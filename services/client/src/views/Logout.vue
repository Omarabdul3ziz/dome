<template>
  <div></div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import VueCookie from "vue-cookie";

Vue.use(VueCookie);
Vue.use(VueAxios, axios);
export default {
  name: "Logout",
  data() {
    return {
      baseUrl: this.$store.state.api_url,
    };
  },
  created() {
    this.logout();
  },
  methods: {
    logout() {
      // remove token from cookie
      this.$cookie.delete("access_token_cookie");

      // remove token from localStorage
      localStorage.clear(); // not the best practice but workes for now

      // remove the token from store state
      this.$store.commit("distroyToken");

      // redirect
      this.$router.push({ name: "Login" });
    },

    distroyToken() {
      const path = this.baseUrl + "/auth/logout";

      Vue.axios.defaults.headers.common["Authorization"] =
        "Bearer " + this.$store.state.token;

      Vue.axios.get(path).then((response) => {
        // remove the cookie from server
        console.log(response.data.message);

        // remove token from localStorage
        // localStorage.removeItem("access-token");
        localStorage.clear(); // not the best practice but workes for now

        // remove the token from store state
        this.$store.commit("distroyToken");

        // redirect
        this.$router.push({ name: "Login" });
      });
    },
  },
};
</script>
