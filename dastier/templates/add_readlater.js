javascript:(
  function() {
    var url = '{{ url_for("readitlater.add", _external=True) }}';
    var args = [
      'title=' + encodeURIComponent(document.title),
      'url=' + encodeURIComponent(document.location.href)
    ];
    var redirect = url + '?' + args.join('&');
    window.open(redirect, '_blank');
  }
)()
