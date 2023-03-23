
function addItemToCart(e) {
    let itemID = undefined
    
    e.currentTarget.classList.forEach(cls => {
        if (cls.startsWith("itemID")) {
            itemID = cls.split("-")[1];
            return;
        }
    });

    if (!itemID)
        return;

    $.ajax({
        url: `/api/cart/add?item_id=${itemID}`, 
        type: "PUT", 
        success: function (data) {
            $(e.currentTarget).find("span").first().text("В кошику");
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
}

function removeItemFromCart(e) {
    let itemID = undefined
    
    e.currentTarget.classList.forEach(cls => {
        if (cls.startsWith("itemID")) {
            itemID = cls.split("-")[1];
            return;
        }
    });

    if (!itemID)
        return;

    $.ajax({
        url: `/api/cart/remove?item_id=${itemID}`, 
        type: "DELETE", 
        success: function (data) {
            $(e.currentTarget).parents(".cartItem").remove();
            $(`.itemID-${itemID}`).eq(0).find("span").first().text("До кошика");

            if ($("#cartPopup").find(".cartItem").length == 0) {
                $("#cartBuyItemsButton").hide();
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
}

$(document).ready(() => {
    $(".addItemToCartButton").click(addItemToCart);
    $(".removeItemFromCartButton").click(removeItemFromCart);
})
