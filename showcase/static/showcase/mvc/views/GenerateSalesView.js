window.GenerateSalesView = Backbone.View.extend({

    initialize: function () {
        console.log('Initializing Generate Sales View');
        this.model = new GenerateSalesCollection({});
        this.$el = $("#header_content");
    },

    events: {
        "click #generateButton": "generate"
    },

    render: function () {
        console.log('Generate Sales View : Render function');
        $("#content").html('');
        this.$el.html(_.template($("#generation_template").html())({ header: "Random sales generation page" }));
        self = this;

        $('#generationButton').on('click', function (e) {
           self.generate();
        })

        return this;
    },

    generate: function () {
        console.log('Generating... ');
        self = this;

        this.model.fetch({ 
            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', $.cookie("api_key"));
            },
            error: function (model, response) {
                console.log("Generation error");
            },
            success: function (collection, response, options) {
                console.log("Generation is Successful.");
            }
        });
    }
});