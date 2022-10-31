let cartIcon = "i.fas.fa-shopping-basket";

addPizza = (data) => {
  rotateAnimation($(cartIcon)[0], 1);

  let parent = data.closest(".pizza");
  let price = parent.querySelector(".product-price").innerText;
  let pizza_name = parent.querySelector(".pizza-name").innerText;

  let params = { price: price, pizza_name: pizza_name };

  $.ajax({
    type: "POST",
    url: "/add_pizza",
    data: JSON.stringify(params),
    contentType: "application/json",
    success: function (result) {
      console.log(result);

      let backet = $(".basket-order-list")[0];
      backet.innerHTML = "";
      let backet_total = $(".basket-total-price")[0];

      if(result == null){
        let new_item = `<div class="empty-basket" style="">Cart is empty!</div>`
        backet.insertAdjacentHTML("beforeend", new_item);
        backet_total.innerHTML = "0.00";
        return;
      }

      for (const [key, value] of Object.entries(result)) {
        if(key == "total"){
          backet_total.innerHTML = value;
          return;
        }
        let new_item =`
        <li class="basket-order-item">
            <div class="item-details">
                <a href="#" onclick="removeItem(this);return false;" class="basket-remove-item">
                    <i class="fas fa-times"></i>
                </a>
                <span class="basket-amount-item">` + value.count + `</span>
                x
                <span class="basket-name-item">` + key + `</span>
            </div>
      
            <span class="basket-price-item">` + value.price + `$</span>
        </li>`;
        backet.insertAdjacentHTML("beforeend", new_item);
      };
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


removeItem = (data) => {

  let item = data.closest(".basket-order-item");
  let amount = $(item).find(".basket-amount-item")[0].innerText;
  let name = $(item).find(".basket-name-item")[0].innerText;
  let price = $(item).find(".basket-price-item")[0].innerText.replace("$", "").replace(" ", "");
  let params = { "amount": amount, "name": name, "price": price };
  console.log(params);

  $.ajax({
    type: "POST",
    url: "/remove_item",
    data: JSON.stringify(params),
    contentType: "application/json",
    success: function (result) {
      console.log(result);
      item.remove();
      let total = result["total"];
      if(total == 0){
        total = "0.00";
        let backet = $(".basket-order-list")[0];
        let new_item = `<div class="empty-basket" style="">Cart is empty!</div>`
        backet.insertAdjacentHTML("beforeend", new_item);
      }
      $(".basket-total-price")[0].innerText = total;
    },
    error: function (result, status) {
      console.log(result);
    },
  });
}

let modal = $("#modal")[0];

showModal = () => {
  modal.classList.add("show-modal");
  querySelectorAll("*:not(.modal)");
}
hideModal = () => {
  modal.classList.remove("show-modal");
}

completeOrder = () => {
  hideModal();

  let params = "";

  $.ajax({
    type: "POST",
    url: "/complete_order",
    data: JSON.stringify(params),
    contentType: "application/json",
    success: function (result) {
      console.log(result);
      // window.location.replace(result["url"]);
      window.location = result["url"] + '?json=' + encodeURIComponent(JSON.stringify(result));
    },
    error: function (result, status) {
      console.log(result);
    },
  });

}

