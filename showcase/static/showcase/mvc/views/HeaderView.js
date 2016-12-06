window.HeaderView = Backbone.View.extend({

    initialize: function () {
        console.log('Initializing Registration View');
        this.model = new RegistrationModel({});
        this.$el = $("#header_content");
    },

    render: function (breadcrumbs) {
        self = this;
        console.log("Render HeaderView");     
        self.$el.html(_.template($("#header_template").html())({ breadcrumbs: breadcrumbs }));

        if (!$.cookie('api_key')) {
            $('#logoutButton').hide();
            $('#loginButton').show();
        }
        else {
            $('#logoutButton').on('click', function (e) {
                $.removeCookie('api_key', { path: '/showcase/' });
                self.$el.html("");
                window.router.navigate("", true);
            })
            $('#loginButton').hide();
            $('#logoutButton').show();
        }
        $('#regButton').on('click', function (e) {
            var userData = self.serialize();
            var userModel = new CustomUserModel(userData);

            userModel.save(null, {
                success: function (model, response) {
                    console.log("Success saving user model");

                    $('#regModal').modal('hide');
                    $('#regModal').on('hidden.bs.modal', function () {
                        Backbone.history.stop();
                        Backbone.history.start();
                    })
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