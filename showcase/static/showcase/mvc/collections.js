var AuthCollection = Backbone.Collection.extend({
    url: '/api/v1/AuthenticationResource',
    parse: function(data) {
        return data.queryset;
    }
});

var ConfirmationCollection = Backbone.Collection.extend({
    url: '/api/v1/ConfirmationResource',
    parse: function(data) {
        return data.queryset;
    }
});

var GenerateSalesCollection = Backbone.Collection.extend({
    url: '/api/v1/GenerationResource/'
});

var CurrencyCollection = Backbone.Collection.extend({
    url: '/api/v1/CurrencyResource',
    parse: function(data) {
        return data.queryset;
    }
});

var ProductCollection = Backbone.Collection.extend({
    url: '/api/v1/ProductResource',
    parse: function(data) {
        return data.queryset;
    }
});

var CustomUserCollection = Backbone.Collection.extend({
    url: '/api/v1/CustomUserResource',
    parse: function(data) {
        return data.queryset;
    }
});

var ReviewCollection = Backbone.Collection.extend({
    url: '/api/v1/ReviewResource',
    parse: function(response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

var IngredientCollection = Backbone.Collection.extend({
    url: '/api/v1/IngredientResource',
    parse: function(response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

var OrderCollection = Backbone.Collection.extend({
    url: '/api/v1/OrderResource',
    parse: function(response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

var OrderItemCollection = Backbone.Collection.extend({
    url: '/api/v1/OrderItemResource',

    parse: function(response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});