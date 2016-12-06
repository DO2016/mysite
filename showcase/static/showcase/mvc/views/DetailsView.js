window.DetailsView = Backbone.View.extend({
    initialize: function () {
        console.log('Initializing Details View');
        this.$el = $("#content");
    },

    getObj: function(obj) {
       return obj.id == this.id;
    },

    render: function (id, breadcrumbs, headerView) {
        console.log('ProductListView: Render function');
        this.model = new ProductModel({ id: id });
        self = this;

        this.model.fetch({
            success: function(model, response, options) {
                console.log("Success: " + response.objects);
                this.id = id;
                var filtered = response.objects.filter(self.getObj);

                if (filtered.length > 0) {
                    var prod = filtered[0];
                    self.$el.html(_.template($("#details_template").html())({ some_item: prod }));

                    if (breadcrumbs.length <= 1) {
                        breadcrumbs.push("<a href=\"#products\">Products </a>");
                    }
                    breadcrumbs.push("<a href=\"#details/" + id + "\">" + prod.name + "</a>");
                    headerView.render(breadcrumbs);
                }
            },
            error: function(model, response, options) {
                console.log('Details view: Error');
            }
        });
        return this;
    },
}); 