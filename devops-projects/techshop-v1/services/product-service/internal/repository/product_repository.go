package repository

import (
	"context"
	"time"

	"github.com/techshop/product-service/internal/models"
	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type ProductRepository interface {
	CreateProduct(ctx context.Context, product *models.Product) (*models.Product, error)
	GetProduct(ctx context.Context, id string) (*models.Product, error)
	ListProducts(ctx context.Context, page, limit int) ([]*models.Product, error)
	UpdateProduct(ctx context.Context, id string, product *models.Product) (*models.Product, error)
	DeleteProduct(ctx context.Context, id string) error
}

type productRepository struct {
	collection *mongo.Collection
}

func NewProductRepository(db *mongo.Database) ProductRepository {

	collection := db.Collection("products")

	// Create indexes
	indexes := []mongo.IndexModel{
		{
			Keys: bson.D{{Key: "name", Value: 1}},
		},
		{
			Keys: bson.D{{Key: "category", Value: 1}},
		},
		{
			Keys: bson.D{{Key: "price", Value: 1}},
		},
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	collection.Indexes().CreateMany(ctx, indexes)

	return &productRepository{
		collection: collection,
	}
}

func (r *productRepository) CreateProduct(ctx context.Context, product *models.Product) (*models.Product, error) {

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	product.ID = bson.NewObjectID()
	product.CreatedAt = time.Now()
	product.UpdatedAt = time.Now()

	_, err := r.collection.InsertOne(ctx, product)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (r *productRepository) GetProduct(ctx context.Context, id string) (*models.Product, error) {

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	objectID, err := bson.ObjectIDFromHex(id)
	if err != nil {
		return nil, err
	}

	var product models.Product

	err = r.collection.FindOne(ctx, bson.M{"_id": objectID}).Decode(&product)
	if err != nil {
		return nil, err
	}

	return &product, nil
}

func (r *productRepository) ListProducts(ctx context.Context, page, limit int) ([]*models.Product, error) {

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	if page <= 0 {
		page = 1
	}

	if limit <= 0 {
		limit = 10
	}

	skip := (page - 1) * limit

	opts := options.Find().
		SetSkip(int64(skip)).
		SetLimit(int64(limit)).
		SetSort(bson.D{{Key: "created_at", Value: -1}})

	cursor, err := r.collection.Find(ctx, bson.M{}, opts)
	if err != nil {
		return nil, err
	}

	defer cursor.Close(ctx)

	var products []*models.Product

	for cursor.Next(ctx) {

		var product models.Product

		if err := cursor.Decode(&product); err != nil {
			return nil, err
		}

		products = append(products, &product)
	}

	if err := cursor.Err(); err != nil {
		return nil, err
	}

	return products, nil
}

func (r *productRepository) UpdateProduct(ctx context.Context, id string, product *models.Product) (*models.Product, error) {

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	objectID, err := bson.ObjectIDFromHex(id)
	if err != nil {
		return nil, err
	}

	product.UpdatedAt = time.Now()

	update := bson.M{
		"$set": bson.M{
			"name":        product.Name,
			"category":    product.Category,
			"price":       product.Price,
			"stock":       product.Stock,
			"description": product.Description,
			"updated_at":  product.UpdatedAt,
		},
	}

	_, err = r.collection.UpdateOne(
		ctx,
		bson.M{"_id": objectID},
		update,
	)

	if err != nil {
		return nil, err
	}

	return r.GetProduct(ctx, id)
}

func (r *productRepository) DeleteProduct(ctx context.Context, id string) error {

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	objectID, err := bson.ObjectIDFromHex(id)
	if err != nil {
		return err
	}

	_, err = r.collection.DeleteOne(
		ctx,
		bson.M{"_id": objectID},
	)

	return err
}
