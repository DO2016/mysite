
var AuthModel = Backbone.Model.extend({
    url: '/api/v1/AuthenticationResource/'
    , idAttribute: "username"
    , password: "password"
    , key: ""
});

var RegistrationModel = Backbone.Model.extend({
    url: '/api/v1/RegistrationResource/'
    , first_name: 'first_name'
    , last_name: 'last_name'
    , password: 'password'
    , email: 'email'    
});

var GenerateSalesModel = Backbone.Model.extend({
    url: '/api/v1/GenerationResource/'
});

var ProductModel = Backbone.Model.extend({
    urlRoot: '/api/v1/ProductResource/'
    , name: 'name'
    , description: 'description'
    , is_published: 'is_published'
    , date_published: 'date_published'
    , price: 'price'
    , currency: 'currency'
    , objects: 'objects'
    , currency: 'currency'
});

var AddProductModel = Backbone.Model.extend({
    url: '/api/v1/AddProductResource/'
    , name: 'name'
    , description: 'description'
    , is_published: 'is_published'
    , date_published: 'date_published'
    , price: 'price'
    , currency: 'currency'
    , objects: 'objects'
    , currency: 'currency'
});

var CurrencyModel = Backbone.Model.extend({
    url: '/api/v1/CurrencyResource/'
    , name: 'name'
    , char_code: 'char_code'
    , int_code: 'int_code'
    , usd_coeff: 'usd_coeff'
});

var CustomUserModel = Backbone.Model.extend({
    url: '/api/v1/CustomUserResource/'
    , timezone: 'timezone'
    , username: 'username'
    , email: 'email'
    , last_name: 'last_name'
});

var ConfirmationModel = Backbone.Model.extend({
    url: '/api/v1/ConfirmationResource/'
    , timezone: 'timezone'
    , username: 'username'
    , email: 'email'
    , last_name: 'last_name'
    , is_active: 'is_active'
    , api_key: 'api_key'
});


var ReviewModel = Backbone.Model.extend({
    url: '/api/v1/ReviewResource/'
    , content: 'content'
    , product: 'product'
    , author: 'author'
});

var IngredientModel = Backbone.Model.extend({
    url: '/api/v1/IngredientResource/'
    , price: 'price' 
    , name: 'name'
});

var OrderModel = Backbone.Model.extend({
    url: '/api/v1/OrderResource/'
    , id: 'id'
    , customer: 'customer'
});

var OrderItemModel = Backbone.Model.extend({
    url: '/api/v1/OrderItemResource/'
    , product: 'product'
    , order: 'order'
    , number: 'number'
});