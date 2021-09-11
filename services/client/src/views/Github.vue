<template>
  <div></div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
export default {
  name: "Github",
  data() {
    return {
      baseUrl: this.$store.state.api_url,
    };
  },
  created() {
    this.githubLogin();
  },
  methods: {
    githubLogin() {
      const path = this.baseUrl + "/auth/github";
      Vue.axios.get(path).then((response) => {
        const token = response.data.access_token;
        console.log(token);

        // add to local storage
        localStorage.setItem("access_token", token);

        // update the store state token
        this.$store.commit("updateToken", token);

        // redirect for next route
        this.$router.push({ name: "Todo" });
      });
    },
  },
};
</script>
