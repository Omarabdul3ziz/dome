<template>

  <div>
    <input type="text" class="todo-input" placeholder="Add new task" v-model="newTodo" @keyup.enter="addTodo">
    
    <!-- List -->
        <div v-for="(todo, index) in todos" :key="todo.id" class="todo-item">
            
            <dir class="todo-item-left">
                <input type="checkbox" v-model="todo.done">
                <div v-if="!todo.editing" @dblclick="editTodo(todo)" class="todo-item-label" :class="{ done : todo.done }">{{ todo.content }}</div>
                <input v-else class="todo-item-edit" type="text" v-model="todo.content" @blur="doneEdit(todo)" @keyup.enter="doneEdit(todo)" @keyup.esc="doneEdit(todo)" v-focus>
            </dir>

            <div class="remove-item" @click="removeTodo(index)">
                        &times;
            </div>
            
        </div>
    <!-- End list -->


  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

export default {
  name: 'todo-list',
  data() {
      return {
          newTodo: '',
          idForTodo: 3,
          baseUrl: 'http://192.168.1.111:5000',

          todos: []}
  },

  directives: {
    focus: {
      inserted: function (el) {
        el.focus()
      }
    }
  },

  created() {
    this.getTodos();
  },

  methods: {

      getTodos(){
        const path = this.baseUrl + "/tasks"
        Vue.axios.get(path)
          .then((res) => {
            res.data["Tasks"].forEach((todo) => {
              this.todos.push({
                'content': todo.content,
                'done': todo.done,
                'editing': false
              })
            });
          })
      },

      addTodo() {

          if (this.newTodo.trim().length == 0){
              return
          }

          // this.todos.push({
          //     id: this.idForTodo,
          //     title: this.newTodo,
          //     done: false
          // })

          const path = this.baseUrl + "/add";
          var newEntry = {
            'content': this.newTodo,
            'done': false,
            'editing': false
          }
          Vue.axios.post(path, newEntry)
            .then(response => this.idForTodo = response.data.id)
            .then(location.reload())
          this.newTodo=''
          this.idForTodo++
      },

      removeTodo(index) {
          this.todos.splice(index, 1)
      },

      editTodo(todo) {
          todo.editing = true
      },

      doneEdit(todo) {
          todo.editing = false
      }
  }
}
</script>

<style>
  .todo-input {
    width: 100%;
    padding: 10px 18px;
    font-size: 18px;
    margin-bottom: 16px;
  }

  .todo-item {
    margin-bottom: 12px;
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
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
  }

  .done {
    text-decoration: line-through;
    color: grey;
  }
  
</style>
