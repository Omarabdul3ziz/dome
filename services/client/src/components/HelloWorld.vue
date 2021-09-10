<template>
  <div class="hello">
    <div class="container form">
      <form @submit="login()">
        <div>
          <input type="string" placeholder="Username" v-model="username" />
        </div>
        <div>
          <input type="password" placeholder="Password" v-model="password" />
        </div>
        <div v-if="error">
          {{ error }}
        </div>
        <div v-if="success" id="success">Logged in Successfully</div>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);

export default {
  name: "HelloWorld",
  data() {
    return {
      username: "",
      password: "",
      error: null,
      success: false,
    };
  },
  methods: {
    login: function () {
      const auth = { username: this.username, password: this.password };
      // Correct username is 'foo' and password is 'bar'
      const url = "http://127.0.0.1:5000/login";
      this.success = false;
      this.error = null;

      try {
        Vue.axios.get(url, { auth }).then((res) => res.data);
        this.success = true;
      } catch (err) {
        this.error = err.message;
      }
    },
    loginUser() {
      Vue.axios
        .get(
          "http://127.0.0.1:5000/login",
          {},
          {
            auth: {
              username: this.username,
              password: this.password,
            },
          }
        )
        .then((res) => {
          console.log(res.data);
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
