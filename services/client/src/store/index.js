import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";
Vue.use(VueCookies);
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: localStorage.getItem("access_token") || null,
    // access_token_cookie: Vue.$cookies.get("access_token_cookie") || null,
    api_url: "http://127.0.0.1:8080",
  },
  mutations: {
    updateToken(state, token) {
      state.token = token;
      // state.access_token_cookie = token;
    },
    distroyToken(state) {
      state.token = null;
      // state.access_token_cookie = null;
    },
  },
  actions: {},
  modules: {},
  getters: {
    loggedIn(state) {
      return state.token != null;
    },
  },
});
