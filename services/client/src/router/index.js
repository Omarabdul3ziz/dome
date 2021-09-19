import Vue from "vue";
import VueRouter from "vue-router";

import Home from "@/views/Home.vue";
import Todo from "@/views/Todo.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Github from "@/views/Github.vue";
import Tribot from "@/views/Tribot.vue";
import Logout from "@/views/Logout.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },

  {
    path: "/todo",
    name: "Todo",
    component: Todo,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: "/github",
    name: "Github",
    component: Github,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: "/tribot",
    name: "Tribot",
    component: Tribot,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
