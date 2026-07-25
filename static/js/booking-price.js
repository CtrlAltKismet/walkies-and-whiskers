document.addEventListener("DOMContentLoaded", () => {
    const serviceSelect = document.getElementById("id_service");
    const priceDisplay = document.getElementById(
        "service-price-display"
    );
    const priceDataElement = document.getElementById(
        "service-prices"
    );

    if (!serviceSelect || !priceDisplay || !priceDataElement) {
        return;
    }

    const servicePrices = JSON.parse(
        priceDataElement.textContent
    );

    function updatePriceDisplay() {
        const selectedServiceId = serviceSelect.value;
        const selectedPrice = servicePrices[selectedServiceId];

        if (selectedPrice) {
            priceDisplay.innerHTML = `
                <p>
                    <strong>Selected service price:</strong>
                    £${selectedPrice}
                </p>
            `;
        } else {
            priceDisplay.innerHTML = `
                <p>
                    Select a service to view its price.
                </p>
            `;
        }
    }

    serviceSelect.addEventListener(
        "change",
        updatePriceDisplay
    );

    updatePriceDisplay();
});