
$(function(){

var Link = Backbone.Model.extend({

  last_access_dt: function() {
    return Date.parseExact(this.get('last_access').slice(0, 19), "yyyy-MM-ddTHH:mm:ss");
  }
});

var LinkList = Backbone.Collection.extend({
  model: Link,
  url: '/api/bookmark',
  parse: function(response) {
  return response.objects;
  },
  comparator: function(a, b) {
    var i = a.last_access_dt();
  var j = b.last_access_dt();
  if (i > j) return -1;
  if (i < j) return 1;
  return 0;
  } 
});

var LinkView = Backbone.View.extend({
  tagName: 'section',
  className: 'site',
  template: _.template('<a class="link-box" href="/k/<%= id %>"><%= title %></a>'),
  initialize: function(){
    this.listenTo(this.model, 'change', this.render);
    this.listenTo(this.model, 'destroy', this.remove);
  },
  render: function(){
    this.$el.html(this.template(this.model.attributes));
  return this;
  },
  events: {
    'click .link-box': 'click'
  },
  click: function(event){
    if (window.app.isEditting) {
      event.preventDefault();
      var model = this.model;
      bootbox.dialog({
        title: "Edit link",
        message: '<input class="bootbox-input bootbox-input-text form-control" autocomplete="off" type="text" name="edit-link-name" value="' + model.get('title') + '">',
        buttons: {
          remove: {
            label: 'Delete',
            className: 'btn-danger',
            callback: function() {
              model.destroy();
            }
          },
          save: {
            label: 'Save',
            className: 'btn-primary',
            callback: function() {
              var val = $('input[name="edit-link-name"]').val();
              model.save({ 'title': val });
            }
          }
        }
      });
    }
  }
});

var Home = Backbone.View.extend({
  links: new LinkList(),
  initialize: function(){
    this.listenTo(this.links, 'reset', this.addAll);
    this.links.fetch({ reset: true });
    this.isEditting = false;
  },
  addOne: function(it){
    var view = new LinkView({model: it});
  this.$el.append(view.render().el);
  },
  addAll: function(){
    this.links.sortBy(function(it){ return it.last_access_dt(); });
    this.links.each(this.addOne, this);
  }
});

window.app = new Home({ el: $('.sites')[0] });

var AppRouter = Backbone.Router.extend({
  routes: {
    '': 'home',
    'edit': 'edit'
  },
  home: function(){
    window.app.isEditting = false;
  },
  edit: function(){
    window.app.isEditting = true;
  }
});

window.appRouter = new AppRouter();
Backbone.history.start();

});
