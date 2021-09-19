<template>
  <div>
    <br />
    <div>
      <button type="submit" class="btn btn-primary" @click="start">
        Login with 3bot connect
      </button>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
export default {
  name: "Tribot",
  data() {
    return {
      baseUrl: this.$store.state.api_url,
    };
  },

  methods: {
    start() {
      const path = "https://127.0.0.1:5000" + "/3bot/login";
      window.location.href = path;
    },

    login() {
      const path = this.baseUrl + "/3bot/login";
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
