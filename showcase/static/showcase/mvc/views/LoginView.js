window.LoginView = Backbone.View.extend({

    initialize: function () {
        console.log('Initializing Login View');
        this.model = new AuthModel({});
        this.$el = $("#content");
    },

    events: {
        "click #loginButton": "login"
    },

    render: function () {
        console.log('Login View : Render function');
        this.$el.html(_.template($("#login_form").html())());
        return this;
    },

    serialize: function() {
        return {
            username: $("#login_username").val(),
            password: $("#inputPassword").val()
        };
    },

    login: function (event) {
        console.log('Loggin in... ');
        event.preventDefault();
        var userData = this.serialize();
        var header = userData.username + ':' + userData.password;

        this.header = "Basic ".concat(btoa(header)); 
        self = this;
        this.model.fetch({ beforeSend:
            function(xhr) {
                xhr.setRequestHeader('Authorization', self.header);
            },
            success: function (collection, response, options) {
                console.log(response.objects[0].key);
                var api_key = "ApiKey ".concat(userData.username + ':' + response.objects[0].key);
                $.cookie("api_key", api_key);

                console.log(window.AppRouter);
                window.router.navigate("/products", true);
            }
        });
    }
});
