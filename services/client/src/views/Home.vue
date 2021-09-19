<template>
  <div class="home">
    <div class="container">
      <h1>Home page</h1>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import VueCookie from "vue-cookie";

Vue.use(VueCookie);

export default {
  name: "Home",
  beforeCreate() {
    var token = this.$cookie.get("access_token_cookie");
    console.log(token);
    // add to local storage
    localStorage.setItem("access_token", token); // token stores in cookies

    // update the store state token
    this.$store.commit("updateToken", token);
  },
};
</script>
