var callback_error = function (element) {
  element.src = "/static/images/transparent.png";
};

var ll = new LazyLoad({
  threshold: 0,
  callback_error: callback_error,
});
