<template>

  <div>
    <br>
    <br>

    <input type="text" class="todo-input" placeholder="Add new task" v-model="newTodo" @keyup.enter="addTodo">
    <!-- List -->
        <div v-for="(todo, index) in todos" :key="todo.id" class="todo-item">
            
            <dir class="todo-item-left">
                <input type="checkbox" v-model="todo.status" @click="updateStatus(todo, index)">
                <div v-if="!todo.editing" @dblclick="editTodo(todo, index)" class="todo-item-label" :class="{ status : todo.status }">{{ 12 }}</div>
                <input v-else class="todo-item-edit" type="text" v-model="todo.title" @blur="doneEdit(todo, index)" @keyup.enter="doneEdit(todo, index)" @keyup.esc="doneEdit(todo)" v-focus>
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
          baseUrl: 'http://flask:5000/tasks',

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
        const path = this.baseUrl
        Vue.axios.get(path)
          .then((res) => {
            res.data["Tasks"].forEach((todo) => {
              this.todos.push({
                'title': todo.title,
                'status': todo.status,
                'due': todo.due,
                'editing': false
              })
            });
          })
      },

      addTodo() {

          if (this.newTodo.trim().length == 0){
              return
          }

          const path = this.baseUrl;
          var newEntry = {
            'title': this.newTodo,
            'status': false,
            'due': 0,
            'editing': false
          }
          Vue.axios.post(path, newEntry)
            .then(response => this.idForTodo = response.data.id)
            .then(this.todos.push(newEntry))
          this.newTodo=''
          this.idForTodo++
          
      },

      removeTodo(index) {
          this.todos.splice(index, 1)
          const path = this.baseUrl + "/" + index
          Vue.axios.delete(path)
      },

      editTodo(todo) {
          todo.editing = true
      },

      updateTodo(todo, index) {
          const path = this.baseUrl + "/" + index
          Vue.axios.put(path, {'title': todo.title})
      },

      doneEdit(todo, index) {
          this.updateTodo(todo, index);
          todo.editing = false
      }, 

      updateStatus(todo, index) {
          const path = this.baseUrl + "/" + index + "/check"
          Vue.axios.put(path, {'status': !todo.status}) // i think it takes the value before changing so i NOT it
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

  .status {
    text-decoration: line-through;
    color: grey;
  }
  
</style>
