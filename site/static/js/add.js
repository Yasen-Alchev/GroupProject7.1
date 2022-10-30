let cartIcon = "i.fas.fa-shopping-basket";

addPizza = (data) => {
  rotateAnimation($(cartIcon)[0], 1);

  let parent = data.closest(".pizza");
  let price = parent.querySelector(".product-price").innerText;
  let pizza_name = parent.querySelector(".pizza-name").innerText;

  var params = { price: price, pizza_name: pizza_name };

  $.ajax({
    type: "POST",
    url: "/add_pizza",
    data: JSON.stringify(params),
    contentType: "application/json",
    success: function (result) {
      console.log(result);
      window.location.replace('/', cart=result);
    },
    error: function (result, status) {
      console.log(result);
    },
  });
};

toggleCart = () => {
  let basketClasses = $("div.basket-wrapper")[0].classList;

  if (basketClasses.contains("show-basket")) {
    basketClasses.remove("show-basket");
    return;
  }

  basketClasses.add("show-basket");
};

var degrees = 0;

function rotateAnimation(elem, speed) {
  if (navigator.userAgent.match("Chrome")) {
    elem.style.WebkitTransform = "rotate(" + degrees + "deg)";
  } else if (navigator.userAgent.match("Firefox")) {
    elem.style.MozTransform = "rotate(" + degrees + "deg)";
  } else if (navigator.userAgent.match("MSIE")) {
    elem.style.msTransform = "rotate(" + degrees + "deg)";
  } else if (navigator.userAgent.match("Opera")) {
    elem.style.OTransform = "rotate(" + degrees + "deg)";
  } else {
    elem.style.transform = "rotate(" + degrees + "deg)";
  }

  degrees += 5;
  if (degrees == 365) {
    degrees = 0;
    return;
  }

  setTimeout(() => {
    rotateAnimation(elem, speed);
  }, speed);

}
