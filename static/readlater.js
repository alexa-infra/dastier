
$(function(){

var ReadLater = Backbone.Model.extend({
});

var ReadLaterList = Backbone.Collection.extend({
  model: ReadLater,
  url: '/api/readitlater',
  num_results: 0,
  page: 1,
  num_pages: 1,
  parse: function(response){
    this.num_results = response.num_results;
    this.page = response.page;
    this.num_pages = response.total_pages;
    return response.objects;
  }
});

var ReadLaterView = Backbone.View.extend({
  tagName: 'li',
  template: _.template($('#item-template').text()),
  initialize: function(){
    this.listenTo(this.model, 'change', this.render);
    this.listenTo(this.model, 'destroy', this.remove);
  },
  render: function(){
    this.$el.html(this.template(this.model.attributes));
    this.readcheckbox = this.$('.mark-read')[0];
    return this;
  },
  events: {
    'click .close': 'markdelete',
    'click .mark-read': 'markread'
  },
  markdelete: function(){
    var model = this.model;
    bootbox.confirm('Are you sure?', function(result){
      if (result)
        model.destroy();
    });
  },
  markread: function(){
    var val = this.readcheckbox.checked;
    this.model.save({ 'readed': val });
  }
});

var Reader = Backbone.View.extend({
  items: new ReadLaterList(),
  searchQuery: '',
  initialize: function(){
    this.listenTo(this.items, 'reset', this.addAll);
  },
  update: function(page) {
    var query = {};
    var order = [{'field': 'created', 'direction': 'desc'}];
    query.order_by = order;
    if (this.searchQuery) {
      var filters = [{'name': 'title', 'op': 'like', 'val': '%' + this.searchQuery + '%'}];
      query.filters = filters;
    }
    this.items.fetch({ reset: true,
      data: {
        'q': JSON.stringify(query),
        'page': page
      }
    });
  },
  addOne: function(it){
    var view = new ReadLaterView({ model: it });
    this.$el.append(view.render().el);
  },
  addAll: function(){
    this.clear();
    this.items.each(this.addOne, this);
    this.render();
  },
  clear: function(){
    this.$el.empty();
  },
  render: function(){
    var tmpl = _.template($('#paginator-tmpl').html());
    $('#paginator').html(tmpl({
      page: this.items.page,
      num_pages: this.items.num_pages,
      num_results: this.items.num_results,
      query: (this.searchQuery) ? ('search/' + this.searchQuery) : 'page'
    }));
    return this;
  },
  search: function(q){
    this.searchQuery = q;
  }
});

var AppRouter = Backbone.Router.extend({
  routes: {
    '': 'home',
    'page/:page': 'paged',
    'search/:query': 'searchFirst',
    'search/:query/:page': 'search'
  },
  go: function(q, page) {
    window.app.search(q);
    window.app.update(page);
  },
  home: function(){
    this.go('', 1);
  },
  paged: function(page){
    this.go('', page);
  },
  searchFirst: function(query){
    this.go(query, 1);
  },
  search: function(query, page){
    this.go(query, page);
  }
});

window.app = new Reader({ el: $('#read-list') });
window.appRouter = new AppRouter();
Backbone.history.start();

$('#search').keyup(function(){
  var term = $(this).val().toLowerCase();
  term = term.replace(/\s/g, '');
  if (term)
    window.appRouter.navigate('search/' + term, { trigger: true, replace: true });
  else
    window.appRouter.navigate('', { trigger: true });
});
$('#search').focus();

});
