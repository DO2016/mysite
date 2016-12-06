window.AppRouter = Backbone.Router.extend({
    initialize: function(){
        this.loginView = new LoginView({});
        this.productListView = new ProductListView({});
        this.headerView = new HeaderView({});
        this.generateView = new GenerateSalesView({});
        this.signupView = new SignupView({});
        this.detailsView = new DetailsView({});
        this.breadcrumbs = [];
    },

    routes: {
        "" : "index",
        "login" : "login",
        "products" : "products",
        "details/:id" : "productDetails",
        "register" : "register",
        "confirm/:apikey/:username/": "confirm",
        "generate": "generate",
        "signup": "signup"
    },

    index: function() {
        this.breadcrumbs = [ "<a href=\"#\">Bristol</a>" ];
        this.breadcrumbs.push("<a href=\"#products\"> <span class=\"glyphicon glyphicon-th\"></span> Products </a>");
        this.headerView.render(this.breadcrumbs);
        this.show(this.productListView);
    },

    products: function() {
        this.breadcrumbs = [ "<a href=\"#\">Bristol</a>" ];
        this.breadcrumbs.push("<a href=\"#products\">Products </a>");
        this.headerView.render(this.breadcrumbs);
        this.show(this.productListView);
    },

    login: function() {
        this.breadcrumbs = [];
        this.breadcrumbs.push("<a href=\"#login\">Log In </a>");
        this.headerView.render(this.breadcrumbs);
        this.show(this.loginView);
    },

    register: function() {
        this.headerView.render();
        this.show(this.headerView);
    },

    signup: function() {
        this.breadcrumbs = [ "<a href=\"#\">Bristol</a>" ];
        this.breadcrumbs.push("<a href=\"#signup\"> Register new account </a>");
        this.headerView.render(this.breadcrumbs);
        this.show(this.signupView);
    },

    productDetails: function(id) {
        this.breadcrumbs = [ "<a href=\"#\">Bristol</a>" ];
        this.breadcrumbs.push("<a href=\"#products\">Products </a>");
        this.detailsView.render(id, this.breadcrumbs, this.headerView);
    },

    confirm: function(apikey, username) {
        this.model = new ConfirmationCollection({});
        self = this;
        self.apikey = apikey;
        self.username = username;

        self.model.fetch({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('username', self.username);
                xhr.setRequestHeader('apikey', self.apikey);
            },
            error: function (collection, response) {
                console.log("Error fetching!");
            },
            success: function (collection, response, options) {
                console.log("Successful activation!");
                window.router.navigate("", true);
            }
        });
    },

    generate: function() {
        if (!$.cookie('api_key')) { 
            window.router.navigate("", true); // If not auth.
        } 
        else {
            this.show(this.generateView);
        }
    },

    show: function(view, options) {
        // Close and unbind any existing page view
        if(this.currentView && _.isFunction(this.currentView.close)) this.currentView.close();

        // Establish the requested view into scope
        this.currentView = view;
        this.currentView.render();
    }
});
