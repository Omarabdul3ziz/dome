<template>
  <div class="todo">
    <div class="container">
      <input
        type="text"
        class="todo-input"
        placeholder="Add new task"
        v-model="newTodo"
        @keyup.enter="addTodo"
      />

      <!-- List -->
      <div class="container">
        <div class="todo-list">
          <div v-for="(todo, index) in todos" :key="todo.id" class="todo-item">
            <div class="todo-item-left">
              <input
                type="checkbox"
                v-model="todo.complete"
                @click="updateStatus(todo, index)"
              />
              <div
                v-if="!todo.editing"
                @dblclick="editTodo(todo)"
                class="todo-item-label"
                :class="{ complete: todo.complete }"
              >
                {{ todo.text }}
              </div>
              <input
                v-else
                class="todo-item-edit"
                type="text"
                v-model="todo.text"
                @blur="doneEdit(todo, index)"
                @keyup.enter="doneEdit(todo, index)"
                @keyup.esc="doneEdit(todo)"
                v-focus
              />
            </div>

            <div class="remove-item" @click="removeTodo(index)">&times;</div>
          </div>
        </div>
      </div>

      <!-- End list -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Todo",
  data() {
    return {
      newTodo: "",
      idForTodo: "",
      todos: [],
      baseUrl: "http://localhost:8080/tasks",
    };
  },

  directives: {
    focus: {
      inserted: function (el) {
        el.focus();
      },
    },
  },

  created() {
    this.getTodos();
  },

  methods: {
    getTodos() {
      const path = this.baseUrl;
      axios.get(path).then((res) => {
        res.data["tasks"].forEach((todo) => {
          this.todos.push({
            id: todo.ID,
            text: todo.Text,
            complete: todo.Completed,
            author: todo.User,
            editing: false,
          });
        });
      });
    },

    addTodo() {
      if (this.newTodo.trim().length == 0) {
        return;
      }

      const path = this.baseUrl;
      var newEntry = {
        text: this.newTodo,
        // complete: false,
        // editing: false,
      };

      axios
        .post(path, newEntry)
        // .then((response) => (this.idForTodo = response.data.id))
        .then(this.todos.push(newEntry));
      this.newTodo = "";
    },

    removeTodo(index) {
      var task_id = this.todos[index]["id"];
      this.todos.splice(index, 1);
      const path = this.baseUrl + "/" + task_id;
      axios.delete(path);
    },

    editTodo(todo) {
      todo.editing = true;
    },

    updateTodo(todo, index) {
      var task_id = this.todos[index]["id"];
      const path = this.baseUrl + "/" + task_id;
      axios.put(path, { text: todo.text });
    },

    doneEdit(todo, index) {
      this.updateTodo(todo, index);
      todo.editing = false;
    },

    updateStatus(todo, index) {
      var task_id = this.todos[index]["id"];
      const path = this.baseUrl + "/" + task_id + "/check";
      axios.put(path);
    },
  },
};
</script>

<style>
.todo-list {
  text-align: center;
}
.todo-input {
  width: 60%;
  padding: 10px 18px;
  font-size: 18px;
  margin-bottom: 16px;
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation-duration: 0.3s;
}

.remove-item {
  cursor: pointer;
  margin-left: 14px;
}

.todo-item-left {
  display: flex;
  align-items: center;
}

.todo-item-label {
  padding: 10px;
  border: 1px solid white;
  margin-left: 12px;
}

.todo-item-edit {
  font-size: 24px;
  color: #2c3e50;
  margin-left: 12px;
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
}

.complete {
  text-decoration: line-through;
  color: grey;
}
</style>
