// =========================================================
// DOOMART
// =========================================================


const MAX_PRODUCTS = 5;

const STORAGE_KEY = "doomart_cart";

let cart = loadCart();


document.addEventListener(
    "DOMContentLoaded",
    () => {

        setupCart();

        setupAddButtons();

        setupTicketButton();

        setupBreakTicket();

        setupStreak();

        renderCart();

        updateAddButtons();

    }
);


// =========================================================
// DOOMCART
// =========================================================

function setupCart() {

    const openButton =
        document.getElementById(
            "doomcart-toggle"
        );


    const closeButton =
        document.getElementById(
            "doomcart-close"
        );


    const overlay =
        document.getElementById(
            "cart-overlay"
        );


    if (openButton) {

        openButton.addEventListener(
            "click",
            openCart
        );

    }


    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closeCart
        );

    }


    if (overlay) {

        overlay.addEventListener(
            "click",
            closeCart
        );

    }

}


function openCart() {

    const panel =
        document.getElementById(
            "doomcart"
        );


    const overlay =
        document.getElementById(
            "cart-overlay"
        );


    panel.classList.add("open");

    overlay.classList.add("open");

    document.body.style.overflow =
        "hidden";

}


function closeCart() {

    const panel =
        document.getElementById(
            "doomcart"
        );


    const overlay =
        document.getElementById(
            "cart-overlay"
        );


    panel.classList.remove("open");

    overlay.classList.remove("open");

    document.body.style.overflow =
        "";

}


// =========================================================
// LOCAL STORAGE
// =========================================================

function loadCart() {

    try {

        const saved =
            localStorage.getItem(
                STORAGE_KEY
            );


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
// AGREGAR
// =========================================================

function setupAddButtons() {

    const buttons =
        document.querySelectorAll(
            ".add-to-cart"
        );


    buttons.forEach(
        button => {

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

        }
    );

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
// RENDER DOOMCART
// =========================================================

function renderCart() {

    const container =
        document.getElementById(
            "cart-items"
        );


    const counter =
        document.getElementById(
            "cart-count"
        );


    if (
        !container ||
        !counter
    ) {

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
        cart.map(
            item => `

                <div class="cart-item">

                    <div
                        class="cart-item-header"
                    >

                        <div>

                            <div
                                class="cart-item-name"
                            >
                                ${escapeHtml(
                                    item.name
                                )}
                            </div>

                            <div
                                class="cart-item-company"
                            >
                                ${escapeHtml(
                                    item.company
                                )}
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

            `
        ).join("");


    document
        .querySelectorAll(
            ".remove-cart-item"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        removeFromCart(
                            button.dataset.removeId
                        );

                    }
                );

            }
        );

}


// =========================================================
// BOTONES
// =========================================================

function updateAddButtons() {

    const buttons =
        document.querySelectorAll(
            ".add-to-cart"
        );


    buttons.forEach(
        button => {

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


            if (
                cart.length >=
                MAX_PRODUCTS
            ) {

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

        }
    );

}


// =========================================================
// PARTE 4
// GENERAR TICKET
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
        generateTicket
    );

}


async function generateTicket() {

    if (cart.length === 0) {

        showEmptyCartModal();

        return;

    }


    const button =
        document.getElementById(
            "generate-ticket"
        );


    button.disabled = true;

    button.textContent =
        "GENERANDO TICKET...";


    try {

        const response =
            await fetch(
                "/api/ticket",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        productos:
                            cart.map(
                                item =>
                                    item.id
                            )
                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.ok) {

            throw new Error(
                data.error ||
                "No se pudo generar el ticket."
            );

        }


        renderDamageTicket(
            data.productos
        );


        closeCart();

        openDamageTicket();


    } catch (error) {

        console.error(error);

        alert(
            error.message
        );

    } finally {

        button.disabled = false;

        button.textContent =
            "GENERAR TICKET";

    }

}


// =========================================================
// MOSTRAR TICKET
// =========================================================

function openDamageTicket() {

    const overlay =
        document.getElementById(
            "damage-ticket-overlay"
        );


    const ticket =
        document.getElementById(
            "damage-ticket"
        );


    if (!overlay || !ticket) {

        return;

    }


    ticket.classList.remove(
        "breaking"
    );


    overlay.classList.add(
        "show"
    );


    document.body.style.overflow =
        "hidden";

}


// =========================================================
// CONTENIDO DEL TICKET
// =========================================================

function renderDamageTicket(
    productos
) {

    const container =
        document.getElementById(
            "ticket-products"
        );


    if (!container) {

        return;

    }


    container.innerHTML =
        productos.map(
            producto => `

                <article
                    class="ticket-product"
                >

                    <img
                        src="/static/img/${escapeHtml(
                            producto.imagen
                        )}"
                        alt="${escapeHtml(
                            producto.nombre
                        )}"
                        class="ticket-product-image"
                    >


                    <div
                        class="ticket-product-content"
                    >

                        <span
                            class="ticket-company"
                        >
                            ${escapeHtml(
                                producto.empresa
                            )}
                        </span>


                        <h3>
                            ${escapeHtml(
                                producto.nombre
                            )}
                        </h3>


                        <span
                            class="ticket-label"
                        >
                            ${escapeHtml(
                                producto.etiqueta
                            )}
                        </span>


                        <p>
                            ${escapeHtml(
                                producto.descripcion
                            )}
                        </p>


                        <div
                            class="ticket-data"
                        >

                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Características
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.caracteristicas
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Daño al suelo
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.danio_suelo
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Daño al aire
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.danio_aire
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Daño al agua
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.danio_agua
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Uso de recursos
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.uso_recursos
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Residuos
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.plasticos_residuos
                                    )}
                                </span>

                            </div>


                            <div
                                class="ticket-data-row"
                            >

                                <strong>
                                    Fuente
                                </strong>

                                <span>
                                    ${escapeHtml(
                                        producto.fuente
                                    )}
                                </span>

                            </div>

                        </div>

                    </div>

                </article>

            `
        ).join("");

}


// =========================================================
// ROMPER TICKET
// =========================================================

function setupBreakTicket() {

    const button =
        document.getElementById(
            "break-ticket"
        );


    const overlay =
        document.getElementById(
            "damage-ticket-overlay"
        );


    if (!button || !overlay) {

        return;

    }


    button.addEventListener(
        "click",
        () => {

            const ticket =
                document.getElementById(
                    "damage-ticket"
                );


            ticket.classList.add(
                "breaking"
            );


            setTimeout(
                () => {

                    overlay.classList.remove(
                        "show"
                    );


                    ticket.classList.remove(
                        "breaking"
                    );


                    document.body.style.overflow =
                        "";


                },
                550
            );

        }
    );

}


// =========================================================
// MODAL CARRITO VACÍO
// =========================================================

function showEmptyCartModal() {

    const modal =
        document.getElementById(
            "emptyCartModal"
        );


    if (modal) {

        modal.classList.add(
            "show"
        );

    }

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


                modal.classList.remove(
                    "show"
                );

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
                24 *
                60 *
                60 *
                1000;


            if (
                lastDay &&
                now -
                Number(lastDay) <
                DAY
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
// SEGURIDAD
// =========================================================

function escapeHtml(value) {

    if (value === null ||
        value === undefined) {

        return "";

    }


    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}