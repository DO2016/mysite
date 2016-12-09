window.DetailsView = Backbone.View.extend({
    initialize: function () {
        console.log('Initializing Details View');
        this.$el = $("#content");
    },

    render: function (id, breadcrumbs, headerView) {
        console.log('ProductListView: Render function');
        this.model = new ProductModel({ id: id });
        self = this;

        this.model.fetch({
            success: function(model, response, options) {
                console.log("Success: " + response.objects);
                self.$el.html(_.template($("#details_template").html())({ some_item: response }));
                breadcrumbs.push("<a href=\"#details/" + id + "\">" + response.name + "</a>");
                headerView.render(breadcrumbs);
            },
            error: function(model, response, options) {
                console.log('Details view: Error');
            }
        });
        return this;
    },
}); 