window.ProductListView = Backbone.View.extend({
    initialize: function () {
        console.log('Initializing ProductList View');
        this.collection = new ProductCollection();
        this.$el = $("#content");
    },

    serialize: function() {
        return {
            name: $("#name").val(),
            price: $("#price").val(),
            currency : "/api/v1/CurrencyResource/1/",
            is_published: "t"
        };
    },

    setVisibility: function () {
        if (!$.cookie('api_key')) { 
            $('#newProductButton').hide();
        } 
        else {
            $('#newProductButton').show();
        }        
    },

    render: function () {
        console.log('ProductListView: Render function');
        self = this;
        this.collection.fetch({ beforeSend: function(xhr) {
                console.log('ProductListView: beforeSend');
                console.log($.cookie("api_key"));
                xhr.setRequestHeader('Authorization', $.cookie("api_key"));
            },
            success: function(collection, response, options) {
                console.log("Success: " + response.objects);                
                self.$el.html(_.template($("#products_template").html())({ product_list: response.objects }));
                self.setVisibility();

                $('#addButton').on('click', function (e) {
                    var userData = self.serialize();
                    var productModel = new AddProductModel(userData);

                    productModel.save(null, {
                        success: function (model, response) {
                            console.log("Success saving model");
                            $('#myModal').modal('hide');
                            $('#myModal').on('hidden.bs.modal', function () {
                                window.router.products();
                            })
                        },
                        error: function (model, response) {
                            console.log("Error saving model");
                        },
                        beforeSend: function(xhr) {
                            xhr.setRequestHeader('Authorization', $.cookie("api_key"));
                        }
                    });
                })
            },
            error: function(collection, response, options) {
                console.log('ProductListView: Error');
            }
        });
        return this;
    },
});