<template>
  <div></div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
export default {
  name: "Logout",
  data() {
    return {
      baseUrl: this.$store.state.api_url,
    };
  },
  created() {
    this.distroyToken();
  },
  methods: {
    distroyToken() {
      const path = this.baseUrl + "/auth/logout";

      axios.defaults.headers.common["Authorization"] =
        "Bearer " + this.$store.state.token;

      axios.get(path).then((response) => {
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
