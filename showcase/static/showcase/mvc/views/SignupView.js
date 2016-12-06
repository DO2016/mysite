window.SignupView = Backbone.View.extend({

    initialize: function () {
        console.log('Initializing Registration View');
        this.model = new RegistrationModel({});
        this.$el = $("#content");
    },

    render: function () {
        console.log("Render Signup View");
        self = this;
        self.$el.html(_.template($("#signup_template").html())({}));

        $('#signupButton').on('click', function (e) {
            var userData = self.serialize();
            var userModel = new CustomUserModel(userData);

            userModel.save(null, {
                success: function (model, response) {
                    console.log("Success saving user model");
                    window.router.navigate("#products", true);

                },
                error: function (model, response) {
                    console.log("Error saving user model");
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('Authorization', $.cookie("api_key"));
                }
            });
        })
        return this;
    },

    serialize: function() {
        return {
            username: $("#username").val(),
            first_name: $("#first_name").val(),
            last_name: $("#last_name").val(),
            password: $("#password").val(),
            email: $("#email").val(),
            is_active: "f"
        };
    },
});
