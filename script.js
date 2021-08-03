const app = new Vue({
    el: '#app',

    data: {
        tasks: [],
    },

    mounted() {
        fetch("http://rest.learncode.academy/api/vue-5/tasks")
        .then(response => response.json())
        .then((data) => {
            this.tasks = data;
        }
    },

    template: `
        <div> 
            <h3 v-for="person in persons"> 
                <h2> {{ show(person) }}</h2>
                <input v-model="person.name"/>
                <button v-on:click="incrementAge(person)">+</button>
            </h3>
        </div>
    `
})