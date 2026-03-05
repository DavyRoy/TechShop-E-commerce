package proxy

import (
	"net/http/httputil"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"
)

type Proxy struct {
	productProxy *httputil.ReverseProxy
	orderProxy   *httputil.ReverseProxy
	userProxy    *httputil.ReverseProxy
}

func New(productURL, orderURL, userURL string) *Proxy {
	return &Proxy{
		productProxy: newProxy(productURL),
		orderProxy:   newProxy(orderURL),
		userProxy:    newProxy(userURL),
	}
}

func newProxy(target string) *httputil.ReverseProxy {
	url, _ := url.Parse(target)
	return httputil.NewSingleHostReverseProxy(url)
}

func (p *Proxy) ProductService(c *gin.Context) {
	c.Request.URL.Path = strings.TrimPrefix(c.Request.URL.Path, "/api")
	p.productProxy.ServeHTTP(c.Writer, c.Request)
}

func (p *Proxy) OrderService(c *gin.Context) {
	c.Request.URL.Path = strings.TrimPrefix(c.Request.URL.Path, "/api")
	p.orderProxy.ServeHTTP(c.Writer, c.Request)
}

func (p *Proxy) UserService(c *gin.Context) {
	c.Request.URL.Path = strings.TrimPrefix(c.Request.URL.Path, "/api")
	p.userProxy.ServeHTTP(c.Writer, c.Request)
}
