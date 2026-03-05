package handlers

import (
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"github.com/techshop/product-service/internal/models"
	"github.com/techshop/product-service/internal/repository"
)

type ProductHandler struct {
	repo   repository.ProductRepository
	logger *logrus.Logger
}

func NewProductHandler(repo repository.ProductRepository, logger *logrus.Logger) *ProductHandler {
	return &ProductHandler{repo: repo, logger: logger}
}

func errorResponse(c *gin.Context, status int, code, message string) {
	c.JSON(status, gin.H{
		"error": gin.H{"code": code, "message": message, "status": status},
	})
}

func (h *ProductHandler) HealthCheck(c *gin.Context) {
	c.JSON(200, gin.H{"status": "ok", "service": "product-service"})
}

func (h *ProductHandler) CreateProduct(c *gin.Context) {
	var input struct {
		Name        string  `json:"name"        binding:"required"`
		Category    string  `json:"category"    binding:"required"`
		Price       float64 `json:"price"       binding:"required,gt=0"`
		Stock       int     `json:"stock"       binding:"gte=0"`
		Description string  `json:"description"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		errorResponse(c, 400, "VALIDATION_ERROR", err.Error())
		return
	}

	product, err := h.repo.CreateProduct(c.Request.Context(), &models.Product{
		Name:        input.Name,
		Category:    input.Category,
		Price:       input.Price,
		Stock:       input.Stock,
		Description: input.Description,
	})
	if err != nil {
		errorResponse(c, 500, "INTERNAL_ERROR", err.Error())
		return
	}
	c.JSON(201, gin.H{"data": product})
}

func (h *ProductHandler) GetProduct(c *gin.Context) {
	id := c.Param("id")
	product, err := h.repo.GetProduct(c.Request.Context(), id)
	if err != nil {
		errorResponse(c, 404, "PRODUCT_NOT_FOUND", "Product not found")
		return
	}
	c.JSON(200, gin.H{"data": product})
}

func (h *ProductHandler) ListProducts(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "20"))

	products, err := h.repo.ListProducts(c.Request.Context(), page, limit)
	if err != nil {
		errorResponse(c, 500, "INTERNAL_ERROR", err.Error())
		return
	}
	c.JSON(200, gin.H{"data": products, "meta": gin.H{"page": page, "limit": limit}})
}

func (h *ProductHandler) UpdateProduct(c *gin.Context) {
	id := c.Param("id")
	var input models.Product

	if err := c.ShouldBindJSON(&input); err != nil {
		errorResponse(c, 400, "VALIDATION_ERROR", err.Error())
		return
	}

	product, err := h.repo.UpdateProduct(c.Request.Context(), id, &input)
	if err != nil {
		errorResponse(c, 500, "INTERNAL_ERROR", err.Error())
		return
	}
	c.JSON(200, gin.H{"data": product})
}

func (h *ProductHandler) DeleteProduct(c *gin.Context) {
	id := c.Param("id")
	if err := h.repo.DeleteProduct(c.Request.Context(), id); err != nil {
		errorResponse(c, 500, "INTERNAL_ERROR", err.Error())
		return
	}
	c.JSON(200, gin.H{"data": gin.H{"message": "Product deleted"}})
}
