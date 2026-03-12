package models

import (
	"time"

	"go.mongodb.org/mongo-driver/v2/bson"
)

type Product struct {
	ID          bson.ObjectID `bson:"_id,omitempty" json:"id"`
	Name        string        `bson:"name"        json:"name"`
	Category    string        `bson:"category"    json:"category"`
	Price       float64       `bson:"price"       json:"price"`
	Stock       int           `bson:"stock"       json:"stock"`
	Description string        `bson:"description" json:"description"`
	CreatedAt   time.Time     `bson:"created_at"  json:"created_at"`
	UpdatedAt   time.Time     `bson:"updated_at"  json:"updated_at"`
}

type Category struct {
	ID   bson.ObjectID `bson:"_id,omitempty" json:"id"`
	Name string        `bson:"name" json:"name"`
	Slug string        `bson:"slug" json:"slug"`
}
