package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Task struct {
	ID        primitive.ObjectID `bson:"_id"`
	Text      string             `bson:"text"`
	Completed bool               `bson:"completed"`
	User      string             `bson:"user"`
}

var collection *mongo.Collection
var ctx = context.TODO()

func initDb() {
	const uri = "mongodb://localhost:27017"

	opt := options.Client().ApplyURI(uri)
	client, err := mongo.Connect(ctx, opt)
	alarm(err)

	collection = client.Database("domeAPI").Collection("tasks")
}

func handlers() {
	router := mux.NewRouter()

	router.HandleFunc("/tasks", getTasks).Methods("GET")
	router.HandleFunc("/tasks", addTask).Methods("POST")
	router.HandleFunc("/tasks/{id}", getTask).Methods("GET")
	router.HandleFunc("/tasks/{id}", updateTask).Methods("PUT")
	router.HandleFunc("/tasks/{id}", deleteTask).Methods("DELETE")
	router.HandleFunc("/tasks/{id}/check", checkTask).Methods("PUT")

	log.Fatal(http.ListenAndServe(":5000", router))
}

// APIs
func getTasks(res http.ResponseWriter, req *http.Request) {

	filter := bson.D{{}}

	var tasks []Task

	cur, err := collection.Find(ctx, filter)
	alarm(err)

	for cur.Next(ctx) {
		var task Task
		cur.Decode(&task) // decode the current document itself
		tasks = append(tasks, task)
	}

	payload := map[string][]Task{"tasks": tasks}

	// respond
	setHeader(&res, 200)
	json.NewEncoder(res).Encode(payload) // write response message

}

func addTask(res http.ResponseWriter, req *http.Request) {

	// task schema with default values
	id := primitive.NewObjectID()
	text := "Empty task"
	completed := false
	user := "Current user"

	task := Task{
		ID:        id,
		Text:      text,
		Completed: completed,
		User:      user,
	}

	// get data from body * comming overwrite dafault values *
	err := json.NewDecoder(req.Body).Decode(&task)
	alarm(err)

	// insert the task
	_, err = collection.InsertOne(ctx, &task)
	alarm(err)

	payload := map[string]Task{"task": task}

	// respond

	setHeader(&res, 201)
	json.NewEncoder(res).Encode(payload)

}

func getTask(res http.ResponseWriter, req *http.Request) {

	// get id from link as object ID
	params := mux.Vars(req)
	id := params["id"]
	oid, _ := primitive.ObjectIDFromHex(id)

	filter := bson.D{primitive.E{Key: "_id", Value: oid}}

	var task Task
	err := collection.FindOne(ctx, filter).Decode(&task)
	alarm(err)

	if isTask(oid) {
		payload := map[string]Task{"task": task}

		setHeader(&res, 200)
		json.NewEncoder(res).Encode(payload)

	} else {
		setHeader(&res, 404)

	}
}

func updateTask(res http.ResponseWriter, req *http.Request) {

	// get content from request and store in blank task schema
	var newTask Task
	err := json.NewDecoder(req.Body).Decode(&newTask)
	alarm(err)

	// find the requested task
	params := mux.Vars(req)
	id := params["id"]
	oid, _ := primitive.ObjectIDFromHex(id)

	filter := bson.D{primitive.E{Key: "_id", Value: oid}}

	update := bson.D{primitive.E{Key: "$set", Value: bson.D{
		primitive.E{Key: "text", Value: newTask.Text},
	}}}

	if isTask(oid) {
		collection.FindOneAndUpdate(ctx, filter, update)

		setHeader(&res, 200)
		json.NewEncoder(res).Encode("Task updated.")

	} else {
		setHeader(&res, 404)

	}

}

func deleteTask(res http.ResponseWriter, req *http.Request) {
	params := mux.Vars(req)
	id := params["id"]
	oid, _ := primitive.ObjectIDFromHex(id)

	filter := bson.D{primitive.E{Key: "_id", Value: oid}}

	if isTask(oid) {

		collection.DeleteOne(ctx, filter)

		setHeader(&res, 200)
		json.NewEncoder(res).Encode("Task deleted.")

	} else {
		setHeader(&res, 404)

	}
}

func checkTask(res http.ResponseWriter, req *http.Request) {

	params := mux.Vars(req)
	id := params["id"]
	oid, _ := primitive.ObjectIDFromHex(id)

	filter := bson.D{primitive.E{Key: "_id", Value: oid}}

	// get the task to inverse the status
	var task Task
	collection.FindOne(ctx, filter).Decode(&task)

	// the update operation
	update := bson.D{primitive.E{Key: "$set", Value: bson.D{
		primitive.E{Key: "completed", Value: !task.Completed},
	}}}

	if isTask(oid) {

		collection.FindOneAndUpdate(ctx, filter, update)

		setHeader(&res, 200)
		json.NewEncoder(res).Encode("Task checked.")

	} else {
		setHeader(&res, 404)

	}
}

// helper functions
func alarm(err error) {
	if err != nil {
		fmt.Println(err)
	}
}

func isTask(oid primitive.ObjectID) bool {
	filter := bson.D{primitive.E{Key: "_id", Value: oid}}

	var task Task
	err := collection.FindOne(ctx, filter).Decode(&task)

	if err == nil {
		return true
	} else {
		return false
	}

}

func setHeader(res *http.ResponseWriter, statusCode int) {
	(*res).Header().Set("Content-Type", "application/json")                                                    // set header to accept json
	(*res).Header().Set("Access-Control-Allow-Origin", "*")                                                    // allow cors
	(*res).Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")                     // allow cors methods
	(*res).Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Authorization") // allow auth
	(*res).WriteHeader(statusCode)                                                                             // return status code
}

func main() {
	initDb()
	handlers()
}
