// =========================================================
// DOOMART
// =========================================================


const MAX_PRODUCTS = 5;

const STORAGE_KEY = "doomart_cart";

let cart = loadCart();


document.addEventListener("DOMContentLoaded", () => {

    setupCart();

    setupAddButtons();

    setupTicketButton();

    setupStreak();

    renderCart();

    updateAddButtons();

});


// =========================================================
// DOOMCART
// =========================================================

function setupCart() {

    const openButton =
        document.getElementById("doomcart-toggle");

    const closeButton =
        document.getElementById("doomcart-close");

    const overlay =
        document.getElementById("cart-overlay");


    if (openButton) {
        openButton.addEventListener("click", openCart);
    }


    if (closeButton) {
        closeButton.addEventListener("click", closeCart);
    }


    if (overlay) {
        overlay.addEventListener("click", closeCart);
    }

}


function openCart() {

    const panel =
        document.getElementById("doomcart");

    const overlay =
        document.getElementById("cart-overlay");


    panel.classList.add("open");

    overlay.classList.add("open");

    document.body.style.overflow = "hidden";

}


function closeCart() {

    const panel =
        document.getElementById("doomcart");

    const overlay =
        document.getElementById("cart-overlay");


    panel.classList.remove("open");

    overlay.classList.remove("open");

    document.body.style.overflow = "";

}


// =========================================================
// LOCAL STORAGE
// =========================================================

function loadCart() {

    try {

        const saved =
            localStorage.getItem(STORAGE_KEY);


        if (!saved) {
            return [];
        }


        const parsed =
            JSON.parse(saved);


        return Array.isArray(parsed)
            ? parsed
            : [];


    } catch (error) {

        console.error(
            "Error cargando DOOMCART:",
            error
        );

        return [];

    }

}


function saveCart() {

    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(cart)
    );

}


// =========================================================
// AGREGAR PRODUCTOS
// =========================================================

function setupAddButtons() {

    const buttons =
        document.querySelectorAll(".add-to-cart");


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                addToCart(
                    button.dataset.productId,
                    button.dataset.productName,
                    button.dataset.company
                );

            }
        );

    });

}


function addToCart(
    id,
    name,
    company
) {

    if (cart.length >= MAX_PRODUCTS) {

        alert(
            "El DOOMCART permite máximo 5 productos."
        );

        return;

    }


    const exists =
        cart.some(
            item => item.id === id
        );


    if (exists) {

        alert(
            "Este producto ya está en el DOOMCART."
        );

        return;

    }


    cart.push({
        id: id,
        name: name,
        company: company
    });


    saveCart();

    renderCart();

    updateAddButtons();

    openCart();

}


// =========================================================
// ELIMINAR
// =========================================================

function removeFromCart(id) {

    cart =
        cart.filter(
            item => item.id !== id
        );


    saveCart();

    renderCart();

    updateAddButtons();

}


// =========================================================
// RENDER CARRITO
// =========================================================

function renderCart() {

    const container =
        document.getElementById("cart-items");

    const counter =
        document.getElementById("cart-count");


    if (!container || !counter) {
        return;
    }


    counter.textContent =
        cart.length;


    if (cart.length === 0) {

        container.innerHTML = `

            <div class="cart-empty">

                El DOOMCART está vacío.

            </div>

        `;

        return;

    }


    container.innerHTML =
        cart.map(item => `

            <div class="cart-item">

                <div class="cart-item-header">

                    <div>

                        <div class="cart-item-name">
                            ${escapeHtml(item.name)}
                        </div>

                        <div class="cart-item-company">
                            ${escapeHtml(item.company)}
                        </div>

                    </div>


                    <button
                        type="button"
                        class="remove-cart-item"
                        data-remove-id="${item.id}"
                    >
                        ×
                    </button>

                </div>

            </div>

        `).join("");


    document
        .querySelectorAll(".remove-cart-item")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    removeFromCart(
                        button.dataset.removeId
                    );

                }
            );

        });

}


// =========================================================
// ESTADO DE BOTONES
// =========================================================

function updateAddButtons() {

    const buttons =
        document.querySelectorAll(".add-to-cart");


    buttons.forEach(button => {

        const id =
            button.dataset.productId;


        const exists =
            cart.some(
                item => item.id === id
            );


        if (exists) {

            button.disabled = true;

            button.textContent =
                "YA ESTÁ EN DOOMCART";

            return;

        }


        if (cart.length >= MAX_PRODUCTS) {

            button.disabled = true;

            button.textContent =
                "LÍMITE DE 5";

            return;

        }


        button.disabled = false;

        button.innerHTML = `

            <img
                src="/static/img/logo.png"
                alt=""
                class="button-logo"
            >

            AGREGAR AL DOOMCART

        `;

    });

}


// =========================================================
// TICKET
// =========================================================

function setupTicketButton() {

    const button =
        document.getElementById(
            "generate-ticket"
        );


    if (!button) {
        return;
    }


    button.addEventListener(
        "click",
        () => {

            if (cart.length === 0) {

                showEmptyCartModal();

                return;

            }


            alert(
                "DOOMCART preparado. El TICKET DE DAÑO se conectará en la Parte 4."
            );

        }
    );

}


// =========================================================
// MODAL
// =========================================================

function showEmptyCartModal() {

    const modal =
        document.getElementById(
            "emptyCartModal"
        );


    modal.classList.add("show");

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        const closeButton =
            document.getElementById(
                "close-empty-modal"
            );


        if (!closeButton) {
            return;
        }


        closeButton.addEventListener(
            "click",
            () => {

                const modal =
                    document.getElementById(
                        "emptyCartModal"
                    );


                modal.classList.remove("show");

            }
        );

    }
);


// =========================================================
// RACHA
// =========================================================

function setupStreak() {

    const number =
        document.getElementById(
            "streak-number"
        );

    const addDay =
        document.getElementById(
            "add-day"
        );

    const breakStreak =
        document.getElementById(
            "break-streak"
        );


    if (
        !number ||
        !addDay ||
        !breakStreak
    ) {
        return;
    }


    let days =
        Number(
            localStorage.getItem(
                "doomart_streak"
            )
        ) || 0;


    let lastDay =
        localStorage.getItem(
            "doomart_last_day"
        );


    number.textContent =
        days;


    addDay.addEventListener(
        "click",
        () => {

            const now =
                Date.now();

            const DAY =
                24 * 60 * 60 * 1000;


            if (
                lastDay &&
                now - Number(lastDay) < DAY
            ) {

                alert(
                    "Todavía no han pasado 24 horas."
                );

                return;

            }


            days += 1;

            lastDay =
                String(now);


            localStorage.setItem(
                "doomart_streak",
                days
            );


            localStorage.setItem(
                "doomart_last_day",
                lastDay
            );


            number.textContent =
                days;

        }
    );


    breakStreak.addEventListener(
        "click",
        () => {

            days = 0;

            lastDay = null;


            localStorage.removeItem(
                "doomart_streak"
            );


            localStorage.removeItem(
                "doomart_last_day"
            );


            number.textContent =
                "0";

        }
    );

}


// =========================================================
// SEGURIDAD HTML
// =========================================================

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}